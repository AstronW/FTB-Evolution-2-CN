#!/usr/bin/env python3
"""Independent invariants for installed quest translations and reward-name overlay."""
from pathlib import Path
import collections, hashlib, json, re
import quest_translation as q

def component_inventory(value,path=()):
    out=[]
    if isinstance(value,str):
        try: nested=json.loads(value)
        except (ValueError,TypeError):return out
        if isinstance(nested,(dict,list)):return component_inventory(nested,path+('component',))
    elif isinstance(value,list):
        for i,v in enumerate(value):out.extend(component_inventory(v,path+(i,)))
    elif isinstance(value,dict):
        for k,v in value.items():
            if k in {'click_event','clickEvent','keybind','translate','color','font','bold','italic','underlined','strikethrough','obfuscated','insertion','score','selector','nbt','interpret','storage','block','entity'}:
                out.append((path+(k,),v))
            elif k in {'hover_event','hoverEvent'}:
                out.append((path+(k,'action'),v.get('action')))
                if v.get('action')!='show_text':out.append((path+(k,),v))
            out.extend(component_inventory(v,path+(k,)))
    return out

def list_shapes(value,path=()):
    out=[]
    if isinstance(value,list):
        out.append((path,len(value)))
        for i,v in enumerate(value):out.extend(list_shapes(v,path+(i,)))
    return out

def main():
    manifest=q.read_json(q.WORK/'source_manifest.json',{})
    current={str(p.relative_to(q.SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in q.SOURCE.rglob('*.json5')}
    assert current==manifest,'English source changed'
    checked=0;keys=0;unmodified=[]
    for p in sorted(q.TARGET.rglob('*.json5')):
        rel=p.relative_to(q.TARGET);en=q.load_source(q.SOURCE/rel);zh=json.loads(p.read_text())
        q.assert_quest_format(zh)
        assert list(en)==list(zh),(rel,'language keys or order changed')
        for k in en:
            assert type(en[k]) is type(zh[k]),(rel,k,'value type changed')
            assert list_shapes(en[k])==list_shapes(zh[k]),(rel,k,'description paragraph count changed')
            assert component_inventory(en[k])==component_inventory(zh[k]),(rel,k,'component action/binding/style changed')
        checked+=1;keys+=len(en)
        es=q.segments(en);zs=q.segments(zh)
        # Segment IDs refer to source; Chinese may have no Latin characters, so collect all text leaves independently.
        def collect(v):
            leaves=[]
            q.transform(v,lambda s:leaves.append(s) or s)
            return leaves
        a,b=collect(en),collect(zh)
        assert len(a)==len(b),(rel,'text leaf count changed')
        for src,dst in zip(a,b):
            q.assert_ascii(dst, (str(rel),'visible text'))
            assert q.protected(src)==q.protected(dst),(rel,'format or markup changed')
            # Commands and resource identifiers must be preserved even inside prose.
            ids=lambda s:collections.Counter(re.findall(r'(?<![A-Za-z0-9_])[a-z][a-z0-9_]*:[a-z0-9_./-]+',s))
            assert ids(src)==ids(dst),(rel,src,dst,'resource ID changed')
            cmds=lambda s:collections.Counter(re.findall(r'(?<![A-Za-z0-9_:])/[a-z][a-z0-9_]*',s))
            assert cmds(src)==cmds(dst),(rel,src,dst,'command name changed')
            if src==dst and q.needs_translation(src):unmodified.append({'file':str(rel),'text':src})
    reward_en=q.read_json(q.WORK/'reward_labels_source.json',{})
    reward_zh=q.read_json(q.WORK/'reward_labels_zh_cn.json',{})
    assert reward_en.keys()==reward_zh.keys(),'reward label coverage mismatch'
    live=q.read_json(q.ROOT/'.minecraft/kubejs/assets/ftb/lang/zh_cn.json',{})
    for k,v in reward_zh.items():
        assert live.get(k)==v,('missing installed reward label',k)
        assert q.protected(v)==q.protected(reward_en[k]),('reward placeholder mismatch',k)
    names=q.read_json(q.WORK/'quest_item_names.json',{}).get('entries',{})
    for k,entry in names.items():
        assert live.get(k)==entry['zh'],('missing installed quest item name',k)
        assert q.protected(entry['en'])==q.protected(entry['zh']),('quest item name format changed',k)
    extra_count=0
    for group in q.read_json(q.WORK/'quest_extra_labels.json',[]):
        source=q.ROOT/group['source']
        assert hashlib.sha256(source.read_bytes()).hexdigest()==group['source_sha256'],'supplementary source changed'
        original=q.load_source(source)
        overlay=q.read_json(q.ROOT/group['target'],{})
        for k,entry in group['entries'].items():
            assert original.get(k)==entry['en'],('supplementary English changed',k)
            assert overlay.get(k)==entry['zh'],('supplementary name not installed',k)
            q.assert_ascii(entry['zh'],k)
            assert q.protected(entry['en'])==q.protected(entry['zh']),('supplementary format changed',k)
            extra_count+=1
    report={'checked_files':checked,'checked_keys':keys,'reward_labels':len(reward_zh),'quest_item_labels':len(names),'quest_extra_labels':extra_count,'preserved_english':unmodified,'status':'passed'}
    q.dump(q.WORK/'reports/verification.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='preserved_english'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
