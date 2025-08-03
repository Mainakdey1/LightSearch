#main fast api app
from storage.document_store import Document_store
from storage.inverted_index import InvertedIndex
from search.tokenizer import tokenize

doc_store = Document_store()
index = InvertedIndex()


def index_doc(doc_id : str, title : str, content : str):
    full_text = f'{title} {content}'
    tokens = tokenize(full_text)

    doc_store.add_document(doc_id, {"id" : doc_id, "title" : title, "content" : content})
    index.index_document(doc_id, tokens)

def search(term : str):
    results = index.search(term)
    return [doc_store.get_document(doc_id) for score, doc_id in results]

#---Test----
if __name__ == "__main__":
    index_doc("1", "Elasticsearch Basics", "Learn how it works")
    index_doc("2", "Search Engines", "Elasticsearch is fast and scalable")
    index_doc("3", "Full text search", "Search engines power modern apps")

    print("\nSearch results for 'elasticsearch':")
    for doc in search("elasticsearch"):
        print(doc)

    print("\nSearch results for 'search':")
    for doc in search("search"):
        print(doc)