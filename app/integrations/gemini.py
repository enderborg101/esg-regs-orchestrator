import os

from google import genai


class GeminiClient:
    def __init__(self) -> None:
        api_key = os.environ["GEMINI_API_KEY"]
        self.client = genai.Client(api_key=api_key)
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text or ""
