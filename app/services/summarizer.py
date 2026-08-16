import json
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize client gracefully to avoid crashing if GEMINI_API_KEY is missing
client = None
if os.environ.get("GEMINI_API_KEY"):
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Warning: Failed to initialize Gemini client: {e}")
else:
    print("Warning: GEMINI_API_KEY environment variable not set. Summarization will be disabled.")

def generate_summary(text: str) -> dict:
    """
    Generates a structured summary from the given text using Gemini.
    Returns a dictionary with 'tldr_bullets' (list) and 'eli5_summary' (str).
    """
    prompt = f"""
    Please analyze the following article text and provide a JSON response with two keys:
    1. 'tldr_bullets': A list of 3-5 key takeaways (strings).
    2. 'eli5_summary': A simple, easy-to-understand breakdown of the article (string).
    
    Article text:
    {text}
    """
    
    if not client:
        print("Gemini client not initialized. Missing API key?")
        return None
        
    try:
        # Using the fast and cost-effective flash-lite model with JSON mode enabled
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        result = json.loads(response.text)
        return {
            "tldr_bullets": result.get("tldr_bullets", []),
            "eli5_summary": result.get("eli5_summary", "")
        }
    except Exception as e:
        print(f"Generation error: {e}")
        return None
