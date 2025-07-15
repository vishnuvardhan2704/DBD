import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

def get_gemini_api_key():
    key = os.getenv("GEMINI_API_KEY")
    return key

def get_gemini_reason(product_a, product_b):
    """
    Calls Gemini API to compare two products and return a sustainability reason.
    Falls back to a dummy response if no API key is set or on error.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        # Dummy fallback
        return f"{product_b['name']} is more sustainable than {product_a['name']} because it is organic, uses better packaging, and has a lower carbon footprint."
    try:
        genai.configure(api_key=api_key)
        prompt = f"Compare these two products for sustainability.\nProduct A: {product_a['name']}, {product_a.get('description', '')}\nProduct B: {product_b['name']}, {product_b.get('description', '')}\nWhich is greener and why? Give short answer."
        model = genai.GenerativeModel("gemini-2.0-flash") 
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error: {e}")
        return f"(Gemini API error, using dummy reason) {product_b['name']} is more sustainable than {product_a['name']}." 