"""Executable text syntax shared by localization validators.

Do not treat Markdown emphasis, prose punctuation, or arbitrary English words as
syntax. Replication's search DSL is enabled only for quest text.
"""
import collections
import re

PRINTF = re.compile(r'(?<![0-9])%(?:\d+\$)?[-#+0,(<]*\d*(?:\.\d+)?(?:[tT][HIklMSLNpzZsQBbhAaCYyjmdeRTrDFc]|[bBhHsScCdoxXeEfgGaA%n])')
MACRO = re.compile(r'\$\([^)]*\)|\$\{[^{}\n]+\}|\{\d+(?:,[^{}\n]+)?\}|\{\}')
COLOR = re.compile(r'(?:&(?!(?:amp|lt|gt|quot|apos|nbsp|#\d+|#x[0-9a-f]+);)|§)[0-9a-fk-orz]', re.I)
# Keep wildcard-bearing resource selectors intact, including tag prefixes.
RESOURCE_GLOB = re.compile(r'(?<![A-Za-z0-9_])#?[a-z][a-z0-9_]*:(?:[a-z0-9_./?\-]|\*(?!\*))+')
SEARCH = re.compile(r'(?<![A-Za-z0-9_])(?:[a-z][a-z0-9_]+(?:>=|<=|!=|>|<|=)\d+(?:\.\d+)?|[!*][a-z][a-z0-9_]*)(?![A-Za-z0-9_*])')

def printf_signature(text):
    automatic=0
    previous=None
    result=collections.Counter()
    for match in PRINTF.finditer(text):
        token=match.group()[1:]
        indexed=re.match(r'(\d+)\$',token)
        if indexed:
            argument=int(indexed[1]);token=token[indexed.end():]
        elif token in ('%', 'n'):
            argument=None
        elif '<' in token:
            argument=previous;token=token.replace('<','')
        else:
            automatic+=1;argument=automatic
        if argument is not None:previous=argument
        result[(argument,token)]+=1
    return result

def signature(text, *, quest=False):
    patterns = {'printf': PRINTF, 'macros': MACRO, 'colors': COLOR,
                'resource_globs': RESOURCE_GLOB}
    if quest:
        patterns['search_expressions'] = SEARCH
    result = {name: collections.Counter(pattern.findall(COLOR.sub('', text) if name == 'search_expressions' else text)) for name, pattern in patterns.items()}
    result['printf'] = printf_signature(text)
    return result

def assert_protected(source, target, context='', *, quest=False):
    left, right = signature(source, quest=quest), signature(target, quest=quest)
    differences = [name for name in left if left[name] != right[name]]
    if differences:
        raise ValueError(f'{context}: protected syntax differs: {differences}: {source!r} -> {target!r}')
