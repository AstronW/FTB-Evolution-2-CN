"""Build, check and install the consolidated FTB Evolution 2 zh_CN release pack.

Everything shipped here is derived from *explicit* project manifests instead of a
blind copy of the work copy. The work copy `.minecraft/` stays the only place the
individual stage builders write to; this tool only reads from it.

Consolidated inputs and where they go:

| Part | Origin | Destination |
| --- | --- | --- |
| KubeJS/ordinary language overlays | `localization/ordinary/batch-*/manifest.json`, `localization/custom/source-bindings-1.4.0.json` | resource pack `assets/<ns>/lang/zh_cn.json` |
| Manuals (GuideME/MDX) | `.minecraft/resourcepacks/FTB-Evolution-2-Manuals-zh_CN` | resource pack `assets/**` |
| Reviewed CFPA/PR overlay | `localization/cfpa_review/build-manifest.json` | resource pack `assets/**` + notices |
| Quest book language | `.minecraft/config/ftbquests/quests/lang/zh_cn` | instance `config/ftbquests/quests/lang/zh_cn` |
| Pack dialog / echo definitions | `localization/custom/batches/batch-001|002` | instance `datapacks/ftb/...` |
| Runtime message scripts | `localization/custom/batches/batch-004` | instance `kubejs/server_scripts/...` |

Nothing is copied from the work copy wholesale, no mod JAR is touched and no
player save or config outside the listed paths is modified. `install` always
backs up the exact files it replaces.
"""
import argparse
import collections
import datetime
import hashlib
import io
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
MC = ROOT / '.minecraft'
ORDINARY = ROOT / 'localization/ordinary'
CUSTOM = ROOT / 'localization/custom'
CFPA_REVIEW = ROOT / 'localization/cfpa_review'
MANUALS_PACK = MC / 'resourcepacks/FTB-Evolution-2-Manuals-zh_CN'
CFPA_PACK = MC / 'resourcepacks/FTB-Evolution-2-CFPA-Reviewed-zh_CN'
QUEST_LANG = MC / 'config/ftbquests/quests/lang/zh_cn'
DIST = ROOT / 'dist'
VERSION = '1.4.0'
PACK_NAME = f'FTB-Evolution-2-{VERSION}-zh_CN'
RESOURCEPACK = DIST / f'{PACK_NAME}.zip'
INSTALL_ZIP = DIST / f'{PACK_NAME}-install.zip'
RELEASE_MANIFEST = DIST / f'{PACK_NAME}-manifest.json'
INSTALL_RECORD = DIST / f'{PACK_NAME}-installation.json'
# Namespaces left in the work copy by earlier baselines with no current source.
# `power_armor` is a 1.3.2 leftover whose content was removed in 1.4.0; it has no
# ordinary/custom manifest and is deliberately not shipped.
STALE_NAMESPACES = {'power_armor'}


