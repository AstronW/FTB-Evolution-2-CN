"""Build/check reviewed pack-specific batches against pinned current sources."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import subprocess
import sys
from punctuation import assert_ascii

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'localization/custom/batches'

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(en, zh, label):
    assert_ascii(zh, label)
    for pattern in [r'%(?:\d+\$)?[sdif]|%%', r'§[0-9a-fk-or]', r'[+-]?\d+(?:\.\d+)?', r'https?://[^\s]+']:
        assert collections.Counter(re.findall(pattern, en)) == collections.Counter(re.findall(pattern, zh)), (label, en, zh)
    assert en.count('\n') == zh.count('\n'), label

def process(folder, build=False):
    manifest = read(folder / 'manifest.json')
    config = read(ROOT / 'project.json')
    game = Path(config['target_instance'])
    work = ROOT / config['worktree']
    instance = read(game / 'instance.json')
    assert instance['version'] == manifest['target_pack_version'] == config['target_pack_version']
    changes = 0
    # Source identity is pinned by the batch snapshots, not by the live instance:
    # an installed translation (or a pack-side reformat) rewrites the instance copy
    # while the reviewed English text stays what the batch was approved against.
    for row in manifest['files']:
        snapshot = folder / row['snapshot']
        assert sha(snapshot) == row['sha256'], row['source_path']
        original = read(snapshot)
        expected = copy.deepcopy(original)
        for change in row.get('changes', []):
            node = expected
            for part in change['path'][:-1]:
                node = node[part]
            leaf = change['path'][-1]
            assert node[leaf] == change['en'], change
            validate(change['en'], change['zh'], change['path'])
            node[leaf] = change['zh']
            changes += 1
        if row.get('output_path'):
            output = ROOT / row['output_path']
            assert output.is_relative_to(ROOT / config['worktree'])
            assert not output.is_symlink()
            if build:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + '\n')
            assert read(output) == expected, ('Output differs beyond approved text leaves', output)
    for entry in manifest.get('language_entries', []):
        en = read(work / entry['source_path'])[entry['key']]
        assert en == entry['en'], entry['key']
        validate(en, entry['zh'], entry['key'])
        output = ROOT / entry['output_path']
        if build:
            data = read(output) if output.exists() else {}
            data[entry['key']] = entry['zh']
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        assert read(output)[entry['key']] == entry['zh'], entry['key']
    for entry in manifest.get('reused_language', []):
        assert read(work / entry['source_path'])[entry['key']] == entry['en'], entry['key']
        assert read(ROOT / entry['output_path'])[entry['key']] == entry['zh'], entry['key']
        validate(entry['en'], entry['zh'], entry['key'])
    for row in manifest.get('scripts', []):
        assert sha(folder / row['snapshot']) == row['source_sha256'], row['snapshot']
        assert sha(ROOT / row['output_path']) == row['output_sha256'], row['output_path']
        subprocess.run(['node', '--check', str(ROOT / row['output_path'])], check=True, capture_output=True)
    synthetic = manifest.get('synthetic_language')
    if synthetic:
        en = read(ROOT / synthetic['source_path'])
        zh = read(ROOT / synthetic['output_path'])
        for key, entry in synthetic['entries'].items():
            assert en[key] == entry['en'] and zh[key] == entry['zh'], key
            validate(entry['en'], entry['zh'], key)
    report = {'status': 'passed', 'batch': folder.name, 'target_pack_version': instance['version'],
              'manifest_sha256': sha(folder / 'manifest.json'), 'source_files_verified': len(manifest['files']),
              'translated_json_fields': changes, 'translated_language_keys': len(manifest.get('language_entries', [])),
              'reused_language_keys': len(manifest.get('reused_language', [])), 'in_game_tested': False,
              'verified_scripts': len(manifest.get('scripts', [])),
              'installed_to_game': False}
    (folder / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    names = [a for a in sys.argv[1:] if not a.startswith('--')]
    folders = [BASE / names[0]] if names else sorted(BASE.glob('batch-*'))
    for folder in folders:
        process(folder, '--build' in sys.argv)
