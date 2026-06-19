import os
from dotenv import load_dotenv

load_dotenv()

# We cache the instances so we don't reconnect on every node execution
_ollama_instance = None
_groq_instance = None

def get_llm():
    """
    Dynamically routes LLM requests to either local Ollama or cloud Groq
    based on the LLM_PROVIDER environment variable.
    """
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    
    if provider == "groq":
        global _groq_instance
        if _groq_instance is None:
            # We import here to keep dependencies clean if Groq isn't used
            try:
                from langchain_groq import ChatGroq # type: ignore
                
                # Check for API key
                api_key = os.getenv("GROQ_API_KEY")
                if not api_key:
                    raise ValueError("GROQ_API_KEY environment variable is not set. Please add it to your .env file.")
                    
                _groq_instance = ChatGroq(
                    temperature=0.0,
                    model="llama-3.1-8b-instant",
                    api_key=api_key,
                    max_retries=2
                )
            except ImportError:
                raise ImportError("langchain-groq is not installed. Run: pip install langchain-groq")
        return _groq_instance
        
    else:
        # Fallback to local Ollama
        global _ollama_instance
        if _ollama_instance is None:
            from langchain_ollama import OllamaLLM # type: ignore
            _ollama_instance = OllamaLLM(model="llama3", temperature=0.0)
        return _ollama_instance
