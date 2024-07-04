# Clean't up by Scruff

import re

def TokenMyzer(text, clean=False, Tarzan=False, concise=False, all=False):
    COMMON_WORDS = set("""a,an,the,is,are,was,were,can,am,has,been,be,of,and,it,in,to,for,on,at,by,as,or,if,but,so,yet""".split(','))

    if all:
        clean = Tarzan = concise = True

    if clean:
        text = re.sub(r'\s+', ' ', re.sub(r'[^\w\s.!?]', '', text)).lower().strip()
    
    if Tarzan:
        text = ' '.join([word for word in text.split() if word.lower() not in COMMON_WORDS])
    
    if concise:
        text += " Be concise."

    return text
