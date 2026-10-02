"""Single-request live test proving Notion page content reaches Gemini."""
import os
from typing import Any

from app.integrations.gemini import GeminiClient
from app.integrations.notion import NotionClient

TEST_TITLE = "GEMINI ACCESS TEST v2 — ORANGE-MALT-8472"
EXPECTED_PHRASE = "ORANGE-MALT-8472"


def title_from_page(page: dict[str, Any]) -> str:
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return "".join(item.get("plain_text", "") for item in prop.get("title", []))
    return "(untitled)"


def rich_text_from_block(block: dict[str, Any]) -> str:
    data = block.get(block.get("type", ""), {})
    return "".join(item.get("plain_text", "") for item in data.get("rich_text", []))


def page_text(notion: NotionClient, page_id: str) -> str:
    response = notion.client.blocks.children.list(block_id=page_id, page_size=100)
    return "\n".join(text for block in response.get("results", []) if (text := rich_text_from_block(block)))


def main() -> None:
    data_source_id = os.environ["NOTION_TASKS_DATA_SOURCE_ID"]
    notion = NotionClient()
    gemini = GeminiClient()

    response = notion.query_data_source(data_source_id, page_size=100)
    pages = response.get("results", [])
    page = next((p for p in pages if title_from_page(p) == TEST_TITLE), None)
    if page is None:
        raise RuntimeError(f"Test task not found: {TEST_TITLE}")

    content = page_text(notion, page["id"])
    if EXPECTED_PHRASE not in content:
        raise RuntimeError("Verification phrase was not retrieved from the Notion page content")

    print(f"Notion task found: {TEST_TITLE}")
    print(f"Notion content retrieved: {len(content)} characters")
    print("Submitting one controlled Gemini request...")

    prompt = (
        "You are running a controlled integration test. The following text was retrieved "
        "from a Notion task. Identify the exact verification phrase in the supplied text. "
        "Return the phrase exactly, followed by one short sentence confirming it was found.\n\n"
        f"NOTION TASK CONTENT:\n{content}"
    )
    result = gemini.generate(prompt)
    print("Gemini response received.")
    print(result)

    if EXPECTED_PHRASE not in result:
        raise RuntimeError("Gemini did not return the expected verification phrase")

    print("VERIFICATION: PASS — Notion content reached Gemini and was correctly interpreted.")


if __name__ == "__main__":
    main()
