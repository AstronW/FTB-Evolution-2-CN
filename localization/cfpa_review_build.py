"""Build/check the individually reviewed 1.4.0 CFPA/PR overlay.

Only decisions with status=accepted are emitted. The original repository, PR
cache, game installation and prior project translations remain input-only.
"""
from pathlib import Path
import argparse, collections, copy, hashlib, io,json, re,zipfile
from assess_1_4_remaining import scan_instance, GAME
from cfpa_review_format import invariant_errors

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'localization/cfpa_review'
PACK=ROOT/'.minecraft/resourcepacks/FTB-Evolution-2-CFPA-Reviewed-zh_CN'
ARCHIVE=ROOT/'dist/FTB-Evolution-2-1.4.0-CFPA-Reviewed-zh_CN.zip'
LANG_FILES=['primary.json','witchery.json','mods.json','remaining-a.json','remaining-b.json','group-labels.json']


def read(path):return json.loads(path.read_text())
def digest(data):return hashlib.sha256(data).hexdigest()
def archive_content_digest(outputs):
    # ZIP bytes depend on the local zlib build, so the reproducible identity is the
    # ordered member list plus each member's own hash. Byte equality is implied by
    # it without pinning an environment-specific deflate implementation.
    h=hashlib.sha256()
    for rel,data in sorted(outputs.items()):h.update(rel.encode()+b'\0'+bytes.fromhex(digest(data)))
    return h.hexdigest()
