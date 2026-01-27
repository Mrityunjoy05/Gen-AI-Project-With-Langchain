from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver 
import sqlite3
import os
from config.settings import settings
from langchain_core.messages import HumanMessage , AIMessageChunk
from typing import List ,Generator
from langchain_core.tools import tool

class AgentManager:

    """
    Manages Langchain agent with memory and tools.
    
    Provides conversational agent with tool calling capabilities
    and persistent memory across conversations.
    """
    # Create the directory structure if it doesn't exist
    os.makedirs('data/database', exist_ok=True)

    def __init__(self , model_name : str = None):
        """
        Initialize agent manager.
        
        Args:
            model_name: LLM model name (defaults to settings.LLM_MODEL)
        """
        self.model_name = model_name or settings.LLM_MODEL

        self.llm : ChatGroq = ChatGroq(
            model= self.model_name,
            temperature= settings.LLM_TEMPERATURE,
            api_key= settings.GROQ_API_KEY,
            streaming=True
        )
        self._conn = sqlite3.connect(database="data/database/chatbot.db" , check_same_thread= False)
        self.checkpointer : SqliteSaver = SqliteSaver(conn=self._conn)
        self._agent = None

    @property
    def agent(self):

        """Get the agent instance."""
        return self._agent
    
    @property
    def is_initialized(self):
        """Check if agent has been initialized with tools."""
        return self._agent is not None
    

    def agent_initialization(self,tools :List[tool] , prompt : str = None):
        """
        Initialize agent with tools and system prompt.
        
        Args:
            tools: List of tools the agent can use
            prompt: System prompt for agent behavior
            
        Returns:
            Initialized agent
        """
        prompt = prompt or "You are a helpful AI assistant"
        self._agent = create_agent(
            model=self.llm ,
            tools=tools,
            system_prompt=prompt,
            checkpointer= self.checkpointer
        )

        
        return self._agent
    
    def get_response(self,query :str, thread_id :str) -> str:
        """
        Get non-streaming response from agent.
        
        Args:
            query: User's question
            thread_id: Thread ID for conversation memory
            
        Returns:
            Agent's response text
            
        Raises:
            ValueError: If agent is not initialized
        """

        if not self.is_initialized :
            raise ValueError("Agent is not initialized. Call agent_initialization() first.")
        
        config={"configurable": {"thread_id": thread_id}}

        response = self._agent.invoke({"messages": [HumanMessage(content=query)]},config=config)

        result = response['messages'][-1].content

        return result
    
    def get_response_stream(self,query :str , thread_id :str) -> Generator[str, None, None]:

        """
        Get streaming response from agent.
        
        Args:
            query: User's question
            thread_id: Thread ID for conversation memory
            
        Yields:
            Response chunks as they're generated
            
        Raises:
            ValueError: If agent is not initialized
        """


        if not self.is_initialized:
            raise ValueError("Agent is not initialized. Call agent_initialization() first.")
        
        config={"configurable": {"thread_id": thread_id}}
    
        response = self._agent.stream({"messages": [HumanMessage(content=query)]},config=config , stream_mode='messages')

        for chunk in response:

            if isinstance(chunk[0] , AIMessageChunk) and chunk[0].content :

                yield chunk[0].content
    


