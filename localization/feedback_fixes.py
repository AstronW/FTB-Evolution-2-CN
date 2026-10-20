"""Source-bound 2026-10-19 feedback overlays; never rewrite upstream manuals/JARs."""
import hashlib,json,pathlib,re,sys,zipfile
from punctuation import assert_ascii
from protected_text import signature
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'localization/feedback_20261019'
OUTPUT=BASE/'pack'
GAME=pathlib.Path(json.loads((ROOT/'project.json').read_text())['target_instance'])
TAG=re.compile(r'<(RecipeFor|RecipesFor)\b[^>]*\bid="([^"]+)"[^>]*>')
def sha(data):return hashlib.sha256(data).hexdigest()
def encode(data):return (json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
def read(p):return json.loads(p.read_text())
def inputs():
    result={};sources={}
    def bind(p):sources[str(p.relative_to(GAME))]=sha(p.read_bytes())
    for pat in ['nodeworks-*.jar','oracle_index-*.jar','kindredspirits-*.jar','patchouli-*.jar','guideme-*.jar','ftb-industrial-*.jar','auroral-*.jar','Powah-*.jar','justdynathings-*.jar']:
        for p in (GAME/'mods').glob(pat):bind(p)
    db=GAME/'config/ftbmaterials/unifier-db.json';bind(db)
    bind(GAME/'kubejs/server_scripts/recipes/removals.js')
    mapping=read(db)['items']
    metadata=read(BASE/'metadata-translations.json')
    for rel,translations in metadata.items():
        book,rest=rel.split('/',1)
        jar=next((GAME/'mods').glob('kindredspirits-*.jar' if book=='kindredspirits' else 'oracle_index-*.jar'))
        member='assets/oracle_index/books/'+rel
        with zipfile.ZipFile(jar) as z:data=json.loads(z.read(member))
        assert set(data)==set(translations),(rel,'metadata coverage')
        for k,zh in translations.items():assert_ascii(zh,rel);data[k]['name']=zh
        target='assets/oracle_index/books/'+book+'/translated/zh_cn/'+rest.removeprefix('docs/')
        result[target]=encode(data)
    landings=read(BASE/'landing-translations.json')
    for ns,translation in landings.items():
        found=set()
        for jar in (GAME/'mods').glob('*.jar'):
            with zipfile.ZipFile(jar) as z:
                for member in z.namelist():
                    if member.startswith('data/'+ns+'/patchouli_books/') and member.endswith('/book.json'):
                        bind(jar);book=json.loads(z.read(member));found.update(v for k,v in book.items() if k in {'name','landing_text','subtitle'})
        assert set(translation)<=found,(ns,'book source changed')
        for en,zh in translation.items():
            assert_ascii(zh,ns);assert signature(en)==signature(zh),(ns,en)
        # Patchouli's current landing GUI calls Component.translatable on these
        # literal English values too. No server book definition needs replacing.
        result[f'assets/{ns}/lang/zh_cn.json']=encode(translation)
    return result,sources,mapping

def component_corrections(outputs, result, sources):
    corrections=read(BASE/'component-corrections.json')
    grouped={}
    for row in corrections:grouped.setdefault(row['page'],[]).append(row)
    for member,rows in grouped.items():
        if member in outputs:original=outputs[member][0]
        else:
            ns=member.split('/')[1]
            pat='Powah-*.jar' if ns=='powah' else ns+'-*.jar'
            jar=next((GAME/'mods').glob(pat))
            with zipfile.ZipFile(jar) as z:original=z.read(member)
        text=result.get(member,original).decode()
        for row in rows:
            assert text.count(row['old'])==1,(member,row['old'])
            text=text.replace(row['old'],row['new'],1)
            if row['classification']=='pack_disabled' and 'justdynathings' in member:
                rid=re.search('id="([^"]+)"',row['old'])[1]
                ns,name=rid.split(':')
                p=GAME/f'datapacks/ftb/data/{ns}/recipe/{name}.json'
                assert any(c['type']=='neoforge:never' for c in read(p)['neoforge:conditions'])
                sources[str(p.relative_to(GAME))]=sha(p.read_bytes())
        result[member]=text.encode()
    return corrections

def resource_overrides(base_outputs=None):
    """Return only explicitly built and source-verified feedback files."""
    manifest=read(BASE/'manifest.json')
    if base_outputs is not None:
        for member,digest in manifest['base_files'].items():
            assert member in base_outputs and sha(base_outputs[member][0])==digest,('Feedback base page changed',member)
    for rel,digest in manifest['source_inputs'].items():assert sha((GAME/rel).read_bytes())==digest,rel
    for rel,digest in manifest['files'].items():
        p=OUTPUT/rel;assert sha(p.read_bytes())==digest,rel
        yield rel,p

def compile_pages(outputs,mapping):
    changes=[];patches={}
    for member,(data,origin) in outputs.items():
        if not member.endswith(('.md','.mdx')) or '/oracle_index/' in member:continue
        text=data.decode();ns=member.split('/')[1]
        def replace(m):
            old=m[2] if ':' in m[2] else ns+':'+m[2]
            new=mapping.get(old)
            if not new:return m[0]
            changes.append({'page':member,'tag':m[1],'old':old,'new':new,'origin':origin,'base_sha256':sha(data)})
            return m[0].replace('id="'+m[2]+'"','id="'+new+'"',1)
        changed=TAG.sub(replace,text)
        if changed!=text:patches[member]=changed.encode()
    return patches,changes

def build(command):
    import release_pack
    # Base build must remain independent from feedback overlays.
    outputs,_,_=release_pack.assemble_resourcepack([],include_feedback=False)
    result,sources,mapping=inputs()
    pages,changes=compile_pages(outputs,mapping);result.update(pages)
    corrections=component_corrections(outputs,result,sources)
    base_files={member:sha(outputs[member][0]) for member in result if member in outputs and not member.endswith('/lang/zh_cn.json')}
    manifest={'target_pack_version':'1.4.0','source_inputs':sources,'base_files':base_files,'files':{k:sha(v) for k,v in sorted(result.items())},'recipe_reference_changes':changes,'component_corrections':corrections,'in_game_tested':False}
    if command=='build':
        for rel,data in result.items():
            p=OUTPUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        (BASE/'manifest.json').write_bytes(encode(manifest))
    else:
        assert read(BASE/'manifest.json')==manifest,'Feedback source/outputs changed; rebuild'
        assert {p.relative_to(OUTPUT).as_posix() for p in OUTPUT.rglob('*') if p.is_file()}==set(result)
        for rel,data in result.items():assert (OUTPUT/rel).read_bytes()==data,rel
    print(f'{command}: {len(result)} resource files, {len(changes)} unified recipe references')
if __name__=='__main__':build(sys.argv[1])
