"""Build per-mod English/Chinese name glossaries for the remaining manuals.

The glossary is a translation aid, not a replacement dictionary: it contains
only names that already exist in the current JAR, the project ordinary overlay
or the reviewed CFPA overlay.  It never invents a translation.
"""
from __future__ import annotations

import json
import pathlib
import re
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
MC = ROOT / '.minecraft'
BASE = ROOT / 'localization/manuals_extra'
PACKS = [
    MC / 'resourcepacks/FTB-Evolution-2-CFPA-Reviewed-zh_CN',
    MC / 'resourcepacks/FTB-Evolution-2-Manuals-zh_CN',
]
NAME_KEYS = re.compile(
    r'^(item|block|entity|fluid_type|effect|itemGroup|gui|jei|config|advancement|bacteria|'
    r'subtitles|death|biome|dimension|trim_material|enchantment|mob_effect)\.'
)


def read_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def jar_lang(namespace: str, language: str) -> dict:
    values = {}
    for jar in sorted((MC / 'mods').glob('*.jar')):
        try:
            with zipfile.ZipFile(jar) as archive:
                name = f'assets/{namespace}/lang/{language}.json'
                if name in archive.namelist():
                    # Later JARs win, matching the deterministic scan order used
                    # by the assessment, not a claim about runtime priority.
                    values.update(json.loads(archive.read(name)))
        except Exception:
            continue
    return values


def overlay_lang(namespace: str, language: str = 'zh_cn') -> dict:
    values = {}
    path = MC / f'kubejs/assets/{namespace}/lang/{language}.json'
    if path.is_file():
        values.update(read_json(path))
    for pack in PACKS:
        path = pack / f'assets/{namespace}/lang/{language}.json'
        if path.is_file():
            values.update(read_json(path))
    return values


def main() -> None:
    manifest = json.loads((BASE / 'source_manifest.json').read_text())
    groups = sorted({entry['group'] for entry in manifest['documents'].values()})
    out_dir = BASE / 'glossaries'
    out_dir.mkdir(parents=True, exist_ok=True)
    for group in groups:
        en = jar_lang(group, 'en_us')
        zh = {}
        zh.update(jar_lang(group, 'zh_cn'))
        zh.update(overlay_lang(group))
        terms = {}
        for key, value in en.items():
            if not isinstance(value, str) or not value.strip():
                continue
            chinese = zh.get(key)
            if not isinstance(chinese, str) or not re.search(r'[\u3400-\u9fff]', chinese):
                continue
            if not NAME_KEYS.match(key) and 'item.' not in key and 'block.' not in key:
                continue
            terms[key] = {'en': value, 'zh': chinese}
        path = out_dir / f'{group}.json'
        path.write_text(json.dumps(terms, ensure_ascii=False, indent=2) + '\n')
        print(f'{group}: {len(terms)} name pairs -> {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
