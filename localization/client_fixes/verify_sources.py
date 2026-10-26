"""Check source bindings for the narrow client compatibility overlay."""
import hashlib
import json
import pathlib
import tomllib
import zipfile
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from punctuation import normalize, assert_ascii
from build_mod_names import render
from source_archive import find_mod, read_resource
ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / 'localization/client_fixes'
read = lambda p: json.loads(p.read_text())
names = read(BASE / 'mod-names.json')
assert (BASE / 'mod_names.js').read_text() == render(names), 'Generated name bridge differs'
audit = read(BASE / 'mod-name-audit.json')
for row in audit['rows']:
    if row['status'] == 'enabled':
        assert names[row['id']]['translation'] == row['translation'], row['id']
for mod_id, row in names.items():
    assert_ascii(row['translation'], mod_id)
    jar = find_mod(mod_id)
    with zipfile.ZipFile(jar) as archive:
        metadata = tomllib.loads(archive.read('META-INF/neoforge.mods.toml').decode())
    assert any(m['modId'] == mod_id and m['displayName'] == row['english'] for m in metadata['mods']), mod_id
    if row.get('user_decision'):
        assert read(BASE / row['user_decision'])['names'][mod_id] == row['translation'], mod_id
    evidence = row.get('source_evidence')
    if evidence:
        with zipfile.ZipFile(jar) as archive:
            if evidence['kind'] == 'native':
                source = json.loads(archive.read(evidence['path']))
                english = json.loads(archive.read(evidence['path'].replace('zh_cn.json', 'en_us.json')))
                assert ''.join(c.lower() for c in english[evidence['key']] if c.isascii() and c.isalnum()) == ''.join(c.lower() for c in row['english'] if c.isascii() and c.isalnum()), mod_id
            else:
                source = read(ROOT / evidence['path'])
        assert source[evidence['key']] == evidence['chinese'], mod_id
        assert normalize(evidence['chinese']) == row['translation'], mod_id
manifest = read(BASE / 'manifest.json')
for script in manifest['scripts']:
    assert hashlib.sha256((BASE / script['file']).read_bytes()).hexdigest() == script['sha256']
for source in manifest['runtime_sources']:
    read_resource(source['class'], ROOT / source['jar'], source['sha256'])
print('PASS: current mod IDs, display names, JARs, runtime API classes and script hashes')
