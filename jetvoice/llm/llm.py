import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def simple_fallback_response(prompt):
    """Simple fallback when OpenAI API is not available"""
    prompt_lower = prompt.lower()
    
    if "hello" in prompt_lower or "hi" in prompt_lower:
        return "Hello! I'm your JetVoice assistant running on Jetson Nano. How can I help you?"
    elif "how are you" in prompt_lower:
        return "I'm running well on your Jetson Nano! How are you?"
    elif "what" in prompt_lower and "time" in prompt_lower:
        return "I don't have access to current time right now."
    elif "weather" in prompt_lower:
        return "I don't have access to weather data at the moment."
    elif "help" in prompt_lower:
        return "I'm JetVoice, your AI assistant running on Jetson Nano. I can chat with you and respond to your voice commands."
    elif "test" in prompt_lower:
        return "Test successful! Your JetVoice system is working perfectly on Jetson Nano."
    else:
        return f"I heard you say: '{prompt}'. I'm your voice assistant running locally on Jetson Nano!"

def ask_llm(prompt):
    """Main LLM function for Jetson Nano voice assistant"""
    
    # Try OpenAI if we have a real API key
    if api_key and api_key != "your_api_key_here":
        try:
            # Use getattr to avoid linter error, but this works for openai==0.28.1
            chat_completion = getattr(openai, "ChatCompletion")
            response = chat_completion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful voice assistant running on Jetson Nano. Keep responses brief and natural."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            print(f"[OpenAI Error]: {str(e)}")
            print("[LLM] Using local fallback...")
    
    # Use simple local fallback
    return simple_fallback_response(prompt)