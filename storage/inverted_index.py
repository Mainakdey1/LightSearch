#inverted logic application
from collections import defaultdict
import math

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(int))
        self.doc_lengths = defaultdict(int)
        self.doc_freq = defaultdict(int)
        self.num_docs = 0

    def index_document(self, doc_id : str, tokens : list[str]):
        self.num_docs += 1
        seen_terms = set()
        for token in tokens:
            self.index[token][doc_id] += 1
            self.doc_lengths[doc_id] += 1
            if token not in self.doc_freq:
                self.doc_freq[token] += 1
                seen_terms.add(token)

    def compute_tfidf(self, term : str, doc_id : str):
        tf = self.index[term][doc_id] / self.doc_lengths[doc_id]
        idf = math.log((self.num_docs + 1) / (1 + self.doc_freq[term])) + 1
        return tf * idf

    def search(self, term : str):
        term = term.lower()
        if term not in self.index:
            return []
        scores = []
        for doc_id in self.index[term]:
            score = self.compute_tfidf(term, doc_id)
            scores.append((score, doc_id))
        scores.sort(reverse= True)
        return scores

    def all_terms(self):
        return self.index
