

from typing import List
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader , TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings

class DocumentProcessor:
    
    def __init__(self , chunk_size : int = None , chunk_overlap : int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n","\n"," ",""]
        )
    
    def load_document(self, file_path : str ) -> List[Document]:
        path = Path(file_path)
        extension = path.suffix.lower()

        if  extension == '.txt':
            loader = TextLoader(file_path=file_path ,  encoding="utf-8")
        elif  extension == '.pdf':
            loader = PyPDFLoader(file_path=file_path)
        else:
            raise ValueError(f'Unsupported file {extension} .Use .txt or pdf')
        
        return loader.load()
    
    def split_documents(self,documents : List[Document]) -> List[Document] :

        return self.text_splitter.split_documents(documents)
    
    def process(self , file_path :str ) -> List[Document]:

        documents = self.load_document(file_path)
        chunks = self.split_documents(documents)
        return chunks

