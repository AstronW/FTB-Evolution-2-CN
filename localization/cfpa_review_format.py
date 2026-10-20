"""Protected-format checks for reviewed CFPA language resources."""
from protected_text import signature
import collections,re
from punctuation import normalize,assert_ascii
FORMAT=re.compile(r'%(?:(\d+)\$)?[-+#0,(]*\d*(?:\.\d+)?([a-zA-Z%])')

def format_signature(text):
    auto=0;out=[]
    for m in FORMAT.finditer(text):
        index,kind=m.groups()
        if kind=='%':out.append(('%','%'));continue
        if index is None:auto+=1;index=auto
        out.append((str(index),kind))
    return collections.Counter(out)

def invariant_errors(en,zh):
    errors=[]
    if not isinstance(zh,str) or not zh.strip():return ['empty translation']
    left,right=signature(en),signature(zh)
    labels={'printf':'printf placeholders','macros':'Patchouli controls',
            'colors':'format codes','resource_globs':'resource IDs'}
    errors.extend(labels[name] for name in left if left[name]!=right[name])
    try:assert_ascii(zh,'reviewed CFPA')
    except ValueError:errors.append('non-ASCII Chinese punctuation')
    if format_signature(en)!=format_signature(zh):errors.append('printf placeholders')
    if en.count('%')!=zh.count('%'):errors.append('percent count')
    for label,pattern in [
        ('format codes',r'(?:§|&)[0-9a-fk-or]'),
        ('resource IDs',r'(?<![A-Za-z0-9_])[a-z][a-z0-9_]*:[a-z0-9_./-]+'),
        ('URLs',r'https?://[^\s<>"\)]+'),
        ('Patchouli controls',r'\$\([^)]*\)'),
        ('literal line breaks',r'\\n'),
    ]:
        if collections.Counter(re.findall(pattern,en,re.I if label=='format codes' else 0))!=collections.Counter(re.findall(pattern,zh,re.I if label=='format codes' else 0)):
            errors.append(label)
    def numbers(text):
        text=FORMAT.sub('',text)
        text=re.sub(r'(?:[a-z][a-z0-9_]*:[a-z0-9_./-]+|https?://[^\s<>]+)','',text)
        values=re.findall(r'[+-]?\d+(?:[,.]\d+)*',text)
        return collections.Counter(re.sub(r',(?=\d{3}(?:\D|$))','',value) for value in values)
    if numbers(en)!=numbers(zh):errors.append('numbers')
    return errors
