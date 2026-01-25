from core.vector_store import VectorStoreManager
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from typing import List , Generator
from langchain_groq import ChatGroq
from config.settings import settings

RAG_PROMPT_TEMPLATE = """You are a helpful AI assistant. Use the following context to answer the user's question.
If the context doesn't contain relevant information, say so and provide what help you can.

Context:
{context}

Question: {question}

Answer"""

class RAGchain:

    def __init__(
        self , 
        vectorstoremanager : VectorStoreManager = None,
        model_name : str = None,
        temperature : float = None):

        self.vector_store = vectorstoremanager or VectorStoreManager()
        self.model_name = model_name or settings.LLM_MODEL 

        self.temperature = temperature or settings.LLM_TEMPERATURE
        self._llm = ChatGroq(
            model= self.model_name ,
            temperature= self.temperature,
            api_key= settings.GROQ_API_KEY
        )

        self._prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        self._output_parser = StrOutputParser()
    
    @property
    def llm(self) -> ChatGroq:
        """Get the LLM instance."""
        return self._llm
    
    @property
    def prompt(self) -> ChatPromptTemplate:
        """Get the prompt template."""
        return self._prompt
    
    @property
    def output_parser(self) -> StrOutputParser:

        return self._output_parser
    
    def _format_context(self, documents : List[Document]) -> str :

        if not documents:
            return "No relevant context found." 
        
        context_parts = []

        for index , doc in enumerate(documents , start= 1 ) :
            context_source = doc.metadata.get("source" , "Unknown")
            context_parts.append(f"[Document {index}] (Source: {context_source})\n{doc.page_content}")
        
        return "\n\n".join(context_parts)

    def retrieve(self, query: str, k: int = None) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: User's question
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
    
        if not self.vector_store .is_initialized:
            return []
        
        return self.vector_store.search(query, k=k)
    
    
    def retrieve_mmr(self, query: str, k: int = None) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: User's question
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
    
        if not self.vector_store .is_initialized:
            return []
        
        retriever = self.vector_store.get_mmr_retriever(k=k)
        top_k_documents = retriever.invoke(query)

        return top_k_documents

    def generate(self, query: str, context: str) -> str:
        """
        Generate a response given query and context.
        
        Args:
            query: User's question
            context: Retrieved context string
            
        Returns:
            Generated response
        """
        # Create the chain: prompt -> llm -> parser
        chain = self._prompt | self._llm | self._output_parser
        
        # Invoke the chain
        response = chain.invoke({
            "context": context,
            "question": query
        })

        return response
    
    def generate_stream(self, query: str, context: str) -> Generator[str, None, None]:
        """
        Generate a streaming response.
        
        Args:
            query: User's question
            context: Retrieved context string
            
        Yields:
            Response chunks as they're generated
        """
        # Create the chain
        chain = self._prompt | self._llm | self._output_parser
        
        # Stream the response
        for chunk in chain.stream({
            "context": context,
            "question": query
        }):
            yield chunk
    
    def query(self, question: str, k: int = None) -> dict:
        """
        Complete RAG pipeline: retrieve and generate.
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with 'answer', 'sources', and 'context'
        """
        # Step 1: Retrieve relevant documents
        documents = self.retrieve(question, k=k)
        
        # Step 2: Format context
        context = self._format_context(documents)
        
        # Step 3: Generate response
        answer = self.generate(question, context)
        
        # Extract sources
        sources = [doc.metadata.get("source", "Unknown") for doc in documents]
        
        return {
            "answer": answer,
            "sources": list(set(sources)),  # Unique sources
            "context": context,
            "documents": documents
        }
    
    def query_mmr(self, question: str, k: int = None) -> dict:
        """
        Complete RAG pipeline: retrieve and generate.
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with 'answer', 'sources', and 'context'
        """
        # Step 1: Retrieve relevant documents
        documents = self.retrieve_mmr(question, k=k)
        
        # Step 2: Format context
        context = self._format_context(documents)
        
        # Step 3: Generate response
        answer = self.generate(question, context)
        
        # Extract sources
        sources = [doc.metadata.get("source", "Unknown") for doc in documents]
        
        return {
            "answer": answer,
            "sources": list(set(sources)),  # Unique sources
            "context": context,
            "documents": documents
        }

    def query_stream(self, question: str, k: int = None) -> Generator[str, None, None]:
        """
        Complete RAG pipeline with streaming response.
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            
        Yields:
            Response chunks as they're generated
        """
        # Step 1: Retrieve relevant documents
        documents = self.retrieve(question, k=k)
        
        # Step 2: Format context
        context = self._format_context(documents)
        
        # Step 3: Stream response
        for chunk in self.generate_stream(question, context):
            yield chunk

    def query_stream_mmr(self, question: str, k: int = None) -> Generator[str, None, None]:
        """
        Complete RAG pipeline with streaming response.
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            
        Yields:
            Response chunks as they're generated
        """
        # Step 1: Retrieve relevant documents
        documents = self.retrieve_mmr(question, k=k)
        
        # Step 2: Format context
        context = self._format_context(documents)
        
        # Step 3: Stream response
        for chunk in self.generate_stream(question, context):
            yield chunk

    
    def get_document_summaries(self, query: str, k: int = 3) -> dict:
        """
        Get summaries of top-N relevant documents.
        
        Args:
            query: User's question
            k: Number of documents to summarize
            
        Returns:
            Dictionary with document summaries
        """
        if not self.vector_store.is_initialized:
            return {"summaries": [], "message": "No documents available"}
        
        # Retrieve top documents
        documents = self.vector_store.search(query, k=k)
        
        summaries = []
        
        for i, doc in enumerate(documents, 1):
            # Generate summary for each document
            summary_prompt = ChatPromptTemplate.from_template(
                "Summarize this document chunk in 2-3 sentences:\n\n{content}\n\nSummary:"
            )
            
            chain = summary_prompt | self._llm | self._output_parser
            summary = chain.invoke({"content": doc.page_content})
            
            summaries.append({
                "rank": i,
                "source": doc.metadata.get("source", "Unknown"),
                "summary": summary,
                "relevance_score": "High" if i <= 2 else "Medium"
            })
        
        return {
            "query": query,
            "summaries": summaries,
            "total_documents": len(summaries)
        }