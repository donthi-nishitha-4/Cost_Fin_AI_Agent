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
                    
                model_name = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile").strip()
                if model_name in ["llama3", "llama2", "ollama", "mistral"]:
                    # Default to llama-3.3-70b-versatile if using Groq provider
                    model_name = "llama-3.3-70b-versatile"
                    
                _groq_instance = ChatGroq(
                    temperature=0.0,
                    model=model_name,
                    api_key=api_key,
                    max_retries=6
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
