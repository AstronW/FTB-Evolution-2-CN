"""Download pinned official CFPA release ZIPs, without requiring an updater mod.

This only vendors verified source archives. Integration and coverage auditing are
separate steps; it does not install or activate an unreviewed combined pack.
"""
from pathlib import Path
import hashlib
import json
import os
import urllib.request
import zipfile

BASE = Path(__file__).resolve().parent / 'vendor/cfpa'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = BASE / 'sources.json'
    sources = json.loads(manifest.read_text())
    for asset in sources['assets']:
        target = BASE / asset['filename']
        if target.exists():
            if digest(target) != asset['sha256']:
                raise ValueError(f'Existing archive has unexpected SHA-256: {target}')
            print(f'Verified cached archive: {target.name}')
            continue
        partial = target.with_suffix('.zip.part')
        request = urllib.request.Request(asset['url'], headers={'User-Agent': 'FTB-Evolution-2-localization'})
        try:
            with urllib.request.urlopen(request, timeout=60) as response, partial.open('wb') as out:
                while chunk := response.read(1024 * 1024):
                    out.write(chunk)
            if digest(partial) != asset['sha256']:
                raise ValueError(f'Download SHA-256 mismatch: {target.name}')
            with zipfile.ZipFile(partial) as archive:
                bad = archive.testzip()
                if bad is not None:
                    raise ValueError(f'ZIP CRC mismatch: {bad}')
                if 'pack.mcmeta' not in archive.namelist():
                    raise ValueError(f'Missing resource pack metadata: {target.name}')
            os.replace(partial, target)
        finally:
            partial.unlink(missing_ok=True)
        print(f'Downloaded and verified: {target.name}')
    sources['status'] = 'downloaded_verified_not_integrated'
    sources.pop('download_blocker', None)
    manifest.write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n')
    print('Source archives ready. Integration and coverage review are still required.')

if __name__ == '__main__':
    main()