def read(path):
    return json.loads((ROOT / path if not isinstance(path, pathlib.Path) else path).read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def instance_dir():
    game = pathlib.Path(read(ROOT / 'project.json')['target_instance'])
    assert game.is_dir(), f'Target instance missing: {game}'
    instance = read(game / 'instance.json')
    assert instance['version'] == VERSION, f"Instance version changed: {instance['version']}"
    assert instance['mcVersion'] == '26.1.2', f"Minecraft version changed: {instance['mcVersion']}"
    return game


# --------------------------------------------------------------------------- #
# Input inventory
# --------------------------------------------------------------------------- #
def kubejs_language_sources():
    """{[namespace]: [(work-copy path, origin)]} built from stage manifests."""
    sources = collections.defaultdict(list)

    def add(namespace, path, origin):
        sources[namespace].append((path, origin))
    # Ordinary language batches: one namespace each, only completed ones count.
    for folder in sorted(ORDINARY.glob('batch-*')):
        manifest = folder / 'manifest.json'
        if not manifest.exists():
            continue
        data = read(manifest)
        # Unfinished drafts are excluded from every release artifact.
        if not (folder / 'verification.json').exists():
            continue
        add(data['namespace'], ROOT / data['target'], f"ordinary/{folder.name}")
    # Pack custom language namespaces bound to the current instance.
    bindings = read(CUSTOM / 'source-bindings-1.4.0.json')
    for namespace in bindings['sources']:
        add(namespace, MC / f'kubejs/assets/{namespace}/lang/zh_cn.json', 'custom/bindings')
    # Synthetic keys introduced by the runtime scripts (English fallback included).
    for folder in sorted((CUSTOM / 'batches').glob('batch-*')):
        data = read(folder / 'manifest.json')
        synth = data.get('synthetic_language')
        if isinstance(synth, dict):
            add('ftb_custom', ROOT / synth['output_path'], f"custom/{folder.name}")
    # Nothing in the work copy may be shipped without a manifest behind it. Any new
    # namespace here has to be either bound to a source file or listed deliberately.
    installed = {path.parent.parent.name for path in (MC / 'kubejs/assets').glob('*/lang/zh_cn.json')}
    unattributed = installed - set(sources)
    assert unattributed <= STALE_NAMESPACES, (
        'Work copy contains language output without a stage manifest; '
        f'bind it to an English source or exclude it deliberately: {sorted(unattributed)}')
    return sources


def extra_instance_files():
    """Non-resource-pack files that must be installed into the instance."""
    files = {}
    for folder in sorted((CUSTOM / 'batches').glob('batch-*')):
        data = read(folder / 'manifest.json')
        for entry in data.get('files', []):
            # batch-001 only has in-place datapack edits; only changed files ship.
            if not entry.get('changes'):
                continue
            source = MC / entry['source_path']
            assert source.is_file(), str(source)
            files[entry['source_path']] = source
        for script in data.get('scripts', []):
            path = ROOT / script['output_path']
            rel = pathlib.Path(script['source_path'])
            assert path.is_file(), str(path)
            assert digest(path.read_bytes()) == script['output_sha256'], f"Script output drifted: {rel}"
            files[rel.as_posix()] = path
    # Stellaris Wiki pages are server data and cannot be localized through the
    # resource pack.  Ship only pages that have a maintained translation.
    extra = ROOT / 'localization/manuals_extra'
    extra_manifest = extra / 'source_manifest.json'
    if extra_manifest.is_file():
        for path, entry in read(extra_manifest)['documents'].items():
            if not entry['target'].startswith('datapacks/'):
                continue
            translation = extra / 'translations' / path
            assert translation.is_file(), f'Missing extra manual translation: {path}'
            files[entry['target']] = translation
        if any(entry['target'].startswith('datapacks/') for entry in read(extra_manifest)['documents'].values()):
            meta = MC / 'datapacks/ftb_evolution_cn/pack.mcmeta'
            assert meta.is_file(), 'Extra datapack metadata missing; build manual_extra_translation first'
            files['datapacks/ftb_evolution_cn/pack.mcmeta'] = meta
    fixes = ROOT / 'localization/client_fixes'
    for entry in read(fixes / 'manifest.json')['scripts']:
        path = fixes / entry['file']
        assert digest(path.read_bytes()) == entry['sha256'], entry['file']
        files[entry['target']] = path
    return dict(sorted(files.items()))


def cfpa_files():
    manifest = read(CFPA_REVIEW / 'build-manifest.json')['files']
    files = {rel: (CFPA_PACK / rel) for rel in manifest if rel.startswith('assets/')}
    notices = {rel: (CFPA_PACK / rel) for rel in ('CFPA-LICENSE.txt', 'licenses/ANIMAL-PEN-LICENSE.txt', 'ATTRIBUTION.md')}
    for rel, path in notices.items():
        assert path.is_file(), rel
    for rel, path in files.items():
        assert digest(path.read_bytes()) == manifest[rel], f'CFPA output drifted: {rel}'
    return dict(sorted(files.items())), notices


def quest_files():
    assert QUEST_LANG.is_dir(), 'Quest language output missing; build the quest book first'
    files = {}
    for path in sorted(QUEST_LANG.rglob('*')):
        if path.is_file():
            rel = path.relative_to(QUEST_LANG).as_posix()
            files[f'config/ftbquests/quests/lang/zh_cn/{rel}'] = path
    assert files, 'No quest language files found'
    return files


def feedback_files(base_outputs=None):
    """Validate committed feedback artifacts; live sources are checked separately."""
    base = ROOT / 'localization/feedback_20261019'
    manifest = read(base / 'manifest.json')
    if base_outputs is not None:
        for member, sha in manifest['base_files'].items():
            assert member in base_outputs and digest(base_outputs[member][0]) == sha, (
                'Feedback base page changed', member)
    for rel, sha in manifest['files'].items():
        path = base / 'pack' / rel
        assert digest(path.read_bytes()) == sha, rel
        yield rel, path


# --------------------------------------------------------------------------- #
# Resource pack assembly
# --------------------------------------------------------------------------- #
def assemble_resourcepack(conflicts, include_feedback=True):
    """Return {member: (bytes, origin)} for the single consolidated pack."""
    outputs = {}
    language = collections.defaultdict(dict)   # member -> {key: (zh, origin)}
    namespaces = collections.Counter()

    def put_lang(namespace, key, zh, origin, domain='lang'):
        # `group_lang` is a separate Collapsible Groups domain; merging it into
        # `lang` would silently drop those labels.
        assert domain in {'lang', 'group_lang'}, domain
        member = f'assets/{namespace}/{domain}/zh_cn.json'
        previous = language[member].get(key)
        if previous and previous[0] != zh:
            conflicts.append({'member': member, 'key': key, 'a': previous, 'b': (zh, origin)})
        if previous:
            return
        language[member][key] = (zh, origin)
        namespaces[namespace] += 1

    def put_blob(member, path, origin):
        data = path.read_bytes()
        existing = outputs.get(member)
        if existing and existing[0] != data:
            # The Patchouli batch deliberately supersets the reviewed CFPA
            # entries (for example the Modular Routers fake-player note).
            # Manuals are written first and win this specific overlap; any
            # other conflict remains fatal.
            resolution = 'manuals' if existing[1] == 'manuals' and origin == 'cfpa_review' else 'unresolved'
            conflicts.append({'member': member, 'a': (existing[1],), 'b': (origin,), 'resolution': resolution})
            return
        outputs[member] = (data, origin)

    # 1. KubeJS language overlays (ordinary batches + pack custom messages).
    for namespace, entries in sorted(kubejs_language_sources().items()):
        for path, origin in entries:
            assert path.is_file(), f'Missing language output: {path}'
            for key, zh in sorted(json.loads(path.read_text()).items()):
                put_lang(namespace, key, zh, origin)
    # The synthetic ftb_custom keys need their English fallback in the pack too.
    fallback = MC / 'kubejs/assets/ftb_custom/lang/en_us.json'
    if fallback.is_file():
        put_blob('assets/ftb_custom/lang/en_us.json', fallback, 'custom/ftb_custom')

    # 2. Manuals (FTB guides, FTBIC, Nodeworks).
    for path in sorted(MANUALS_PACK.rglob('*')):
        if not path.is_file():
            continue
        member = path.relative_to(MANUALS_PACK).as_posix()
        if member == 'pack.mcmeta':
            continue
        parts = member.split('/')
        if len(parts) == 4 and parts[2] == 'lang' and parts[3] == 'zh_cn.json':
            for key, zh in sorted(json.loads(path.read_text()).items()):
                put_lang(parts[1], key, zh, 'manuals')
        else:
            put_blob(member, path, 'manuals')

    # 3. Reviewed CFPA/PR overlay.
    cfpa, notices = cfpa_files()
    for member, path in cfpa.items():
        parts = member.split('/')
        if len(parts) == 4 and parts[2] in {'lang', 'group_lang'} and parts[3] == 'zh_cn.json':
            for key, zh in sorted(json.loads(path.read_text()).items()):
                put_lang(parts[1], key, zh, 'cfpa_review', parts[2])
        else:
            put_blob(member, path, 'cfpa_review')

    for member, values in sorted(language.items()):
        outputs[member] = (encode({key: zh for key, (zh, _) in values.items()}), 'merged-language')
    if include_feedback:
        for member, path in feedback_files(outputs):
            data = path.read_bytes()
            if member.endswith('/lang/zh_cn.json'):
                merged = json.loads(outputs[member][0]) if member in outputs else {}
                merged.update(json.loads(data))
                data = encode(merged)
            outputs[member] = (data, 'feedback_20261019')
    return outputs, notices, namespaces


def attribution(notices, namespaces, counts):
    lines = [
        '# FTB Evolution 2 简体中文汉化包',
        '',
        f'目标整合包版本 {VERSION} / Minecraft 26.1.2。本包为本项目已通过静态校验部分的汇总产物，不是整包完整汉化。',
        '',
        '## 组成部分',
        '',
        '| 组成部分 | 来源 | 数量 |',
        '| --- | --- | ---: |',
    ]
    for label, value in counts:
        lines.append(f'| {label} | {counts_source(label)} | {value} |')
    lines += [
        '',
        '## 许可与署名',
        '',
        'CFPA 相关译文遵循 CC BY-NC-SA 4.0，见 CFPA-LICENSE.txt；逐条 PR/版本来源见 ATTRIBUTION-CFPA.md。',
        '上游仓库：https://github.com/CFPAOrg/Minecraft-Mod-Language-Package',
        'Animal Pen 的原生修复条目保留 JAR 声明的原许可，见 licenses/ANIMAL-PEN-LICENSE.txt，本包不重新授权这部分内容。',
        '本出库衔的复核、术语统一、语言键映射、版本适配与格式修复由本项目完成。CFPA 未覆盖的名称/正文为本项目自译。',
        '',
        '本产物由项目工作副本生成，未修改模组 JAR、配方、整合包资源与玩家存档。',
    ]
    return ('\n'.join(lines) + '\n').encode()


def counts_source(label):
    return {
        '语言键': 'ordinary/custom 批次 + CFPA 审校',
        '分组名称': 'CFPA 审校 (collapsible_groups)',
        '任务书文件': 'quest_translation',
        '手册/书籍文件': 'manual_translation + CFPA 审校',
        '整合包数据文件': 'custom/batches 001-002',
        '运行时脚本': 'custom/batches 004',
    }.get(label, '本项目')


def compile_release():
    conflicts = []
    outputs, notices, namespaces = assemble_resourcepack(conflicts)
    unresolved = [item for item in conflicts if item.get('resolution') != 'manuals']
    assert not unresolved, json.dumps(unresolved[:5], ensure_ascii=False, indent=2)
    manual_overrides = [item for item in conflicts if item.get('resolution') == 'manuals']
    if manual_overrides:
        print(f'Manuals override reviewed CFPA entries: {len(manual_overrides)}')

    quest = quest_files()
    extras = extra_instance_files()

    language_keys = sum(
        len(json.loads(outputs[m][0])) for m in outputs
        if m.startswith('assets/') and m.endswith('/lang/zh_cn.json')
    )
    group_labels = sum(
        len(json.loads(outputs[m][0])) for m in outputs
        if m.startswith('assets/') and '/group_lang/zh_cn.json' in m
    )
    manual_members = [m for m in outputs if any(x in m.split('/')[2:3] for x in ('guides', 'guideme_guides', 'patchouli_books', 'ae2guide', 'ftbic', 'nodeworksguide'))]
    counts = [
        ('语言键', language_keys),
        ('分组名称', group_labels),
        ('手册/书籍文件', len(manual_members)),
        ('任务书文件', len(quest)),
        ('整合包数据文件', sum(1 for k in extras if k.startswith('datapacks/'))),
        ('运行时脚本', sum(1 for k in extras if k.startswith('kubejs/'))),
    ]
    outputs['pack.mcmeta'] = (encode({'pack': {
        'description': f'FTB Evolution 2 {VERSION} 简体中文汉化：语言覆盖、任务书、手册与整合包自定义文案',
        'min_format': 84, 'max_format': 97}}), 'packer')
    outputs['ATTRIBUTION.md'] = (attribution(notices, namespaces, counts), 'packer')
    outputs['ATTRIBUTION-CFPA.md'] = (notices['ATTRIBUTION.md'].read_bytes(), 'cfpa_review')
    outputs['CFPA-LICENSE.txt'] = (notices['CFPA-LICENSE.txt'].read_bytes(), 'cfpa_review')
    outputs['licenses/ANIMAL-PEN-LICENSE.txt'] = (notices['licenses/ANIMAL-PEN-LICENSE.txt'].read_bytes(), 'cfpa_review')

    install_members = {}
    for member, (data, _origin) in outputs.items():
        install_members[member] = data
    for rel, path in quest.items():
        install_members[rel] = path.read_bytes()
    for rel, path in extras.items():
        install_members[rel] = path.read_bytes()
    install_members['INSTALL.md'] = install_guide().encode()
    return outputs, quest, extras, install_members, counts


def install_guide():
    return '\n'.join([
        '# FTB Evolution 2 简体中文汉化包安装说明',
        '',
        f'版本 {VERSION} / Minecraft 26.1.2。解压后把下面的内容按同名路径放到游戏实例目录。',
        '',
        '```',
        '<实例目录>/',
        f'  resourcepacks/{PACK_NAME}.zip      <- 资源包，语言覆盖 / 手册 / 已审校 CFPA 条目',
        '  config/ftbquests/quests/lang/zh_cn/ <- 任务书翻译（FTB Quests 从 config 读取）',
        '  datapacks/ftb/...                   <- 整合包对话框与游商定义',
        '  kubejs/server_scripts/...           <- 商店/事件运行时消息脚本',
        '```',
        '',
        '步骤：',
        '',
        '1. 关闭游戏。',
        '2. 备份上面提到的同名文件（覆盖前先另存一份）。',
        f'3. 把本包内容复制到实例目录；资源包 ZIP 直接放入 `resourcepacks/`。',
        '4. 启动游戏，在 选项 → 资源包 里把 `FTB-Evolution-2-' + VERSION + '-zh_CN` 移到最上方。',
        '5. 语言设为 简体中文，重载资源或重启客户端。',
        '',
        '注意：任务书翻译依赖 STEP 3 的 config 目录，资源包无法覆盖它。',
        '本包未在实际游戏会话中测试；出现英文回退说明该条目尚未翻译。',
        '',
    ])


# --------------------------------------------------------------------------- #
# ZIP helpers
# --------------------------------------------------------------------------- #
def write_zip(path, members):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for rel in sorted(members):
            entry = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, members[rel])
    payload = buffer.getvalue()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    path.with_suffix('.zip.sha256').write_text(digest(payload) + '  ' + path.name + '\n')
    return payload


