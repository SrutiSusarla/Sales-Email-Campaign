"""
List available Gemini models
"""

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {bool(api_key)}\n")

if not api_key:
    print("ERROR: No API key in .env file")
    exit(1)

# Initialize client
client = genai.Client(api_key=api_key)

print("Available models:\n")

try:
    models = client.models.list()
    for model in models:
        print(f"  - {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"    Methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"ERROR listing models: {e}")

# Test with gemini-2.5-flash
print("\n\nTesting with gemini-2.5-flash...")
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Research Mayo Clinic and provide: 1. CEO name 2. Industry 3. One recent news. Keep under 50 words."
    )
    print(f"SUCCESS:\n{response.text}")
except Exception as e:
    print(f"ERROR: {e}")
