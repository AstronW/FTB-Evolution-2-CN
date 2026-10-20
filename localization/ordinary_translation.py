"""Build and check ordinary-language translation batches against installed JARs."""
from protected_text import assert_protected
import collections
import hashlib
import io
import json
import pathlib
import re
import sys
import zipfile
from punctuation import assert_ascii
ROOT=pathlib.Path(__file__).resolve().parent.parent
WORK=ROOT/'localization/ordinary'
def read(p):return json.loads(p.read_text())
def check_scope(ns, manifest=None):
 scope=read(ROOT/'localization/language_scope.json')
 if ns in scope['excluded_namespaces'] and manifest and manifest.get('preserved_scope'):
  preserved=manifest['preserved_scope']
  previous=read(ROOT/preserved['source_snapshot'])
  assert preserved['reason'] and set(manifest['include_keys'])==set(previous), 'Excluded mod scope expanded'
  return
 assert ns not in scope['excluded_namespaces'], ns
 assert not any(ns.startswith(p) for p in scope['excluded_namespace_prefixes']), ns

def language_source(manifest):
 path=ROOT/manifest['jar']
 container=manifest.get('source_container')
 if container:
  parent=ROOT/container['jar']
  assert hashlib.sha256(parent.read_bytes()).hexdigest()==container['jar_sha256'], 'Source container changed'
  with zipfile.ZipFile(parent) as z:embedded=z.read(container['member'])
  assert hashlib.sha256(embedded).hexdigest()==container['member_sha256'], 'Embedded dependency changed'
  assert embedded==path.read_bytes(), 'Extracted dependency differs from current container'
 if 'nested_jars' in manifest:
  raw=path.read_bytes()
  assert hashlib.sha256(raw).hexdigest()==manifest['jar_sha256'], 'Outer JAR changed'
  for layer in manifest['nested_jars']:
   with zipfile.ZipFile(io.BytesIO(raw)) as z:raw=z.read(layer['path'])
   assert hashlib.sha256(raw).hexdigest()==layer['sha256'], 'Nested JAR changed'
  with zipfile.ZipFile(io.BytesIO(raw)) as z:return z.read(manifest['language_path'])
 if 'nested_jar' not in manifest:
  with zipfile.ZipFile(path) as z:return z.read(manifest['language_path'])
 # Some current distributions put their entire mod, including all language
 # resources, in a jar-in-jar. Bind both layers instead of extracting an
 # untracked copy or silently skipping the namespace.
 assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest['jar_sha256'],'Outer JAR changed'
 with zipfile.ZipFile(path) as z:nested=z.read(manifest['nested_jar'])
 assert hashlib.sha256(nested).hexdigest()==manifest['nested_jar_sha256'],'Nested JAR changed'
 with zipfile.ZipFile(io.BytesIO(nested)) as z:return z.read(manifest['language_path'])

def process(folder,build):
 manifest=read(folder/'manifest.json');check_scope(manifest['namespace'], manifest)
 raw=language_source(manifest);en=json.loads(raw)
 if 'include_keys' in manifest:
  selected=set(manifest['include_keys'])
  assert selected <= en.keys(), 'Selected keys missing from JAR'
  en={key:value for key,value in en.items() if key in selected}
 assert en==read(folder/'source-en_us.json'), 'English source changed'
 values=read(folder/'source-values.json')
 assert values==list(dict.fromkeys(en.values())), 'Value indexes changed'
 translated={}
 for line in (folder/'zh-values.tsv').read_text().splitlines():
  i,value=line.split('\t',1);i=int(i)
  assert i not in translated, ('duplicate',i)
  translated[i]=value.replace('\\n','\n')
 assert set(translated)==set(range(len(values))), 'Incomplete value coverage'
 mapping={value:translated[i] for i,value in enumerate(values)}
 output={key:manifest['context_overrides'].get(key,mapping[value]) for key,value in en.items()}
 for key,value in en.items():
  zh=output[key];assert_ascii(zh,key)
  assert_protected(value,zh,key)
  for literal in manifest.get('protected_literals',[]):
   assert value.count(literal)==zh.count(literal),(key,'protected literal',literal)
  for label,pattern in [('placeholders',r'%(?:\d+\$)?[sdif]|%%'),('numbers',r'(?<![A-Za-z])[+-]?\d+(?:\.\d+)?'),('formatting',r'§[0-9a-fk-or]'),('rich_text',r'</?sc[a-z]+>'),('units',r'\b(?:RF/t|mB/t|mB/s|RF/mB|AP/t|FE/t|RF|FE|AP|mB)\b'),('diagrams',r'[■□]+')]:
   before,after=re.findall(pattern,value),re.findall(pattern,zh)
   assert (collections.Counter(before)==collections.Counter(after) if label=='units' else before==after),(key,label,value,zh)
  assert value.count('\n')==zh.count('\n'),(key,'line breaks')
  # Split labels/values are joined by the UI; retain their boundary spaces.
  assert (value.startswith(' '),value.endswith(' '))==(zh.startswith(' '),zh.endswith(' ')),(key,'boundary spaces')
  if not re.search('[\u3400-\u9fff]',zh):
   assert value in manifest['unchanged_values'],(key,'unreviewed unchanged text',zh)
 path=ROOT/manifest['target']
 original=read(path) if path.exists() else {}
 backup=folder/'overlay-before.json'
 if build and not backup.exists():backup.write_text(json.dumps(original,ensure_ascii=False,indent=2)+'\n')
 merged={**original,**output}
 if build:
  path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n')
 else:
  assert original==merged, 'Installed output differs'
 if backup.exists():
  for key,value in read(backup).items():
   if key not in en and merged[key]!=value:
    # A later review can intentionally repair a shared overlay. Keep immutable
    # before-snapshots and require an exact source/old/new/reason record instead.
    revisions=read(WORK/'overlay-revisions.json')
    matches=[row for row in revisions if row['namespace']==manifest['namespace'] and row['key']==key and row['previous']==value and row['translation']==merged[key]]
    assert len(matches)==1,('Existing custom translation changed',key)
    revision=matches[0];owner=read(WORK/revision['batch']/'manifest.json')
    assert revision['reason'] and owner['namespace']==manifest['namespace'] and owner['target']==manifest['target']
    with zipfile.ZipFile(ROOT/owner['jar']) as archive:
     owner_source=json.loads(archive.read(owner['language_path']))
    assert owner_source[key]==revision['source'],('Reviewed correction source changed',key)
    assert_protected(revision['source'],merged[key],key)
 report=dict(status='passed',batch=manifest['batch'],namespace=manifest['namespace'],source_keys=len(en),unique_values=len(values),chinese_values=sum(bool(re.search('[\u3400-\u9fff]',v)) for v in output.values()),reviewed_non_prose_values=sum(not bool(re.search('[\u3400-\u9fff]',v)) for v in output.values()),installed_overlay_keys=len(merged),source_sha256=hashlib.sha256(raw).hexdigest(),in_game_tested=False)
 (folder/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report
if __name__=='__main__':
 folders=[WORK/sys.argv[1]] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else sorted(WORK.glob('batch-*'))
 for folder in folders:print(json.dumps(process(folder,'--build' in sys.argv),ensure_ascii=False))