def build(command):
    outputs, quest, extras, install_members, counts = compile_release()
    members = {rel: data for rel, (data, _o) in outputs.items()}
    if command == 'plan':
        print(json.dumps({'counts': counts, 'resourcepack_members': len(members),
                          'quest_files': len(quest), 'instance_files': len(extras)},
                         ensure_ascii=False, indent=2))
        return
    write_zip(RESOURCEPACK, members)
    write_zip(INSTALL_ZIP, install_members)
    manifest = {
        'target_pack_version': VERSION,
        'mc_version': '26.1.2',
        'counts': counts,
        'resourcepack': {'file': RESOURCEPACK.name, 'members': {k: digest(v) for k, v in sorted(members.items())}},
        'install_bundle': {'file': INSTALL_ZIP.name, 'members': {k: digest(v) for k, v in sorted(install_members.items())}},
        'in_game_tested': False,
        'installed_to_game': False,
    }
    RELEASE_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'built', 'resourcepack': str(RESOURCEPACK), 'install_bundle': str(INSTALL_ZIP),
                      'counts': counts}, ensure_ascii=False, indent=2))


def check(*, include_installed=True):
    manifest = json.loads(RELEASE_MANIFEST.read_text())
    outputs, quest, extras, install_members, counts = compile_release()
    members = {rel: data for rel, (data, _o) in outputs.items()}
    assert sorted(members) == sorted(manifest['resourcepack']['members']), 'Resource pack member list differs'
    for rel, data in members.items():
        assert digest(data) == manifest['resourcepack']['members'][rel], f'Content differs: {rel}'
    assert sorted(install_members) == sorted(manifest['install_bundle']['members']), 'Install bundle differs'
    for rel, data in install_members.items():
        assert digest(data) == manifest['install_bundle']['members'][rel], f'Bundle content differs: {rel}'
    for path, table in ((RESOURCEPACK, manifest['resourcepack']['members']),
                        (INSTALL_ZIP, manifest['install_bundle']['members'])):
        with zipfile.ZipFile(path) as archive:
            assert sorted(archive.namelist()) == sorted(table), f'Archive members differ: {path.name}'
            assert archive.testzip() is None, f'Archive corrupt: {path.name}'
        assert digest(path.read_bytes()) == hashlib.sha256(path.read_bytes()).hexdigest()
    record = json.loads(INSTALL_RECORD.read_text()) if include_installed and INSTALL_RECORD.exists() else None
    if record:
        game = pathlib.Path(record['instance'])
        for rel, sha in record['files'].items():
            target = game / rel
            assert target.is_file(), f'Installed file missing: {rel}'
            assert digest(target.read_bytes()) == sha, f'Installed file changed: {rel}'
    print(json.dumps({'status': 'passed', 'counts': counts,
                      'resourcepack_members': len(members), 'bundle_members': len(install_members),
                      'installation_verified': bool(record)}, ensure_ascii=False, indent=2))


