#tokenizer application

import re

def tokenize(text : str) -> list[str]:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)

    return text.split()
