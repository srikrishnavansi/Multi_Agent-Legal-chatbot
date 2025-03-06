from collections import deque

class ConversationMemory:
    def __init__(self, max_history=5):
        self.history = deque(maxlen=max_history)
    
    def add_interaction(self, query, response):
        self.history.append({
            "query": query,
            "response": response
        })
    
    def get_context(self):
        context = []
        for interaction in self.history:
            context.append(f"User: {interaction['query']}")
            context.append(f"Assistant: {interaction['response']}")
        return "\n".join(context)
    
    def clear(self):
        self.history.clear()