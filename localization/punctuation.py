"""Shared punctuation policy for authored Chinese translations."""
import re
PUNCTUATION = str.maketrans({'，':',','。':'.','：':':','；':';','！':'!','？':'?','（':'(', '）':')','【':'[','】':']','“':'"','”':'"','‘':"'",'’':"'",'、':',','《':'"','》':'"','「':'"','」':'"','『':'"','』':'"'})
NON_ASCII_PUNCTUATION = re.compile(r'[，。：；！？（）【】“”‘’、》《「」『』]')
def normalize(text):
    text=text.translate(PUNCTUATION).replace('……','...').replace('——','--').replace('—','-')
    text=re.sub(r'(?<=[\u3400-\u9fff])([,:;])(?=\S)',r'\1 ',text)
    return re.sub(r'([&§][0-9a-fk-or])([,:;])(?=\S)',r'\1\2 ',text)
def assert_ascii(text, context):
    if NON_ASCII_PUNCTUATION.search(text):
        raise ValueError(f'Use ASCII punctuation in translation: {context}')
