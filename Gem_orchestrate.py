import os
from google import genai
from notion_client import Client

# Initialize clients using environment variables
notion = Client(auth=os.environ["NOTION_TOKEN"])
gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def process_notion_tasks():
    # Example: Query a database or page from Notion
    # database_id = "your_database_id"
    # response = notion.databases.query(database_id=database_id)
    
    # Generate content with Gemini
    result = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents="Summarize top priorities for today based on Notion notes."
    )
    print("Gemini Response:", result.text)

if __name__ == "__main__":
    process_notion_tasks()