# --------------------------------------------------------------------------- #
# Install
# --------------------------------------------------------------------------- #
def install(enable):
    manifest = json.loads(RELEASE_MANIFEST.read_text())
    game = instance_dir()

    # Every file this command writes, resolved up front from the verified bundle.
    plan = {}
    with zipfile.ZipFile(INSTALL_ZIP) as archive:
        assert digest(INSTALL_ZIP.read_bytes()) == INSTALL_ZIP.with_suffix('.zip.sha256').read_text().split()[0]
        for rel in sorted(manifest['install_bundle']['members']):
            data = archive.read(rel)
            assert digest(data) == manifest['install_bundle']['members'][rel], f'Bundle drifted: {rel}'
            if rel in ('INSTALL.md', 'pack.mcmeta', 'ATTRIBUTION.md') or rel.startswith('assets/'):
                continue  # these live inside the resource pack archive instead
            plan[rel] = data
    resourcepack = RESOURCEPACK.read_bytes()
    expected = RESOURCEPACK.with_suffix('.zip.sha256').read_text().split()[0]
    assert digest(resourcepack) == expected, 'Resource pack archive changed'
    plan[f'resourcepacks/{PACK_NAME}.zip'] = resourcepack

    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = game / f'.cn-backup-{stamp}'
    backed_up = []
    for rel in sorted(plan):
        if rel.endswith('INSTALL.md'):
            continue
        target = game / rel
        if target.exists():
            shadow = backup / rel
            shadow.parent.mkdir(parents=True, exist_ok=True)
            shadow.write_bytes(target.read_bytes())
            backed_up.append(rel)
    written = []
    for rel in sorted(plan):
        if rel.endswith('INSTALL.md'):
            continue
        target = game / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(plan[rel])
        written.append(rel)

    options = None
    if enable:
        options = enable_resource_pack(game, backup)

    record = {'timestamp': stamp, 'instance': str(game), 'backup': str(backup),
              'files': {rel: digest(plan[rel]) for rel in sorted(plan) if not rel.endswith('INSTALL.md')},
              'backup_files': sorted(backed_up), 'resource_pack_enabled': bool(enable),
              'in_game_tested': False}
    INSTALL_RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    if backup.exists():
        (backup / 'INSTALLATION.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'installed', 'instance': str(game), 'written': len(written),
                      'backed_up': len(backed_up), 'backup_dir': str(backup) if backed_up else None,
                      'resource_pack_enabled': bool(options)}, ensure_ascii=False, indent=2))


