"""
Gemini Client - Wrapper for Google Gemini API (NEW package)
"""

from google import genai

class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-2.5-flash'
    
    def generate_email(self, prompt: str) -> str:
        """Generate content using Gemini"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
