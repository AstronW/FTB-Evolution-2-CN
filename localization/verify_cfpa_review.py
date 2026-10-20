"""Independent checks on the emitted reviewed overlay, including JSON structure."""
from pathlib import Path
import collections,json,hashlib,copy,re,zipfile
from assess_1_4_remaining import scan_instance,GAME
from cfpa_review_build import PACK,BASE,ARCHIVE,field_path,get,visible_fields,reviewed_exceptions,archive_content_digest
from cfpa_review_format import invariant_errors

ROOT=Path(__file__).resolve().parent.parent

def read(path):return json.loads(path.read_text())
def unique_object(pairs):
    out={}
    for key,value in pairs:
        assert key not in out,('Duplicate JSON key',key)
        out[key]=value
    return out

def main():
    manifest=read(BASE/'build-manifest.json')
    file_set={str(p.relative_to(PACK)) for p in PACK.rglob('*') if p.is_file()}
    assert file_set==set(manifest['files']),'Output file collection changed'
    with zipfile.ZipFile(ARCHIVE) as archive:
        members={rel:archive.read(rel) for rel in archive.namelist()}
        assert archive.testzip() is None,'Archive is corrupt'
    assert archive_content_digest(members)==manifest['archive_content_sha256'],'Archive contents changed'
    assert set(members)==set(manifest['files']),'Archive member collection differs'
    for rel,expected in manifest['files'].items():
        assert hashlib.sha256(members[rel]).hexdigest()==expected,('Archive member checksum changed',rel)
    global_keys={};parsed={}
    for rel,expected in manifest['files'].items():
        p=PACK/rel
        assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,('Output checksum changed',rel)
        if p.suffix=='.json':parsed[rel]=json.loads(p.read_text(),object_pairs_hook=unique_object)
        if re.fullmatch(r'assets/[^/]+/lang/zh_cn.json',rel):
            for key,value in parsed[rel].items():
                assert key not in global_keys,('Cross-namespace global key collision',key)
                global_keys[key]=(rel,value)
    _,_,resources,_=scan_instance(GAME,True)
    approved_fields=collections.defaultdict(dict)
    for d in read(BASE/'decisions/manuals.json'):
        if d['status']=='accepted' and d['format']=='Patchouli':approved_fields[d['path']][field_path(d['field'])]=d
    structural=[]
    for path,fields in approved_fields.items():
        source=json.loads(resources[path][0]);out=next(iter(fields.values()))['output_resource_path'];target=parsed[out]
        # Every non-visible JSON value, list order, component, recipe, action and
        # resource identifier must be inherited from the actual current source.
        def walk(a,b,loc=()):
            assert type(a)==type(b),('Patchouli value type',path,loc)
            if isinstance(a,dict):
                assert list(a)==list(b),('Patchouli keys/order',path,loc)
                for k,v in a.items():walk(v,b[k],loc+(k,))
            elif isinstance(a,list):
                assert len(a)==len(b),('Patchouli list size',path,loc)
                for i,(x,y) in enumerate(zip(a,b)):walk(x,y,loc+(i,))
            elif isinstance(a,str) and loc in dict(visible_fields(source)):
                if loc in fields:assert b==fields[loc]['chinese'],('Approved text differs',path,loc)
            else:assert a==b,('Patchouli non-text data changed',path,loc)
        walk(source,target);structural.append(out)
    native=read(BASE/'manuals/final-verification.json')
    assert native['target_sources_fresh'] and native['unique_decisions']
    assert not read(BASE/'manuals/ast-review.json'),'Unreviewed Markdown AST differences'
    assert not read(BASE/'manuals/yaml-metadata-review.json'),'Non-display YAML metadata changed'
    actual_findings=read(BASE/'manuals/structural-problems.json')
    reviewed=read(BASE/'manuals/structural-reviewed-differences.json')
    key=lambda x:(x['path'],x.get('field'),x['type'])
    assert {key(x) for x in actual_findings}=={key(x) for x in reviewed},'Unreviewed protected-structure changes'
    assert all(x.get('reviewed_reason') for x in reviewed)
    native_hashes=read(BASE/'manuals/native-input-hashes.json')
    for d in read(BASE/'decisions/manuals.json'):
        if d['status']=='accepted' and d['format']!='Patchouli':
            assert native_hashes[d['path']]['source_lf']==d['english_sha256'],('Native source evidence outdated',d['path'])
            assert native_hashes[d['path']]['chinese']==hashlib.sha256((ROOT/d['file']).read_bytes()).hexdigest(),('Native output evidence outdated',d['path'])
    report={'status':'passed','build_manifest_sha256':hashlib.sha256((BASE/'build-manifest.json').read_bytes()).hexdigest(),'json_files':len(parsed),'global_language_keys':len(global_keys),'patchouli_documents_with_current_source_structure':len(structural),'manual_documents':native['accepted_documents'],'manual_fields':native['accepted_patchouli_fields'],'reviewed_structure_exceptions':len(reviewed),'resource_files_verified':len(file_set),'source_jars_modified':False,'in_game_tested':False,'installed_to_game':False}
    (BASE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
