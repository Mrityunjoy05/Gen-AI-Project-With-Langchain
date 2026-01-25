from tools.tools_for_chat import get_all_tools

# Check tools
tools = get_all_tools()

print("Number of tools:", len(tools))
print("\nTool details:")
for tool in tools:
    print(f"  - Name: {tool.name}")
    print(f"    Description: {tool.description}")
    print()

# Expected output:
# Number of tools: 3
# 
# Tool details:
#   - Name: search_web_tavily
#     Description: Search the web using Tavily...
#   
#   - Name: search_web_duckduckgo
#     Description: Search the web using DuckDuckGo...
#   
#   - Name: calculate
#     Description: Evaluate a mathematical expression...