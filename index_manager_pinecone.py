
from index_manager import IndexManager
from pinecone import Pinecone
from dotenv import load_dotenv
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings,VectorStoreIndex

import os


load_dotenv()


class IndexManagerPinecone(IndexManager):
    def __init__(self,embed_model,index_name):
        super().__init__(embed_model)
        pc = Pinecone(api_key = os.getenv('PINECONE_API_KEY'))
        self.pinecone_index = pc.Index(index_name)
        self.vector_store = PineconeVectorStore(pinecone_index = self.pinecone_index)
        self.storage_context = StorageContext.from_defaults(
             vector_store=self.vector_store
        )
    #create the index and store it in pinecone
    def create_index(self):
        self.documents = []
        self.create_documents_from_papers()
        Settings.chunk_size = 1024
        Settings.chunk_overlap = 50
        self.index = VectorStoreIndex.from_documents(
            self.documents,storage_context = self.storage_context, embed_model = self.embed_model
        )
        
    def retreive_index(self):
        return VectorStoreIndex.from_vector_store(vector_store=self.vector_store,embed_model = self.embed_model)
    
    
    def list_papers(self):
        for paper in self.papers:
            print(paper["title"])
    