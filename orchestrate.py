"""First Notion -> Gemini proof of concept.

This intentionally runs in read-only mode: it reads a small number of Notion tasks,
sends their titles to Gemini for prioritisation, and prints the result. It does not
write anything back to Notion until the task-property mapping has been verified.
"""
import os

from app.integrations.gemini import GeminiClient
from app.integrations.notion import NotionClient


def title_from_page(page: dict) -> str:
    properties = page.get("properties", {})
    for prop in properties.values():
        if prop.get("type") == "title":
            return "".join(item.get("plain_text", "") for item in prop.get("title", []))
    return "(untitled)"


def process_notion_tasks() -> None:
    data_source_id = os.environ["NOTION_TASKS_DATA_SOURCE_ID"]
    notion = NotionClient()
    gemini = GeminiClient()

    response = notion.query_data_source(data_source_id, page_size=10)
    pages = response.get("results", [])
    task_titles = [title_from_page(page) for page in pages]

    if not task_titles:
        print("No tasks returned from Notion.")
        return

    prompt = (
        "You are the research-support agent for ESG Regs. Review these current Notion "
        "tasks and identify the three that appear most useful to progress the project. "
        "Do not invent missing context and do not make regulatory determinations.\n\n"
        + "\n".join(f"- {title}" for title in task_titles)
    )
    result = gemini.generate(prompt)
    print(result)


if __name__ == "__main__":
    process_notion_tasks()
