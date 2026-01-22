from config.settings import settings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingManager:

    def __init__(self, model_name : str = None):
        
        self.model_name = model_name or settings.EMBEDDING_MODEL 
        # self._embeddings = GoogleGenerativeAIEmbeddings(
        #     model= self.model_name
        # )

        self._embeddings = HuggingFaceEmbeddings(
            model_name= self.model_name,
            model_kwargs={'device': 'cpu'} ,
            encode_kwargs={"normalize_embeddings": True} # Normalize for cosine similarity
        )

    @property
    def embeddings(self) -> HuggingFaceEmbeddings:
        return self._embeddings
    
