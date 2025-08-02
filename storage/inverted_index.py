#inverted logic application
from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(list))

    def index_document(self, doc_id : str, text : str):
        tokens = text.split()
        for position, token in enumerate(tokens):
            self.index[token][doc_id].append(position)
    
    def lookup(self, term : str):
        return self.index.get(term, {})

    def all_terms(self):
        return self.index
