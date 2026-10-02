import os
import time

from google import genai


TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


class GeminiClient:
    def __init__(self) -> None:
        api_key = os.environ["GEMINI_API_KEY"]
        self.client = genai.Client(api_key=api_key)
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        self.max_retries = int(os.getenv("GEMINI_MAX_RETRIES", "3"))
        self.base_delay = float(os.getenv("GEMINI_RETRY_BASE_DELAY", "2"))
        self.max_delay = float(os.getenv("GEMINI_RETRY_MAX_DELAY", "30"))

    def generate(self, prompt: str) -> str:
        attempt = 0
        while True:
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
                return response.text or ""
            except Exception as exc:
                status_code = getattr(exc, "status_code", None)
                if status_code not in TRANSIENT_STATUS_CODES or attempt >= self.max_retries:
                    raise RuntimeError(
                        f"Gemini request failed after {attempt + 1} attempt(s) "
                        f"with status {status_code or 'unknown'}"
                    ) from exc

                delay = min(self.base_delay * (2**attempt), self.max_delay)
                retry_after = getattr(exc, "retry_after", None)
                if retry_after is not None:
                    try:
                        delay = min(float(retry_after), self.max_delay)
                    except (TypeError, ValueError):
                        pass

                attempt += 1
                print(
                    f"Gemini transient error (status {status_code}); "
                    f"retry {attempt}/{self.max_retries} in {delay:.1f}s"
                )
                time.sleep(delay)
