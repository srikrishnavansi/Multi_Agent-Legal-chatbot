from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class QueryAgent:
    def __init__(self, vector_store, api_key):
        self.vector_store = vector_store
        self.llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=api_key
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["query", "context"],
            template="""
            You are a legal information retrieval expert. Using the following context, 
            find the most relevant information to answer the user's query.
            
            Context: {context}
            
            Query: {query}
            
            Instructions:
            1. Focus on extracting only the key steps or main points
            2. Keep the initial response brief and actionable
            3. Prepare detailed information for follow-up questions
            4. If the context doesn't contain specific information, provide a general outline of the process
            
            Provide only the essential information needed for an initial response.
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def process_query(self, query):
        try:
            relevant_docs = self.vector_store.similarity_search(query, k=3)
            context = "\n".join([doc.page_content for doc in relevant_docs])
            
            if not context.strip():
                return "I apologize, but I couldn't find specific information about that in the legal documents. Would you like to try rephrasing your question?"
            
            response = self.chain.run({
                "query": query,
                "context": context
            })
            
            return response.strip()
            
        except Exception as e:
            return f"Error processing query: {str(e)}"