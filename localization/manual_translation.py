"""Scoped GuideME manual translation build/check tool."""
from protected_text import signature
import collections,hashlib,json,pathlib,re,sys,zipfile,html
from punctuation import assert_ascii
ROOT=pathlib.Path(__file__).resolve().parent.parent
BASE=ROOT/'localization/manuals'
PACK=ROOT/'.minecraft/resourcepacks/FTB-Evolution-2-Manuals-zh_CN'

def sources():
    result={}
    jar=next((ROOT/'.minecraft/mods').glob('ftb-industrial-contraptions-*.jar'))
    with zipfile.ZipFile(jar) as z:
        for n in z.namelist():
            if n.startswith('assets/ftbic/ftbic/') and n.endswith('.md') and not '/_' in n:
                result['ftbic/'+n.removeprefix('assets/ftbic/ftbic/')]=z.read(n).decode()
    jar=next((ROOT/'.minecraft/mods').glob('nodeworks-*.jar'))
    with zipfile.ZipFile(jar) as z:
        for n in z.namelist():
            if n.startswith('assets/nodeworks/nodeworksguide/') and n.endswith('.md') and not '/_' in n:
                result['nodeworks/'+n.removeprefix('assets/nodeworks/nodeworksguide/')]=z.read(n).decode()
    for ns,root in [('ftb','guides/ftb'),('ftbic','ftbic'),('nodeworks','nodeworksguide')]:
        folder=ROOT/f'.minecraft/kubejs/assets/{ns}/{root}'
        for p in folder.rglob('*.md'):
            rel=p.relative_to(folder).as_posix()
            if '/_' not in '/'+rel:result[ns+'/'+rel]=p.read_text()
    return dict(sorted(result.items()))

def lua_comment(line):
    quoted=None;escaped=False
    for i,c in enumerate(line):
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c==quoted:quoted=None
        elif c in ("'",'"'):quoted=c
        elif line[i:i+2]=='--':return i
    return None

def segments(text):
    front=False;code=False;code_lang=""
    for i,line in enumerate(text.splitlines()):
        if line=='---' and (i==0 or front):front=not front;continue
        if front:
            if re.match(r'\s*title:',line):yield i,line
            continue
        if line.lstrip().startswith('```'):
            code=not code;code_lang=line.strip().removeprefix('```');continue
        if code:
            pos=lua_comment(line) if code_lang=='lua' else None
            if pos is not None and re.search('[A-Za-z]',line[pos+2:]):yield i,line
            continue
        visible=re.sub(r'<[^>]+>|`[^`]+`|\]\([^)]*\)|[a-z_]+:[a-z0-9_./-]+','',line)
        if re.search('[A-Za-z]',visible):yield i,line

def protections(line):
    return {
      'syntax':signature(line),
      'tags':re.findall(r'<[^>]+>',line),
      'links':re.findall(r'\]\(([^)]*)\)',line),
      'code':dict(collections.Counter(re.findall(r'`[^`]+`',line))),
      'numbers':dict(collections.Counter(re.findall(r'(?<![A-Za-z_])\d+(?:[,.]\d+)*(?:%)?',line))),
    }

def target(key):
    ns,rel=key.split('/',1)
    root='guides/ftb' if ns=='ftb' else ('nodeworksguide' if ns=='nodeworks' else 'ftbic')
    if ns=='ftb':
        book,rel=rel.split('/',1)
        return PACK/f'assets/ftb/{root}/{book}/_zh_cn/{rel}'
    return PACK/f'assets/{ns}/{root}/_zh_cn/{rel}'

def anchor_plan(key,source):
    if not key.startswith('nodeworks/'):return {}
    plan={}
    for i,line in enumerate(source.splitlines()):
        match=re.match(r'\s*#{1,6}\s+(.+)',line)
        if not match:continue
        label=re.sub(r'<[^>]+>','',match[1])
        label=re.sub(r'\[([^]]+)\]\([^)]*\)',r'\1',label)
        label=html.unescape(label.replace('`','').replace('*','')).strip()
        native=re.sub(r'\s+','-',label.lower())
        github=re.sub(r'[^\w\s-]','',label.lower())
        github=re.sub(r'\s+','-',github)
        names={native,github}
        if re.fullmatch(r'[A-Za-z][A-Za-z0-9]*',label):names.add(label)
        if key=='nodeworks/items-blocks/storage_card.md' and label=='Configuration':names.add('configuring-priority')
        if key=='nodeworks/lua-api/network.md' and label=='channel':names.add('channel-getall')
        if key=='nodeworks/lua-api/variable-handle.md' and label=='increment / decrement':names.add('increment--decrement')
        plan[i]=sorted(n for n in names if n)
    return plan

