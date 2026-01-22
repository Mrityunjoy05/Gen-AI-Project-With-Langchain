
from tools.tavily_search import TavilySearchTool 

tool = TavilySearchTool()

result = tool.search(query=' Tell me the latest news about AI ')
print("Result :- \n")
print(result)
result_with_context = tool.search_with_context(query=' Tell me the latest news about AI ')
print()
print("result_with_context :- \n")
print(result_with_context)