#!/usr/bin/env python3
"""Translate FTB Quests text leaves without changing quest data or component actions.

show RELATIVE_FILE [START [END]]: print numbered source text leaves
build: write only fully translated language files and a progress report
check: validate generated files and the immutable source manifest
"""
from pathlib import Path
import json, re, hashlib, sys, collections, zipfile
from punctuation import assert_ascii
from protected_text import signature
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'localization'
SOURCE=ROOT/'.minecraft/config/ftbquests/quests/lang/en_us'
TARGET=SOURCE.parent/'zh_cn'

def load_source(path):
    s=path.read_text(encoding='utf-8-sig');out=[];quoted=False;escaped=False
    for i,c in enumerate(s):
        if quoted:
            out.append(c)
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        else:
            if c=='"':quoted=True
            if c==',' and s[i+1:].lstrip().startswith(('}',']')):continue
            out.append(c)
    return json.loads(''.join(out))

def read_json(p,default):return json.loads(p.read_text()) if p.exists() else default

def dump(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def needs_translation(s):
    if re.fullmatch(r'\{(?:@pagebreak|image:.*)\}',s):return False
    return bool(re.search('[A-Za-z]',s))

def transform(data,replace):
    """Only visible literal strings are handed to replace; preserve actions and IDs."""
    def component(v):
        if isinstance(v,str):return replace(v)
        if isinstance(v,list):return [component(t) for t in v]
        if isinstance(v,dict):
            out=dict(v)
            for k in ('text','extra','with','fallback','separator'):
                if k in out:out[k]=component(out[k])
            for k in ('hover_event','hoverEvent'):
                if k in out and out[k].get('action')=='show_text':
                    out[k]=dict(out[k])
                    for a in ('value','contents'):
                        if a in out[k]:out[k][a]=component(out[k][a])
            return out
        return v
    def literal(v):
        if isinstance(v,list):return [literal(t) for t in v]
        if isinstance(v,str):
            if v.lstrip().startswith(('[','{')):
                try:
                    parsed=json.loads(v)
                    if isinstance(parsed,(dict,list)):
                        changed=component(parsed)
                        return v if changed==parsed else json.dumps(changed,ensure_ascii=False,separators=(',',':'))
                except json.JSONDecodeError:pass
            return replace(v)
        return v
    return {k:literal(v) for k,v in data.items()}

def segments(data):
    out=[]
    def record(s):
        if needs_translation(s):out.append(s)
        return s
    transform(data,record)
    return out

def protected(s):
    for entry in read_json(WORK/'quest_format_corrections.json',[]):
        if s == entry['source']:
            before, after = signature(s, quest=True), signature(entry['translation'], quest=True)
            assert {k:v for k,v in before.items() if k != 'colors'} == {k:v for k,v in after.items() if k != 'colors'}
            assert entry['reason']
            s = entry['translation']
            break
    return (signature(s, quest=True), collections.Counter(re.findall(r'\{(?:@pagebreak|image:[^{}]*)\}|(?:&|§)[0-9a-fk-or]|%(?:\d+\$)?[sdf]|https?://[^\s<>]+',s,re.I)))

def assert_quest_format(data):
    """Check plain text codes against FTB Library 26.1.2.9's parser.

    JSON components use Minecraft's component codec, so literal ampersands in
    those components must not be interpreted as FTB formatting codes.
    """
    def check(value, context):
        if isinstance(value, list):
            for i, part in enumerate(value):check(part, f'{context}[{i}]')
        elif isinstance(value, str):
            try:
                if isinstance(json.loads(value), (dict, list)):return
            except ValueError:pass
            i=0
            while i < len(value):
                if value[i] in '&§' and (i == 0 or value[i-1] != '\\'):
                    tail=value[i+1:]
                    if tail.startswith('#'):
                        if not re.match(r'#[0-9a-fA-F]{6}', tail):
                            raise ValueError(f'{context}: invalid hex color at {i}: {value!r}')
                        i+=8
                        continue
                    if not tail or tail[0] not in '0123456789abcdefklmnorz':
                        raise ValueError(f'{context}: invalid quest format at {i}; escape literal & as \\&: {value!r}')
                    i+=2
                    continue
                i+=1
    for key, value in data.items():check(value, key)

def translate(data,translated,terms):
    i=-1;missing=[];resolved=[]
    def sub(s):
        nonlocal i
        if not needs_translation(s):return s
        i+=1
        value=translated.get(str(i),terms.get(s))
        if value is None:missing.append((i,s));return s
        if not isinstance(value,str) or not value.strip():raise ValueError(f'empty/non-string translation {i}')
        if protected(s)!=protected(value):raise ValueError(f'protected token mismatch at {i}: {s!r} -> {value!r}')
        assert_ascii(value, i)
        resolved.append((i,s,value))
        return value
    result=transform(data,sub)
    assert_quest_format(result)
    unknown=set(translated)-set(map(str,range(i+1)))
    if unknown:raise ValueError(f'unknown segment IDs: {unknown}')
    return result,missing,resolved

def main():
    files=sorted(SOURCE.rglob('*.json5'))
    current={str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    manifest=WORK/'source_manifest.json'
    if manifest.exists():
        if read_json(manifest,{})!=current:raise SystemExit('Source changed; reconcile with source_manifest.json before rebuilding.')
    else:dump(manifest,current)
    terms=read_json(WORK/'terms.json',{})
    command=sys.argv[1] if len(sys.argv)>1 else 'status'
    if command=='show':
        s=segments(load_source(SOURCE/sys.argv[2]));start=int(sys.argv[3]) if len(sys.argv)>3 else 0;end=int(sys.argv[4]) if len(sys.argv)>4 else len(s)
        print(f'{sys.argv[2]}: {len(s)} text segments')
        for i in range(start,min(end,len(s))):print(f'{i:04d}\t{s[i]}')
        return
    reward_source=read_json(WORK/'reward_labels_source.json',{})
    reward_translation=read_json(WORK/'reward_labels_zh_cn.json',{})
    if reward_source:
        live_en=load_source(ROOT/'.minecraft/kubejs/assets/ftb/lang/en_us.json')
        if any(live_en.get(k)!=v for k,v in reward_source.items()):
            raise ValueError('Reward-label English source changed')
        if reward_source.keys()!=reward_translation.keys():raise ValueError('Reward-label coverage mismatch')
        for k,v in reward_translation.items():
            assert_ascii(v, k)
            if protected(v)!=protected(reward_source[k]):raise ValueError(f'Reward placeholder changed: {k}')
        if command=='build':
            overlay=ROOT/'.minecraft/kubejs/assets/ftb/lang/zh_cn.json'
            existing=read_json(overlay,{})
            existing.update(reward_translation)
            dump(overlay,existing)
    names=read_json(WORK/'quest_item_names.json',{})
    if names:
        with zipfile.ZipFile(ROOT/names['source_jar']) as archive:
            name_source=json.loads(archive.read(names['language_file']))
        for k,entry in names['entries'].items():
            assert_ascii(entry['zh'], k)
            if name_source.get(k)!=entry['en']:raise ValueError(f'Quest-name source changed: {k}')
            if protected(entry['en'])!=protected(entry['zh']):raise ValueError(f'Quest-name format changed: {k}')
        if command=='build':
            overlay=ROOT/'.minecraft/kubejs/assets/ftb/lang/zh_cn.json'
            existing=read_json(overlay,{})
            existing.update({k:v['zh'] for k,v in names['entries'].items()})
            dump(overlay,existing)
    extra_labels=read_json(WORK/'quest_extra_labels.json',[])
    for group in extra_labels:
        source=ROOT/group['source']
        if hashlib.sha256(source.read_bytes()).hexdigest()!=group['source_sha256']:
            raise ValueError(f'Quest supplementary source changed: {source}')
        original=load_source(source)
        overlay=ROOT/group['target']
        existing=read_json(overlay,{})
        for key,entry in group['entries'].items():
            if original.get(key)!=entry['en']:raise ValueError(f'Quest supplementary English changed: {key}')
            assert_ascii(entry['zh'], key)
            if protected(entry['en'])!=protected(entry['zh']):raise ValueError(f'Quest supplementary format changed: {key}')
            if command=='build':existing[key]=entry['zh']
            elif existing.get(key)!=entry['zh']:raise ValueError(f'Quest supplementary output missing or outdated: {key}')
        if command=='build':dump(overlay,existing)
    rows=[];totals=collections.Counter()
    for p in files:
        rel=p.relative_to(SOURCE);data=load_source(p)
        translated=read_json(WORK/'translations'/rel.with_suffix('.json'),{})
        result,missing,resolved=translate(data,translated,terms)
        complete=not missing
        dest=TARGET/rel
        if command=='build' and complete:dump(dest,result)
        if dest.exists():
            actual=load_source(dest)
            if actual!=result or not complete:raise ValueError(f'Outdated or incomplete output: {rel}')
            if list(actual)!=list(data):raise ValueError(f'Changed quest language keys: {rel}')
        rows.append(dict(file=str(rel),keys=len(data),segments=len(missing)+len(resolved),translated=len(resolved),complete=complete,installed=dest.exists()))
        totals.update(files=1,keys=len(data),segments=len(missing)+len(resolved),translated=len(resolved),complete=int(complete),installed=int(dest.exists()))
    report=dict(totals=dict(totals),files=rows)
    visible={f'chapters/{p.name}' for p in (SOURCE.parent.parent/'chapters').glob('*.json5')}
    visible_done=sum(row['complete'] for row in rows if row['file'] in visible)
    installed_keys=sum(row['keys'] for row in rows if row['installed'])
    report['visible_chapters']={'complete':visible_done,'total':len(visible)}
    report['installed_keys']=installed_keys
    if command in ('build','check'):
        dump(WORK/'reports/progress.json',report)
        lines=['# 当前任务书汉化进度','',
            f'目标：完成全部任务书。当前状态：{"文本翻译已覆盖，静态验收见reports/final-audit.md" if totals["complete"]==totals["files"] else "进行中，尚未完成"}。','',
            f'- 可见章节：{visible_done}/{len(visible)}。',
            f'- 完整中文文件：{totals["installed"]}/{totals["files"]}（含目录、奖励和额外章节文件）。',
            f'- 已安装文本键：{installed_keys}/{totals["keys"]}。',
            f'- 已解决文本片段：{totals["translated"]}/{totals["segments"]}（含已明确保留的专名）。',
            f'- 另有{len(reward_translation)}条奖励标签、{len(names.get("entries",{}))}条任务组件名称/描述及{sum(len(g["entries"]) for g in extra_labels)}条补充名称。',
            '- 文件结构与解析检查见reports；游戏内排版、悬停与链接点击尚未验收。','',
            '| 文件 | 文本键 | 已解决/总片段 | 已安装 |','|---|---:|---:|---|']
        lines += [f'| {row["file"]} | {row["keys"]} | {row["translated"]}/{row["segments"]} | {"是" if row["installed"] else "否"} |' for row in rows]
        (WORK/'PROGRESS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(report if command=='status' else report['totals'],ensure_ascii=False,indent=2))

if __name__=='__main__':main()
