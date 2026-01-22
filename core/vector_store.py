from core.embeddings import EmbeddingManager
from config.settings import settings
from typing import Optional , List 
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
import os 

class VectorStoreManager:
    
    """
    Manages FAISS vector store operations for semantic search.
    
    This class handles the creation, initialization, and management of a FAISS
    vector database for storing and retrieving document embeddings.
    
    Attributes:
        embedding_manager (EmbeddingManager): Manages text embeddings
        vector_store (Optional[FAISS]): The FAISS vector store instance
        index_path (str): File path for saving/loading the vector store

    """
    
    def __init__(self ,embedding_manager : EmbeddingManager = None):

        self.embedding_manager = embedding_manager or EmbeddingManager()

        self._vector_store : Optional[FAISS] = None
        
        self.index_path : str = settings.FAISS_INDEX_PATH

    
    @property
    def vector_store(self) -> Optional[FAISS]:
        """
        Get the FAISS vector store instance.
        
        Returns:
            Optional[FAISS]: The FAISS vector store instance if initialized, 
                None otherwise.
        """
        return self._vector_store

    @property
    def is_initialized(self) -> bool:
        """
            Check if the vector store has been initialized with documents.
            
            Returns:
                bool: True if vector store contains documents, False otherwise.
        """
        return self._vector_store is not None
    
    def create_from_documents(self , documents :List[Document] ) -> FAISS :
        """
        Create a new FAISS vector store from a list of documents.
        
        This method initializes the vector store by converting documents into 
        embeddings and indexing them in FAISS. Any existing vector store will 
        be replaced.
        
        Args:
            documents (List[Document]): A list of LangChain Document objects 
                to be indexed. Each document should contain text in the 
                page_content field.
                
        Returns:
            FAISS: The newly created FAISS vector store instance.
            
        Raises:
            ValueError: If documents list is empty.
        """
        self._vector_store = FAISS.from_documents(
            documents= documents,
            embedding= self.embedding_manager.embeddings
        )

        return self._vector_store
    

    def add_documents(self , documents :List[Document] ) -> FAISS :
        """
            Add documents to the vector store.
            Creates new store if not initialized.
            
            Args:
                documents: List of Document objects to add
                
            Returns:
                FAISS vector store instance
        """
        if not self.is_initialized :
            self._vector_store = self.create_from_documents(documents)
        else:
            self._vector_store.add_documents(documents)
        
        return self._vector_store
    
    def search(self,query: str,k: int = None) -> List[Document]:
        """
            Search for similar documents.
            
            Args:
                query: Search query text
                k: Number of results to return (default from settings)
                
            Returns:
                List of similar Document objects
                
            Raises:
                ValueError: If vector store is not initialized
        """
        if not self.is_initialized:
            raise ValueError("Vector store is not initialized. Add documents first.")
        
        k = k or settings.TOP_K_RESULTS

        return self._vector_store.similarity_search(
            query=query,
            k=k
            )
    def search_with_scores(self, query: str,k: int = None) -> List[tuple]:
        """
        Search for similar documents with relevance scores.
        
        Args:
            query: Search query text
            k: Number of results to return
            
        Returns:
            List of (Document, score) tuples
        """
        if not self.is_initialized:
            raise ValueError("Vector store is not initialized. Add documents first.")
        
        k = k or settings.TOP_K_RESULTS
        return self._vector_store.similarity_search_with_score(query, k=k)
    
    def get_retriever(self, k: int = None) -> VectorStoreRetriever:
        """
            Get a similarity-based retriever interface for the vector store.
        
            This retriever uses cosine similarity to find the most relevant documents.
            It's compatible with LangChain chains and can be used in RAG pipelines.
            
            Args:
                k (int, optional): Number of documents to retrieve. Defaults to 
                    settings.TOP_K_RESULT if not provided.
                    
            Returns:
                VectorStoreRetriever: A retriever object that can be used with 
                    LangChain chains for document retrieval.
                
            Raises:
                ValueError: If vector store is not initialized.
        """
        if not self.is_initialized:
            raise ValueError("Vector store is not initialized.")
        
        k = k or settings.TOP_K_RESULTS
        return self._vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def get_mmr_retriever(self, k: int = None ,lambda_mult :float = 0.5 ) -> VectorStoreRetriever:
        """
            Get an MMR-based retriever interface for the vector store.
            
            MMR (Maximal Marginal Relevance) retriever provides diverse results by 
            balancing relevance with diversity. This helps avoid redundant documents 
            in the results.
            
            Args:
                k (int, optional): Number of documents to retrieve. Defaults to 
                    settings.TOP_K_RESULTS if not provided.
                    
            Returns:
                VectorStoreRetriever: A retriever object using MMR algorithm that 
                    can be used with LangChain chains.
                    
            Raises:
                ValueError: If vector store is not initialized.
        
        """
        if not self.is_initialized:
            raise ValueError("Vector store is not initialized.")
        
        k = k or settings.TOP_K_RESULTS
        return self._vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": k , "lambda_mult": lambda_mult}
        )
    
    def save(self, path: str = None) -> None:
        """
        Save vector store to disk.
        
        Args:
            path: Directory path to save (default from settings)
        """
        if not self.is_initialized:
            raise ValueError("Vector store is not initialized. Nothing to save.")
        
        save_path = path or self.index_path
        os.makedirs(save_path , exist_ok= True)
        self._vector_store.save_local(save_path )
    
    def load(self, path: str = None) -> FAISS:
        """
        Load vector store from disk.
        
        Args:
            path: Directory path to load from (default from settings)
            
        Returns:
            Loaded FAISS vector store
        """
        load_path = path or self.index_path
        if not os.path.exists(load_path) :
            raise FileNotFoundError(f"No saved index found at {load_path}")
        self._vector_store = FAISS.load_local(
            load_path ,
            embeddings= self.embedding_manager.embeddings,
            allow_dangerous_deserialization= True
        )
        return self._vector_store
    
    def clear(self) -> None:
        """Clear the vector store from memory."""
        self._vector_store = None