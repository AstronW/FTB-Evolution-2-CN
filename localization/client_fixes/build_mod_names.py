"""Generate the client name bridge from reviewed, current-instance mappings."""
import hashlib
import json
import pathlib
import sys
BASE = pathlib.Path(__file__).resolve().parent

def render(names):
    return ('// Current-instance mod IDs and decisions: localization/client_fixes/mod-names.json\n'
            '// KubeJS ModInfo.setName updates metadata and its mod-name integration.\n'
            'const ftbCnModNames = ' + json.dumps({k: v['translation'] for k, v in names.items()}, ensure_ascii=False, indent=2) + '\n'
            'Object.keys(ftbCnModNames).forEach(id => {\n'
            '    if (Platform.isLoaded(id)) Platform.getInfo(id).setName(ftbCnModNames[id])\n'
            '})\n')

def main():
    names = json.loads((BASE / 'mod-names.json').read_text())
    output = render(names)
    path = BASE / 'mod_names.js'
    if sys.argv[1:] == ['--check']:
        assert path.read_text() == output, 'Name bridge differs from reviewed mapping; rebuild required'
    else:
        path.write_text(output)
        manifest_path = BASE / 'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        for script in manifest['scripts']:
            if script['file'] == path.name:
                script['sha256'] = hashlib.sha256(output.encode()).hexdigest()
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'PASS: {len(names)} reviewed mod names match the generated client bridge')

if __name__ == '__main__':
    main()
