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

print('Streaming Output : \n')
for chunk in agent_manager.get_response_stream(
    "Can u tell me what i asked before",
    thread_id="user_123"
):
    print(chunk, end="" ,flush=True)