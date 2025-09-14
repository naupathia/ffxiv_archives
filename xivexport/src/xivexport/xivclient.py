from pprint import pp
from pydantic import ValidationError, BaseModel
from . import _scrub
import urllib
import httpx
from . import model
import asyncio
from typing import AsyncIterator, Iterator, List, Dict, Any, Optional, Type

# Language constants
ENGLISH_LANG = "en"
LANGUAGES = [ENGLISH_LANG]
API_URL = "https://v2.xivapi.com/api"



# Define xivapy models for FFXIV data types
class XivModel(BaseModel):
    """Base model for XIV API usage"""

    row_id: int
    __sheetname__: str = None

    @classmethod
    def get_sheet_name(cls) -> str:
        """Returns the sheet name, defaulting to the class name if __sheetname__ not set."""
        if cls.__sheetname__:
            return cls.__sheetname__
        return cls.__name__

    @classmethod
    def get_fields_str(cls):
        return ",".join(cls.model_fields.keys())


class ENpcResident(BaseModel):
    """NPC model for xivapy"""

    Singular: str


class ExVersion(BaseModel):
    """Expansion model for xivapy"""

    Name: str


class PlaceName(BaseModel):
    """PlaceName model for xivapy"""

    Name: str


class JournalCategory(BaseModel):
    """JournalCategory model for xivapy"""

    Name: str


class JournalGenre(BaseModel):
    """JournalGenre model for xivapy"""

    Name: str


class ItemUICategory(BaseModel):
    """ItemUICategory model for xivapy"""

    Name: str = None


class PreviousQuest(BaseModel):
    """PreviousQuest model for xivapy"""

    Id: str = None
    Name: str = None


class Quest(XivModel):
    """Quest model for xivapy"""

    Id: str
    Name: str
    Expansion: ExVersion
    IssuerStart: ENpcResident
    PlaceName: PlaceName
    JournalGenre: JournalGenre
    PreviousQuest: List[PreviousQuest]


class Item(XivModel):
    """Item model for xivapy"""

    Name: str
    Description: str
    ItemUICategory: ItemUICategory


class Mount(XivModel):
    """Mount model for xivapy"""

    Singular: str


class MountTransient(XivModel):
    """MountTransient model for xivapy"""

    Description: str
    DescriptionEnhanced: str
    Tooltip: str


class FishParameter(XivModel):
    """Fish model for xivapy"""

    Text: str
    Item: Item


class Fate(XivModel):
    """Fate model for xivapy"""

    Name: str
    Description: str


class TripleTriadCard(XivModel):
    """TripleTriadCard model for xivapy"""

    Name: str
    Description: str


class Status(XivModel):
    """Status model for xivapy"""

    Name: str
    Description: str

class SheetParseData(XivModel):
    key: str
    Name: str
    Text: str
    expansion: str = None

class XivApiClient:
    """Wrapper for xivapy client to provide common FFXIV data access patterns"""

    _client: httpx.AsyncClient = None

    def __init__(
        self,
        base_url: str = "https://v2.xivapi.com",
        base_api_path: str = "/api",
        game_version: str = "latest",
        schema_version: Optional[str] = None,
        batch_size: int = 100,
    ):
        self.client = None
        self.base_url = base_url
        self.base_api_path = base_api_path
        self.game_version = game_version
        self.schema_version = schema_version
        self.batch_size = batch_size

    async def close(self) -> None:
        """Close the interior HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        transport = httpx.AsyncHTTPTransport(retries=3)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=10.0,
            transport=transport,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    def _flatten_item_data(self, data: Any) -> Any:
        """Extract and flatten row data from API response."""
        if not data:
            return None

        if isinstance(data, list):
            return [self._flatten_item_data(i) for i in data]

        if not isinstance(data, dict):
            return data

        if "fields" not in data:
            return data

        fields = data.get("fields", {})
        processed_data = {
            "row_id": data.get("row_id"),
            **{
                field_name: self._flatten_item_data(field_value)
                for field_name, field_value in fields.items()
            },
        }

        return processed_data

    async def _call_get_api(self, url, params = None) -> dict:
        """makes the async api call"""

        response = await self._client.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        return data

    def _process_sheet_rows[T: XivModel](
        self, data: dict, model_class: type[T] = None
    ) -> Iterator[T | dict]:

        for item_data in data.get("rows", []):
            if not item_data:
                continue

            processed_data = self._flatten_item_data(item_data)

            if model_class:                
                yield model_class.model_validate(processed_data)
            else:
                yield processed_data

    async def sheets(self) -> Iterator[str]:

        res = await self._call_get_api(f"{self.base_api_path}/sheet")

        return [
            row["name"]
            for row in res["sheets"]
        ]

    async def sheet[T: XivModel](
        self, model_class: type[T] | str, rows: Optional[List[int]] = None
    ) -> AsyncIterator[T | dict]:
        rows_param = ",".join(str(id) for id in rows) if rows else None

        is_model_query = not isinstance(model_class, str)
        sheet_name = (
            model_class.get_sheet_name()
            if is_model_query
            else urllib.parse.quote(model_class, safe="")
        )
        fields = model_class.get_fields_str() if is_model_query else "*"

        data = await self._call_get_api(
            f"{self.base_api_path}/sheet/{sheet_name}",
            params={"rows": rows_param, "fields": fields},
        )

        for item in self._process_sheet_rows(
            data, model_class if is_model_query else None
        ):
            yield item

    async def get_sheet_data_as_text(self, sheet_name, speaker_pos=3) -> str:

        sheet_rows = []

        async for item in self.sheet(sheet_name):
            sheet_rows.append(tuple(item.values()))

        return _scrub.parse_speaker_lines(sheet_rows, speaker_pos)

