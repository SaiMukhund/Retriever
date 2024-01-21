import os 
import json 
from transformers import AutoModel
from sentence_transformers import SentenceTransformer

class Embedder():

    def __init__(self,embedding_name,embedding_model_path):
        self.embedding_name=embedding_name
        self.embedding_model_path=embedding_model_path


    def get_embedding_model(self):

        if self.embedding_name.startswith("jina"):
            self.embedding_model=Autotokenizer.from_pretrained(self.embedding_model_path,trust_remote_code=True)
        elif self.embeddings_name.startswith("multilingual"):
            self.embedding_model = SentenceTransformer(self.embedding_model_path)

        if torch.cuda.is_available():
            self.embedding_model.to("cuda")
    def get_embeddings(self,text,is_query=False):
        if self.embedding_name.startswith("jina"):
            emmbeddings=self.embedding_model.encode([text],normalize_embeddings=True)[0].tolist()
        elif self.embeddings_name.startswith("multilingual"):
            if is_query:
                instruction="query"
            else:
                instruction="passage"
            emmbeddings=self.embedding_model.encode([f"{instruction} : {text}"],normalize_embeddings=True)[0].tolist()

        else:
            embeddings= [0]
        return embeddings        
