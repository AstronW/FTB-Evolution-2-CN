"""Build and verify KubeJS custom language overlays, preserving existing translations."""
from protected_text import assert_protected
import collections, hashlib, json, pathlib, re, sys
from punctuation import normalize, assert_ascii
ROOT=pathlib.Path(__file__).resolve().parent.parent
WORK=ROOT/'localization/custom'
MC=ROOT/'.minecraft'
def read(p):return json.loads(p.read_text()) if p.exists() else {}
def norm(s):return re.sub(r'[+-]?\d+(?:\.\d+)?', '{}',s)
def mappings():
 out={}
 for p in sorted(WORK.glob('*.tsv')):
  for line in p.read_text().splitlines():
   if not line or line.startswith('#'):continue
   en,zh=line.split('\t',1)
   if en in out and out[en]!=zh:raise ValueError('Conflicting translation: '+en)
   out[en]=zh
 return out

def main():
 mapping=mappings(); terms=read(ROOT/'localization/terms.json')
 baseline={r['namespace']:r['sha256'] for r in read(WORK/'initial-build.json').get('namespaces',[])}
 adaptation=read(ROOT / read(ROOT/'project.json')['custom_adaptation']['source_bindings'])
 approved={};deferred={}
 if adaptation:
  game=pathlib.Path(read(ROOT/'project.json')['target_instance'])
  for ns,row in adaptation['sources'].items():
   assert hashlib.sha256((game/row['path']).read_bytes()).hexdigest()==row['sha256'], ('Target source changed',ns)
   baseline[ns]=row['sha256']
  assert {p.parent.parent.name for p in (MC/'kubejs/assets').glob('*/lang/en_us.json')}==set(adaptation['sources'])|{'ftb_custom'}, 'Custom source file set changed'
  for folder in sorted((WORK/'batches').glob('batch-*')):
   manifest=read(folder/'manifest.json')
   for entry in manifest.get('language_entries',[]):
    approved[entry['key']]=entry
  deferred={row['key']:row for row in adaptation['deferred_manual_keys']}
 missing=[]; outputs={}; records=[]
 for p in sorted((MC/'kubejs/assets').glob('*/lang/en_us.json')):
  ns=p.parent.parent.name; en=read(p); out=read(p.with_name('zh_cn.json')); before=dict(out)
  if ns in baseline and hashlib.sha256(p.read_bytes()).hexdigest()!=baseline[ns]:
   raise ValueError('English source changed; reconcile before rebuilding: '+str(p))
  for k,v in en.items():
   if k in deferred:
    assert v==deferred[k]['en'], ('Deferred manual source changed',k)
    continue
   if k in approved:
    assert v==approved[k]['en'] and p.with_name('zh_cn.json')==ROOT/approved[k]['output_path'], ('Approved source mismatch',k)
    out[k]=approved[k]['zh']
   if k in out:continue
   translated=mapping.get(v,terms.get(v))
   if translated is None and norm(v) in mapping:
    nums=iter(re.findall(r'[+-]?\d+(?:\.\d+)?',v)); translated=re.sub(r'\{\}',lambda m:next(nums),mapping[norm(v)])
   if translated is None:
    missing.append((ns,k,v));continue
   out[k]=normalize(translated)
  outputs[p.with_name('zh_cn.json')]=out
  records.append(dict(namespace=ns,source_keys=len(en),existing_keys=len(before),added_keys=len(out)-len(before),missing=sum(n==ns for n,k,v in missing),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 pending={}
 for ns,k,v in missing:pending.setdefault(norm(v),[]).append(ns+':'+k)
 (WORK/'pending.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2)+'\n')
 print('Pending keys:',len(missing),'distinct templates:',len(pending))
 if not {'--build','--check'} & set(sys.argv):return
 if missing:raise ValueError('Incomplete translation; review custom/pending.json')
 issues=[]
 for p,out in outputs.items():
  en=read(p.with_name('en_us.json'))
  for k,v in en.items():
   if k in deferred:continue
   z=out[k];assert_ascii(z,k)
   assert_protected(v,z,k)
   for label,pattern in [('placeholders',r'%(?:\d+\$)?[sdif]|%%'),('formatting',r'§[0-9a-fk-or]'),('numbers',r'[+-]?\d+(?:\.\d+)?'),('commands',r'/[a-z][a-z0-9_:]*(?: toggle [a-z]+:[a-z]+)?')]:
    if collections.Counter(re.findall(pattern,v))!=collections.Counter(re.findall(pattern,z)):
     issues.append(dict(key=k,check=label,en=v,zh=z))
 if issues:
  (WORK/'issues.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2)+'\n');raise ValueError(f'{len(issues)} verification issues')
 if '--build' in sys.argv:
  for p,out in outputs.items():p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 # Check mode also verifies that every generated key is actually installed.
 if '--check' in sys.argv:
  for p,out in outputs.items():
   if read(p)!=out:raise ValueError('Installed overlay differs: '+str(p))
 initial=read(WORK/'initial-build.json')
 (WORK/'verification.json').write_text(json.dumps(dict(status='passed',namespaces=records,total_source_keys=sum(r['source_keys'] for r in records),verified_scope_keys=sum(r['source_keys'] for r in records)-len(deferred),deferred_manual_keys=list(deferred),initial_added_keys=initial.get('added_keys'),in_game_tested=False),ensure_ascii=False,indent=2)+'\n')
 print('Validated',sum(r['source_keys'] for r in records)-len(deferred),'keys; deferred handbook keys:',len(deferred))
if __name__=='__main__':main()
