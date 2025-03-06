from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class SummarizationAgent:
   
    def __init__(self, api_key):
        self.llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.5,
            google_api_key=api_key
        )
    
    
        # Initial query prompt template
        self.initial_prompt = PromptTemplate(
            input_variables=["query", "context"],
            template="""
            You are a helpful legal assistant that explains complex legal concepts in simple terms.
            
            User Query: {query}
            Relevant Information: {context}
            
            Instructions:
            - Provide a single, concise paragraph (2-3 sentences maximum)
            - List only the main steps or key points
            - End with "Would you like more details on any step?"
            
            Response:
            """
        )
        
        # Detailed explanation prompt template
        self.detailed_prompt = PromptTemplate(
            input_variables=["query", "context", "conversation_history"],
            template="""
            You are a helpful legal assistant that provides comprehensive legal explanations.
            
            Previous conversation context:
            {conversation_history}
            
            User Query: {query}
            Relevant Information: {context}
            
            Instructions for detailed response:
            1. Provide a comprehensive explanation of the legal process
            2. Break down each step with specific details:
               - Requirements and documentation
               - Relevant authorities or offices involved
               - Typical timeframes
               - Common challenges and solutions
               - Important considerations
            3. Use clear examples where appropriate
            4. Explain any technical terms
            5. Include practical tips and best practices
            
            Format the response with proper headings and bullet points for readability.
            Do NOT end with "Would you like more details?"
            
            Response:
            """
        )
        
        self.initial_chain = LLMChain(llm=self.llm, prompt=self.initial_prompt)
        self.detailed_chain = LLMChain(llm=self.llm, prompt=self.detailed_prompt)
    
    def is_detailed_request(self, query):
        """Check if the query is asking for more details"""
        detail_indicators = [
            'explain', 'detail', 'tell me more', 'elaborate', 
            'specific', 'how exactly', 'what exactly', 'more about',
            'step by step', 'break down', 'in depth'
        ]
        return any(indicator in query.lower() for indicator in detail_indicators)
    
    def summarize(self, query, context, conversation_history=""):
        """
        Generate an appropriate response based on whether it's an initial query
        or a request for more details
        """
        try:
            # Determine if this is a request for detailed information
            if self.is_detailed_request(query):
                # Use the detailed prompt
                response = self.detailed_chain.run({
                    "query": query,
                    "context": context,
                    "conversation_history": conversation_history
                })
            else:
                # Use the initial prompt
                response = self.initial_chain.run({
                    "query": query,
                    "context": context
                })
            
            # Clean up the response
            response = response.strip()
            
            return response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"