def enable_resource_pack(game, backup):
    options = game / 'options.txt'
    assert options.is_file(), str(options)
    original = options.read_text()
    entry = f'file/{PACK_NAME}.zip'
    lines = original.splitlines()
    for index, line in enumerate(lines):
        if line.startswith('resourcePacks:'):
            packs = json.loads(line.split(':', 1)[1])
            # `resourcePacks` is ordered lowest priority first: vanilla is always the
            # first entry and the project's own manual pack was intentionally put
            # last for highest priority. Appending is what actually overrides mods.
            if entry in packs:
                packs.remove(entry)
            packs.append(entry)
            lines[index] = 'resourcePacks:' + json.dumps(packs, ensure_ascii=False)
            break
    else:
        raise ValueError('resourcePacks line not found in options.txt')
    shadow = backup / 'options.txt'
    shadow.parent.mkdir(parents=True, exist_ok=True)
    shadow.write_text(original)
    options.write_text('\n'.join(lines) + '\n')
    return entry


def revert():
    record = json.loads(INSTALL_RECORD.read_text())
    game = pathlib.Path(record['instance'])
    backup = pathlib.Path(record['backup'])
    assert backup.is_dir(), str(backup)
    restored = []
    for rel in sorted(record['backup_files']):
        target = game / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((backup / rel).read_bytes())
        restored.append(rel)
    for rel in record['files']:
        if rel in record['backup_files']:
            continue
        target = game / rel
        if target.is_file():
            target.unlink()
    if record['resource_pack_enabled']:
        (backup / 'options.txt').replace(game / 'options.txt')
    INSTALL_RECORD.unlink()
    print(json.dumps({'status': 'reverted', 'restored': len(restored),
                      'backup_dir': str(backup)}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'build', 'check', 'install', 'revert'])
    parser.add_argument('--enable', action='store_true',
                        help='Write the pack to options.txt so it is enabled automatically')
    args = parser.parse_args()
    if args.command == 'install':
        install(args.enable)
    elif args.command == 'revert':
        revert()
    elif args.command == 'check':
        check()
    else:
        build(args.command)


if __name__ == '__main__':
    main()