def with_anchors(key,source,translated):
    lines=translated.splitlines()
    for i,names in anchor_plan(key,source).items():
        tag=' '.join('<a name="'+html.escape(n,quote=True)+'" />' for n in names)
        lines[i]=re.sub(r'^(\s*#{1,6})\s+',lambda mt:mt[1]+' '+tag+' ',lines[i],count=1)
    return '\n'.join(lines)+'\n'

def main():
    src=sources(); BASE.mkdir(parents=True,exist_ok=True)
    manifest={k:hashlib.sha256(v.encode()).hexdigest() for k,v in src.items()}
    mf=BASE/'source_manifest.json'
    cmd=sys.argv[1]
    if cmd=='init':
        if mf.exists():assert json.loads(mf.read_text())==manifest,'Source changed'
        else:mf.write_text(json.dumps(manifest,indent=2)+'\n')
        print(len(src),'source pages');return
    assert json.loads(mf.read_text())==manifest,'Source changed; review before rebuilding'
    if cmd=='show':
        keys=[k for k in src if k.startswith(sys.argv[2])]
        for k in keys:
            print('\nFILE',k)
            for i,s in segments(src[k]):print(f'{i}: {s}')
        return
    corrections=json.loads((BASE/'source_corrections.json').read_text()) if (BASE/'source_corrections.json').exists() else {}
    entry_manifest=BASE/'entry_source_manifest.json'
    if entry_manifest.exists():
        for path,sha in json.loads(entry_manifest.read_text()).items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,(path,'guide entry changed')
    for extra in (BASE/'extra_resources').rglob('*'):
        if extra.is_file():
            path=PACK/extra.relative_to(BASE/'extra_resources')
            if cmd=='build':path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(extra.read_bytes())
            else:assert path.read_bytes()==extra.read_bytes(),(str(path),'extra resource drift')
    report=[]
    for key,text in src.items():
        trans=BASE/'translations'/pathlib.Path(key).with_suffix('.json')
        data=json.loads(trans.read_text()) if trans.exists() else {}
        seg=dict(segments(text));missing=[i for i in seg if str(i) not in data]
        assert not (set(data)-{str(i) for i in seg}),(key,'unknown segment')
        lines=text.splitlines()
        lua_comments={};in_lua=False
        for line_no,line in enumerate(lines):
            if line.lstrip().startswith('```'):
                in_lua=(line.strip()=='```lua');continue
            if in_lua and lua_comment(line) is not None:lua_comments[line_no]=lua_comment(line)
        for i,en in seg.items():
            if str(i) not in data:continue
            zh=data[str(i)]
            expected=protections(en);actual=protections(zh)
            correction=corrections.get(f'{key}#{i}')
            if correction:
                assert correction['source']==en and correction['translation']==zh and correction['reason'],(key,i,'correction drift')
                expected.pop('numbers');actual.pop('numbers')
            assert expected==actual,(key,i,'protected content changed',expected,actual)
            # Lua comment translations must preserve all code before the comment.
            if i in lua_comments:
                pos=lua_comments[i]
                if en[:pos].strip() or en.lstrip().startswith('--'):
                    assert zh[:pos+2]==en[:pos+2],(key,i,'Lua code prefix changed')
            assert '\n' not in zh,(key,i,'new line')
            assert_ascii(zh, (key,i))
            lines[i]=zh
        out=with_anchors(key,text,'\n'.join(lines)+'\n')
        if not missing:
            path=target(key)
            if cmd=='build':path.parent.mkdir(parents=True,exist_ok=True);path.write_text(out)
            else:assert path.read_text()==out,(key,'output drift')
        report.append({'page':key,'segments':len(seg),'translated':len(data),'complete':not missing,'missing':missing})
    (BASE/'progress.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(sum(r['complete'] for r in report),'/',len(report),'pages complete;',sum(r['translated'] for r in report),'/',sum(r['segments'] for r in report),'segments')
if __name__=='__main__':main()
