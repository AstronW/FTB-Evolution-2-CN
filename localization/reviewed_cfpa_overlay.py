"""Read only a verified reviewed overlay; used by remaining-work inventories."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent.parent

def load_verified_review():
    base=ROOT/'localization/cfpa_review'
    proof=base/'verification.json';manifest=base/'build-manifest.json'
    if not proof.exists() or not manifest.exists():return [],[]
    read=lambda p:json.loads(p.read_text())
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    verification=read(proof)
    if verification.get('status')!='passed':return [],[]
    assert verification['build_manifest_sha256']==sha(manifest),'Reviewed overlay verification is stale; rebuild and check first'
    inputs=read(manifest)
    for name,expected in inputs['reviewed_decisions_sha256'].items():assert sha(base/'decisions'/name)==expected,('Reviewed decisions changed',name)
    pack=ROOT/'.minecraft/resourcepacks/FTB-Evolution-2-CFPA-Reviewed-zh_CN'
    for rel,expected in inputs['files'].items():assert sha(pack/rel)==expected,('Reviewed resource changed',rel)
    language=[]
    for name in inputs['reviewed_decisions_sha256']:
        if name!='manuals.json':language.extend(read(base/'decisions'/name))
    return language,read(base/'decisions/manuals.json')
