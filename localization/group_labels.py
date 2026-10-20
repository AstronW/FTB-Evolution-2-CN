"""Build/check the Collapsible Groups group_lang overlay.

group_lang is a separate resource file from the mod's normal lang file, so the
labels live in their own overlay instead of the ordinary batch output.
"""
import json, pathlib, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANS = ROOT / 'localization/manuals/group_lang-zh.json'
OVERLAY = ROOT / '.minecraft/kubejs/assets/collapsible_groups/group_lang/zh_cn.json'
JAR_GLOB = '*collapsible*'


def source():
    jar = next((ROOT / '.minecraft/mods').glob(JAR_GLOB))
    with zipfile.ZipFile(jar) as z:
        return json.loads(z.read('assets/collapsible_groups/group_lang/en_us.json'))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    en = source()
    zh = json.loads(TRANS.read_text())
    unknown = sorted(set(zh) - set(en))
    assert not unknown, ('unknown group label keys', unknown[:5])
    assert all(zh[k] != en[k] for k in zh), 'translation equals source'
    text = json.dumps(dict(sorted(zh.items())), ensure_ascii=False, indent=2) + '\n'
    if cmd == 'build':
        OVERLAY.parent.mkdir(parents=True, exist_ok=True)
        OVERLAY.write_text(text)
        print(f'wrote {len(zh)} group labels to {OVERLAY.relative_to(ROOT)}')
    else:
        assert OVERLAY.read_text() == text, 'group_lang overlay drifted from translations'
        print(f'group_lang overlay matches {len(zh)} labels; {len(en) - len(zh)} labels left untranslated')


if __name__ == '__main__':
    main()
