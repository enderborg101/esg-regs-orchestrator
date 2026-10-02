# Gemini access test

This test uses the Notion task named `GEMINI ACCESS TEST — ORANGE-MALT-8472`.

Expected verification phrase: `ORANGE-MALT-8472`.

The orchestrator should retrieve the task page content from Notion and pass that content to Gemini in one request. The workflow should then verify that Gemini returns the exact phrase.

No Notion write should be performed by this test.