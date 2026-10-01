import os

from google import genai


class GeminiClient:
    def __init__(self) -> None:
        api_key = os.environ["GEMINI_API_KEY"]
        self.client = genai.Client(api_key=api_key)
        # Keep the model configurable so provider model changes do not require
        # code changes. The current default is the model recommended by the API
        # error returned to this project when the previous model was retired.
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text or ""
