import os
from typing import Any

from notion_client import Client


class NotionClient:
    def __init__(self) -> None:
        self.client = Client(auth=os.environ["NOTION_TOKEN"])

    def fetch_data_source(self, data_source_id: str) -> dict[str, Any]:
        return self.client.data_sources.retrieve(data_source_id=data_source_id)

    def query_data_source(self, data_source_id: str, **kwargs: Any) -> dict[str, Any]:
        return self.client.data_sources.query(data_source_id=data_source_id, **kwargs)

    def update_page(self, page_id: str, **kwargs: Any) -> dict[str, Any]:
        return self.client.pages.update(page_id=page_id, **kwargs)
