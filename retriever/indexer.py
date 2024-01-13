import os 
import json 
import uuid 
from tqdm import tqdm 
import chromadb
from chromadb.config  import Settings

from embedder import Embedder

class Indexer(Embedder):
    def __init__(self,database_directory,collection_name,embedding_name,embedding_model_path):
        self.database_directory=database_directory
        self.collection_name=collection_name
        super().__init__(embedding_name,embedding_model_path)
        self.client=chromadb.Persistclient(path=self.database_directory,settings=(Settings(anonymized_telemetry=False)))
        self.collection=self.client.create_collection(self.collection_name)
    
    def index(self,documents):
        embeddings=[]
        for doc in tqdm(documents):
            embeddings.append(self.get_embeddings(doc.page_content))
        for doc,doc_embeddings in tqdm(zip(documents,embeddings)):
            self.collection.add(
                documents=[doc.page_content],
                embeddings=[doc_embeddings],
                metadatas=doc.metadata,
                ids=[str(uuid.uuid1)]
            )
        