def encode(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
def identity(d):return (d.get('resource_domain','lang'),d['namespace'],d['key'])
def manual_identity(d):return (d['path'],d.get('field'))
def reviewed_exceptions(decision):
    raw=decision.get('validation_exceptions',{})
    if isinstance(raw,list):
        assert all(isinstance(x,dict) and x.get('error') and x.get('reason') for x in raw),'Invalid exception evidence'
        return {x['error']:x['reason'] for x in raw}
    assert isinstance(raw,dict),'Invalid exception type'
    return raw
def visible_fields(value,path=()):
    if isinstance(value,dict):
        for k,v in value.items():
            if k in {'name','description','text','title','subtitle','landing_text','caption'} and isinstance(v,str):yield path+(k,),v
            elif isinstance(v,(dict,list)):yield from visible_fields(v,path+(k,))
    elif isinstance(value,list):
        for i,v in enumerate(value):yield from visible_fields(v,path+(i,))
def field_path(field):return tuple(int(x) if x.isdigit() else x for x in field.split('.'))
def get(value,path):
    for part in path:value=value[part]
    return value
def put(value,path,text):
    for part in path[:-1]:value=value[part]
    value[path[-1]]=text


def compile_overlay():
    instance=read(GAME/'instance.json')
    assert instance['version']=='1.4.0' and instance['mcVersion']=='26.1.2','Game version changed; reconcile the reviewed sources first'
    for source in read(BASE/'code-evidence/jar-manifest.json'):
        assert digest(Path(source['jar']).read_bytes())==source['sha256'],'Code evidence JAR changed; review the correction again'
    decisions=[]
    for name in LANG_FILES:decisions.extend(read(BASE/'decisions'/name))
    expected=[]
    for name in ['witchery','mods','remaining']:
        expected.extend(('lang',r['namespace'],r['key']) for r in read(BASE/'inputs'/f'{name}.json'))
    expected.extend(('group_lang','collapsible_groups',r['key']) for r in read(BASE/'inputs/group-labels.json')['rows'] if r['state']!='no_chinese_candidate')
    actual=[identity(d) for d in decisions]
    assert len(actual)==len(set(actual)),'Duplicate review decisions'
    assert set(actual)==set(expected),'Missing or unexpected review decision'
    for d in decisions:assert d['status'] in {'accepted','rejected'} and d.get('reason'),identity(d)
    langs,origins,documents,jars=scan_instance(GAME,True)
    english=langs['en_us']
    groups={r['key']:r for r in read(ROOT/'localization/reports/remaining-1.4.0-group-labels.json')['rows']}
    scope=read(ROOT/'localization/language_scope.json')
    outputs={};language=collections.defaultdict(dict);accepted=[];exceptions=[]
    for d in decisions:
        if d['status']!='accepted':continue
        ns=d['namespace'];domain=d.get('resource_domain','lang')
        assert re.fullmatch(r'[a-z0-9_.-]+',ns) and ns not in {'.','..'} and domain in {'lang','group_lang'},identity(d)
        assert ns not in scope['excluded_namespaces'] and not any(ns.startswith(p) for p in scope['excluded_namespace_prefixes']),ns
        if domain=='group_lang':assert d['key'] in groups and groups[d['key']]['english']==d['english'],identity(d)
        else:assert english.get(d['key'])==d['english'],('Current English changed',identity(d))
        errors=set(invariant_errors(d['english'],d['chinese']))
        allowances=reviewed_exceptions(d)
        assert all(isinstance(reason,str) and reason.strip() for reason in allowances.values()),identity(d)
        assert not errors-set(allowances),('Protected format changed',identity(d),sorted(errors-set(allowances)))
        # Exceptions never bypass checks silently; exact reviewed source/output is
        # pinned in the emitted provenance manifest and all exceptions are reported.
        if errors:exceptions.append({'key':d['key'],'namespace':ns,'findings':{x:allowances[x] for x in sorted(errors)}})
        path=f'assets/{ns}/{domain}/zh_cn.json'
        assert d['key'] not in language[path],identity(d)
        language[path][d['key']]=d['chinese'];accepted.append(d)
    for path,values in sorted(language.items()):outputs[path]=encode(dict(sorted(values.items())))
    manual=read(BASE/'decisions/manuals.json')
    inventory=read(BASE/'inputs/manual-inventory.json')
    targets={manual_identity(u) for u in inventory['units'] if not u['covered_candidate'] and u['cfpa_best_status']!='none'}
    assert set(map(manual_identity,manual))==targets and len(manual)==len(targets),'Manual decisions incomplete or duplicated'
    patchouli={};manual_counts=collections.Counter();manual_sources={}
    for d in manual:
        assert d['status'] in {'accepted','rejected'} and d.get('reason'),manual_identity(d)
        if d['status']!='accepted':continue
        path=d['path'];raw=documents[path][0]
        raw_text=raw.decode('utf-8-sig',errors='replace') if isinstance(raw,bytes) else raw
        text=raw_text.replace('\r\n','\n').replace('\r','\n')
        manual_sources[path]={'sha256_raw':digest(raw_text.encode()),'sha256_lf':digest(text.encode())}
        out=d['output_resource_path']
        assert out.startswith(('assets/','data/')) and '..' not in Path(out).parts and out!=path,out
        if d['format']=='Patchouli':
            source=json.loads(text);parts=field_path(d['field']);en=get(source,parts)
            assert en==d['english'] and digest(en.encode())==d['english_sha256'],manual_identity(d)
            findings=set(invariant_errors(en,d['chinese']))
            allowances=reviewed_exceptions(d)
            assert not findings-set(allowances),('Manual field format changed',manual_identity(d),sorted(findings-set(allowances)))
            if findings:exceptions.append({'path':path,'field':d['field'],'findings':{x:allowances[x] for x in sorted(findings)}})
            if out not in patchouli:
                target=copy.deepcopy(source)
                # Reuse existing official visible text only, retaining the current
                # English document's full recipe/action/ID/component structure.
                if out in documents:
                    existing=json.loads(documents[out][0])
                    for field,v in visible_fields(source):
                        if v in english:continue
                        try:old=get(existing,field)
                        except (KeyError,IndexError,TypeError):continue
                        if isinstance(old,str) and re.search(r'[\u3400-\u9fff]',old):put(target,field,old)
                patchouli[out]=target
            put(patchouli[out],parts,d['chinese'])
        else:
            assert digest(text.encode())==d['english_sha256'],('Manual source changed',path)
            file=ROOT/d['file'];assert file.is_file(),str(file)
            assert out not in outputs,('Conflicting manual output',out)
            outputs[out]=file.read_bytes()
        manual_counts[d['format']]+=1
    for path,value in sorted(patchouli.items()):outputs[path]=encode(value)
    outputs['pack.mcmeta']=encode({'pack':{'description':'FTB Evolution 2 1.4.0 reviewed CFPA/PR translations','min_format':84,'max_format':84}})
    outputs['CFPA-LICENSE.txt']=(ROOT/'CFPA/LICENSE').read_bytes()
    attribution=['# Translation sources','',
        'CFPA-derived translations: CC BY-NC-SA 4.0. See CFPA-LICENSE.txt.',
        'Upstream: https://github.com/CFPAOrg/Minecraft-Mod-Language-Package',
        'Local review, terminology, key mapping, version adaptation and format repairs were applied.',
        'Native mod translation repairs retain their original mod provenance and license; they are not relicensed by this notice.',
        'This is a project work-copy artifact. It has not been installed or tested in the game.','',
        '| Kind | Author/PR or repository | Version | Commit | Source |','| --- | --- | --- | --- | --- |']
    sources={}
    for d in accepted+[d for d in manual if d['status']=='accepted']:
        s=d.get('source',{});key=json.dumps(s,ensure_ascii=False,sort_keys=True)
        # Attribute files, not every individual key or repeated English fragment.
        source_path=s.get('repo_path',s.get('path',s.get('source_jar','')))
        number=s.get('number',s.get('pr'))
        source_kind=s.get('kind','pr' if number else 'cfpa')
        commit=s.get('head_sha',s.get('cfpa_commit',''))
        if source_kind=='cfpa' and not commit:commit=read(ROOT/'project.json')['cfpa']['commit']
        sid=(source_kind,number,s.get('author','CFPA contributors'),s.get('version',''),commit,source_path)
        sources[sid]=s
    notices=[]
    for sid in sorted(sources,key=str):
        kind,number,author,version,sha,path=sid
        if number:author=f'{author} / https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/{number}'
        attribution.append('| '+' | '.join(str(x).replace('|','\\|') for x in [kind,author,version,sha,path])+' |')
        source=sources[sid]
        if source.get('kind')=='official_repaired' and source.get('license_file'):
            jar=ROOT/source['path']
            assert digest(jar.read_bytes())==source['jar_sha256'],'Native translation input changed'
            with zipfile.ZipFile(jar) as archive:
                outputs['licenses/ANIMAL-PEN-LICENSE.txt']=archive.read(source['license_file'])
            notices.append('Native Animal Pen entries retain the JAR-declared '+source['license']+'; see licenses/ANIMAL-PEN-LICENSE.txt. Per-entry sources are retained in the project decisions.')
    attribution.extend(['',*notices])
    outputs['ATTRIBUTION.md']=('\n'.join(attribution)+'\n').encode()
    source_manifest=BASE/'inputs/manual-source-manifest.json'
    if source_manifest.exists():assert read(source_manifest)==manual_sources,'Manual source snapshot changed; reconcile before rebuilding'
    stats={'target_pack':'1.4.0','language_keys':sum(len(v) for k,v in language.items() if '/lang/' in k),'group_labels':sum(len(v) for k,v in language.items() if '/group_lang/' in k),'language_decisions':dict(collections.Counter(d['status'] for d in decisions)),'manual_decisions':dict(collections.Counter(d['status'] for d in manual)),'manual_accepted_units':dict(manual_counts),'patchouli_output_documents':len(patchouli),'resource_files':len(outputs),'validation_exceptions':exceptions,'in_game_tested':False,'installed_to_game':False}
    manifest={'stats':stats,'files':{k:digest(v) for k,v in sorted(outputs.items())},'reviewed_decisions_sha256':{name:digest((BASE/'decisions'/name).read_bytes()) for name in LANG_FILES+['manuals.json']},'manual_sources':manual_sources}
    return outputs,manifest,manual_sources


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['build','check']);args=parser.parse_args()
    outputs,manifest,sources=compile_overlay()
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for rel,data in sorted(outputs.items()):
            entry=zipfile.ZipInfo(rel,date_time=(1980,1,1,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED
            entry.external_attr=0o100644 << 16
            archive.writestr(entry,data)
    payload=buffer.getvalue()
    manifest['archive_content_sha256']=archive_content_digest(outputs)
    if args.command=='build':
        assert not PACK.is_symlink() and PACK.resolve().is_relative_to(ROOT.resolve()),'Output path escapes project work copy'
        # Preflight every input before mutating this tool-owned output directory.
        previous=read(BASE/'build-manifest.json') if (BASE/'build-manifest.json').exists() else {'files':{}}
        for rel in set(previous['files'])-set(outputs):
            owned=PACK/rel
            if owned.is_file():owned.unlink()
        for rel,data in outputs.items():
            target=PACK/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        (BASE/'inputs/manual-source-manifest.json').write_bytes(encode(sources))
        (BASE/'build-manifest.json').write_bytes(encode(manifest))
        ARCHIVE.parent.mkdir(parents=True,exist_ok=True);ARCHIVE.write_bytes(payload)
        ARCHIVE.with_suffix('.zip.sha256').write_text(digest(payload)+'  '+ARCHIVE.name+'\n')
    else:
        assert read(BASE/'build-manifest.json')==manifest,'Reviewed data changed; rebuild required'
        for rel,data in outputs.items():assert (PACK/rel).read_bytes()==data,('Output differs',rel)
        assert {str(p.relative_to(PACK)) for p in PACK.rglob('*') if p.is_file()}==set(outputs),'Unexpected output files'
        with zipfile.ZipFile(ARCHIVE) as archive:
            assert archive.namelist()==sorted(outputs),'Archive member list differs'
            for rel in sorted(outputs):assert archive.read(rel)==outputs[rel],('Archive member differs',rel)
            assert archive.testzip() is None,'Archive is corrupt'
    print(json.dumps({'status':'passed','command':args.command,**manifest['stats']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
