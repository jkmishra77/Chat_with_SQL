from dotenv import load_dotenv
load_dotenv()

import os
import getpass
from langchain_groq import ChatGroq

def setup_llm():
    """
    Initialize and validate Groq LLM with API key authentication
    Returns: ChatGroq instance if successful, None if failed
    """
    # Check if API key is already set in environment
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("🔑 Groq API Key is required.")
        print("💡 Get your API key from: https://console.groq.com/api-keys")
        api_key = getpass.getpass("Enter your Groq API key (starts with gsk_): ")
        os.environ["GROQ_API_KEY"] = api_key
    
    
    try:
        # Initialize LLM with a simple model
        llm = ChatGroq(
            model_name="llama3-70b-8192",
            temperature=0.1,
              api_key=os.getenv("GROQ_API_KEY"),
            

        )
        
        # Test the API key with a simple request
        test_response = llm.invoke("Say hello in one word.")
        
        print("✅ Groq API authentication successful!")
        return llm
        
    except Exception as e:
        if "401" in str(e) or "Authentication" in str(e) or "Invalid API Key" in str(e):
            print("❌ Authentication failed: Invalid API Key")
            print("💡 Please check your API key at: https://console.groq.com/api-keys")
        elif "429" in str(e):
            print("❌ Rate limit exceeded: Too many requests")
            print("💡 Please wait a moment and try again")
        else:
            print(f"❌ Error initializing LLM: {e}")
        
        # Clear the invalid key from environment
        os.environ["GROQ_API_KEY"] = ""
        return None

# Optional: Test function
def test_llm():
    """Test function to verify LLM is working"""
    llm = setup_llm()
    if llm:
        try:
            response = llm.invoke("What is 2+2?")
            print(f"✅ LLM Test Response: {response.content}")
            return True
        except Exception as e:
            print(f"❌ LLM Test Failed: {e}")
            return False
    return False

if __name__ == "__main__":
    # Test the LLM setup when run directly
    print("🧪 Testing LLM setup...")
    if test_llm():
        print("🎉 LLM setup completed successfully!")
    else:
        print("❌ LLM setup failed. Please check your API key.")