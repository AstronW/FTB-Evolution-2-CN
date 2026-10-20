"""Verify the audited 1.3.2 batch carry-forward against current 1.4.0 inputs."""
import hashlib
import json
from pathlib import Path
import zipfile

from ordinary_translation import process

ROOT = Path(__file__).resolve().parent.parent


def read(path):
    return json.loads(path.read_text())


def verify_historical_1_4_0():
    report = read(ROOT / 'localization/reports/ordinary-1.4.0-rebind.json')
    revisions=read(ROOT/'localization/ordinary/reviewed-revisions.json')
    used=set()
    for row in report['batches']:
        folder = ROOT / 'localization/ordinary' / ('batch-' + row['batch'])
        archive = ROOT / row['archive']
        old_manifest = read(archive / 'manifest.json')
        old = read(archive / 'source-en_us.json')
        manifest = read(folder / 'manifest.json')
        jar = ROOT / manifest['jar']
        assert manifest['jar'] == row['current_jar']
        assert hashlib.sha256(jar.read_bytes()).hexdigest() == row['jar_sha256']
        with zipfile.ZipFile(jar) as source:
            raw = source.read(manifest['language_path'])
        assert hashlib.sha256(raw).hexdigest() == row['language_sha256']
        current = json.loads(raw)
        selected = {key: value for key, value in current.items() if key in old}
        assert selected == read(folder / 'source-en_us.json')
        assert set(manifest.get('include_keys', selected)) == set(selected)
        changes = {key: {'old': old[key], 'new': value}
                   for key, value in selected.items() if value != old[key]}
        assert changes == row['reviewed_changes']
        pending = ({key: value for key, value in current.items() if key not in old}
                   if 'include_keys' not in old_manifest else {})
        assert pending == row['pending_added_keys']
        missing = set(old) - set(current)
        assert missing == set(row['compatibility_only_keys'])
        values = read(archive / 'source-values.json')
        translations = {}
        for line in (archive / 'zh-values.tsv').read_text().splitlines():
            index, value = line.split('\t', 1)
            translations[values[int(index)]] = value.replace('\\n', '\n')
        overlay = read(ROOT / manifest['target'])
        for key, source in old.items():
            expected = old_manifest['context_overrides'].get(key, translations[source])
            if key in changes:
                assert source.rstrip(' ') == current[key]
                expected = expected.rstrip(' ')
            for index,revision in enumerate(revisions):
                if revision['batch']==row['batch'] and revision['key']==key:
                    assert revision['source']==source and revision['previous']==expected and revision['reason']
                    expected=revision['translation'];used.add(index)
            assert overlay[key] == expected, (row['batch'], key, 'translation changed')
            if key in missing:
                assert row['compatibility_only_keys'][key] == {
                    'source': source, 'translation': expected}
        process(folder, False)
    assert used==set(range(len(revisions))), 'Unused reviewed revisions'
    print('PASS: ten rebound batches, source deltas, pending additions and preserved translations')


def main():
    if read(ROOT / 'project.json')['target_pack_version'] == '1.4.0':
        return verify_historical_1_4_0()
    report = read(ROOT / 'localization/updates/1.4.1/ordinary-rebind.json')
    revisions = read(ROOT / 'localization/ordinary/overlay-revisions.json')
    from ordinary_translation import language_source
    verified = 0
    for row in report['batches']:
        if row['state'] == 'retired_mod':
            assert row['reason'] and (ROOT / row['archive'] / 'manifest.json').is_file()
            assert not (ROOT / row['old_jar']).exists()
            continue
        folder = ROOT / 'localization/ordinary' / row['batch']
        before = ROOT / row['before']
        old_manifest = read(before / 'manifest.json')
        old = read(before / 'source-en_us.json')
        manifest = read(folder / 'manifest.json')
        assert manifest['jar'] == row['jar']
        assert hashlib.sha256((ROOT / manifest['jar']).read_bytes()).hexdigest() == row['jar_sha256']
        raw = language_source(manifest)
        assert hashlib.sha256(raw).hexdigest() == row['language_sha256']
        current = json.loads(raw)
        selected = {k: v for k, v in current.items() if k in old}
        assert selected == read(folder / 'source-en_us.json')
        assert set(manifest.get('include_keys', selected)) == set(selected)
        assert {k: {'old': old[k], 'new': v} for k, v in selected.items() if old[k] != v} == row['source_changes']
        assert set(old) - set(current) == set(row['removed_compatibility_keys'])
        values = read(before / 'source-values.json')
        translated = {}
        for line in (before / 'zh-values.tsv').read_text().splitlines():
            index, value = line.split('\t', 1)
            translated[values[int(index)]] = value.replace('\\n', '\n')
        overlay = read(ROOT / manifest['target'])
        for key, source in old.items():
            expected = old_manifest['context_overrides'].get(key, translated[source])
            if key in row['source_changes']:
                matches = [r for r in revisions if r['namespace'] == manifest['namespace']
                           and r['key'] == key and r['previous'] == expected
                           and r['source'] == current[key] and r['reason']]
                assert len(matches) == 1, (row['batch'], key, 'missing reviewed source adaptation')
                expected = matches[0]['translation']
            assert overlay[key] == expected, (row['batch'], key, 'translation carry-forward changed')
        process(folder, False)
        verified += 1
    print(f'PASS: {verified} current batches, exact source deltas and preserved translations')


if __name__ == '__main__':
    main()
