import re

def TokenMyzer(text, clean=False, Tarzan=False, concise=False, all=False):
    def load_common_words():
        common_words = """a,an,the,is,are,was,were,can,am,has,been,be,of,and,it,in,to,for,on,at,by,as,or,if,but,so,yet"""
        return set(word.strip().lower() for word in common_words.split(','))

    def preprocess_text(text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.!?]', '', text)
        return text.lower().strip()

    def remove_articles(text):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in COMMON_WORDS]
        return ' '.join(filtered_words)

    COMMON_WORDS = load_common_words()

    if all:
        clean = Tarzan = concise = True

    if clean:
        text = preprocess_text(text)
    
    if Tarzan:
        text = remove_articles(text)
    
    if concise:
        text += " Be concise."

    return text