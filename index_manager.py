#create classes form thr logic in other to be able to reuse them.

from tools import fetch_arxiv_papers
from llama_index.core import Document,Settings,VectorStoreIndex
from llama_index.core import StorageContext,load_index_from_storage

class IndexManager:
    def __init__(self,embed_model):   #the constructor takes an embedding model as an argument
        self.embed_model = embed_model
        self.papers = []


    def fetch_papers(self, topic, paper_count:10):
        self.papers = fetch_arxiv_papers(topic, paper_count)
    
    
    def create_documents_from_papers(self):  
        for paper in self.papers: 
            content = (
                f'Title: {paper["title"]}\n'
                f'Authors: {", ".join(paper["authors"])}\n'
                f'summary: {paper["summary"]}\n'
                f'Published: {paper["published"]}\n'
                f'journal_ref: {paper["journal_ref"]}\n'
                f'ODOI: {paper["doi"]}\n'
                f'Primary Category: {paper["primary_category"]}\n'
                f'categories: {", ".join(paper["categories"])}\n'
                f'PDF url: {paper["pdf_url"]}\n'
                f'arxiv url: {paper["arxiv_url"]}\n'
            )
            self.documents.append(Document(text = content))


    def create_index(self):
        self.documents = []
        self.create_documents_from_papers()
        Settings.chunk_size = 1024
        Settings.chunk_overlap = 50
        self.index = VectorStoreIndex.from_documents(
            self.documents, embed_model = self.embed_model
        )
    
    def retreive_index(self):
        storage_context = StorageContext.from_defaults(persist_dir='index/')
        return load_index_from_storage(storage_context, embed_model=self.embed_model)

    #print the titles of the papers
    def list_papers(self):
        print([paper["title"] for paper in self.papers])
    