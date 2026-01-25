
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    
    GROQ_API_KEY:str =os.getenv('GROQ_API_KEY')
    TAVILY_API_KEY:str =os.getenv('TAVILY_API_KEY')
    GOOGLE_API_KEY:str =os.getenv('GOOGLE_API_KEY')
    OPENWEATHER_API_KEY:str =os.getenv('OPENWEATHER_API_KEY')
    LLM_MODEL:str =os.getenv('LLM_MODEL')
    EMBEDDING_MODEL:str =os.getenv('EMBEDDING_MODEL')
    CHUNK_SIZE:int = int(os.getenv('CHUNK_SIZE'))
    CHUNK_OVERLAP: int = int(os.getenv('CHUNK_OVERLAP'))
    LLM_TEMPERATURE:float = float(os.getenv('LLM_TEMPERATURE'))
    FAISS_INDEX_PATH:str=os.getenv('FAISS_INDEX_PATH')
    TOP_K_RESULTS:int= int(os.getenv('TOP_K_RESULTS'))

    def validate(self) -> bool:

        if not self.GROQ_API_KEY :
            raise ValueError("GROQ API key is not set. Please add it to your .env file")
        
        if not self.TAVILY_API_KEY :
            raise ValueError("TAVILY API key is not set. Please add it to your .env file")

        return True


settings = Settings()