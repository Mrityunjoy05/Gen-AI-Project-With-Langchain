from core.agent import AgentManager
from tools.tools_for_chat import get_all_tools

# Initialize agent
agent_manager = AgentManager()

# Get tools
tools = get_all_tools()

# Initialize with tools
agent_manager.agent_initialization(
    tools=tools,
    prompt="You are a helpful AI assistant with web search capabilities."
)

# Get response
response = agent_manager.get_response(
    "What's the Latest news about the India vs New Zealand Series",
    thread_id="user_123"
)
print(response)
# Or streaming
print('Streaming Output : \n')
for chunk in agent_manager.get_response_stream(
    "Tell me about the Current Weather in Mumbai",
    thread_id="user_123"
):
    print(chunk, end="" ,flush=True)