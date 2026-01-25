
from core.query_classifier import QueryClassifier

cl = QueryClassifier()

result = cl.classify(query="Tell me the what is the current  News about India vs New Zealand series")
print(result)