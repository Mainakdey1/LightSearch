#document_store app

class Document_store:
    def __init__(self):
        self.documents = {}

    def add_document(self, doc_id : str, document : dict):
        self.documents[doc_id] = document

    def get_document(self, doc_id : str):
        return self.documents.get(doc_id, None)
    
    def all_documents(self):
        return self.documents
    
    