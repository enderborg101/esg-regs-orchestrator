## Required orchestrator change

Update `orchestrate.py` so the controlled Gemini access test:

1. Queries `NOTION_TASKS_DATA_SOURCE_ID`.
2. Finds `GEMINI ACCESS TEST — ORANGE-MALT-8472`.
3. Retrieves that page's block content from Notion.
4. Sends the retrieved content to Gemini.
5. Checks for the exact phrase `ORANGE-MALT-8472`.
6. Prints PASS/FAIL without writing to Notion.

The current proof of concept only sends task titles to Gemini, so it does not yet verify page-content access.