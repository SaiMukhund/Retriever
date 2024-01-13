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
    
    def retrieval(self,query,top_k=10,search_space=None):
        self.query_embeddings=self.get_embeddings(doc.page_content,True)

        if search_space is None:
            retrieved_docs=seelff.collection.query(
                query_embeddings=self.query_embeddings,
                n_results=top_k
            )
        else:
            retrieved_docs=seelff.collection.query(
                query_embeddings=self.query_embeddings,
                n_results=top_k,
                where=search_space
            )
        final_docs=[]

        for docs,metadatas,score in zip(retrieved_docs["documents"][0],retrieved_docs["metadatas"][0],retrieved_docs["distances"][0]):
            final_docs.append(
                {
                    "page_content":docs,
                    "metadata":metadatas,
                    "score":score
                }
            )
        return final_docs
    

        
