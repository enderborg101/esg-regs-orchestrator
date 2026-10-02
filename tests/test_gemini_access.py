from gemini_access_test import EXPECTED_PHRASE, rich_text_from_block, title_from_page


def test_title_from_page():
    page = {
        "properties": {
            "Name": {
                "type": "title",
                "title": [{"plain_text": "GEMINI ACCESS TEST v2 — ORANGE-MALT-8472"}],
            }
        }
    }
    assert title_from_page(page).endswith(EXPECTED_PHRASE)


def test_rich_text_from_block():
    block = {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"plain_text": "The phrase is ORANGE-MALT-8472."}]
        },
    }
    assert EXPECTED_PHRASE in rich_text_from_block(block)
