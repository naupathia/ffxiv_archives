import requests
from pydantic import ValidationError, BaseModel
from . import _scrub
from ._tools import timeit, Timer
import urllib
import httpx
from pydantic.fields import FieldInfo
from typing import Iterator, List, Any, Optional

import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.INFO)

# Language constants
ENGLISH_LANG = "en"
LANGUAGES = [ENGLISH_LANG]
API_URL = "https://v2.xivapi.com/api"

CUTSCENE = "cut_scene"
CUSTOM = "custom"

def expansion_name_from_number(number: int):
    if number == 2:
        return "A Realm Reborn"
    if number == 3:
        return "Heavensward"
    if number == 4:
        return "Stormblood"
    if number == 5:
        return "Shadowbringers"
    if number == 6:
        return "Endwalker"
    if number == 7:
        return "Dawntrail"

    return ""


class QuestKey:
    def __init__(self, sheet_name: str):
        # example sheet name: quest/050/KinGzb011_05040
        tokens = sheet_name.split("/")
        self.folder = tokens[1]
        self.key = tokens[2]
        self.row_id = int(self.key.split("_")[1])


class CutsceneKey:
    def __init__(self, sheet_name: str):
        # example sheet name: cut_scene/034/VoiceMan_03401
        tokens = sheet_name.split("/")
        expansion = tokens[1]
        expansion_num = int(expansion[:2])

        self.key = tokens[2]
        self.row_id = int(self.key.split("_")[1])
        self.patch_num = f"{expansion_num}.{expansion[2]}"
        self.expansion = expansion_name_from_number(expansion_num)


class CustomTextKey:
    def __init__(self, sheet_name: str):
        # example sheet name: custom/009/RegYok6BreathBetween_00906
        tokens = sheet_name.split("/")

        self.key = tokens[2]
        self.row_id = int(tokens[1])


def get_field_names(field, field_info: FieldInfo):

    model_type = None
    list_type = ""
    if issubclass(field_info.annotation, BaseModel):
        model_type = field_info.annotation

    elif hasattr(field_info.annotation, "__args__"):
        base_type = field_info.annotation.__args__[0]
        if field_info.annotation.__name__ == "List":
            list_type = "[]"

        if issubclass(base_type, BaseModel):
            model_type = base_type

    if model_type:
        for child_field, child_field_info in model_type.model_fields.items():
            for fname in get_field_names(child_field, child_field_info):
                yield f"{field}{list_type}.{fname}"

    else:
        yield field


# Define xivapy models for FFXIV data types
class XivModel(BaseModel):
    """Base model for XIV API usage"""

    row_id: int
    __sheetname__: str = None
    __transient__: type = None

    @classmethod
    def get_sheet_name(cls) -> str:
        """Returns the sheet name, defaulting to the class name if __sheetname__ not set."""
        if cls.__sheetname__:
            return cls.__sheetname__
        return cls.__name__

    @classmethod
    def get_fields_str(cls):

        fields = []
        for field, field_info in cls.model_fields.items():
            fields.extend(get_field_names(field, field_info))

        return ",".join(fields)


class ENpcResident(BaseModel):
    """NPC model for xivapy"""

    Singular: Optional[str] = ""


class ExVersion(BaseModel):
    """Expansion model for xivapy"""

    Name: str


class PlaceName(BaseModel):
    """PlaceName model for xivapy"""

    Name: Optional[str] = ""


class JournalCategory(BaseModel):
    """JournalCategory model for xivapy"""

    Name: Optional[str] = ""


class JournalGenre(BaseModel):
    """JournalGenre model for xivapy"""

    Name: Optional[str] = ""


class ItemUICategory(BaseModel):
    """ItemUICategory model for xivapy"""

    Name: Optional[str] = ""


class PreviousQuest(BaseModel):
    """PreviousQuest model for xivapy"""

    Id: Optional[str] = ""
    Name: Optional[str] = ""


class Quest(XivModel):
    """Quest model for xivapy"""

    Id: str
    Name: Optional[str] = ""
    Expansion: ExVersion
    IssuerStart: Optional[ENpcResident]
    PlaceName: Optional[PlaceName]
    JournalGenre: Optional[JournalGenre]
    PreviousQuest: List[PreviousQuest]
    Text: Optional[str] = None


class Item(XivModel):
    """Item model for xivapy"""

    Name: str
    Description: Optional[str] = ""
    ItemUICategory: ItemUICategory


class MountTransient(XivModel):
    """MountTransient model for xivapy"""

    Description: str
    DescriptionEnhanced: str
    Tooltip: str


class Mount(XivModel):
    """Mount model for xivapy"""

    Singular: str
    Description: Optional[str] = ""
    DescriptionEnhanced: Optional[str] = ""
    Tooltip: Optional[str] = ""

    __transient__ = MountTransient


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
    expansion: Optional[str] = None

    __speakerpos__: int = 3

    @staticmethod
    def from_sheet_and_text(sheetname, text):
        pass

    @classmethod
    def get_speaker(cls, text):
        return _scrub.get_speaker(text, cls.__speakerpos__)


class CustomText(SheetParseData):
    __sheetname__: str = CUSTOM

    @staticmethod
    def from_sheet_and_text(sheetname, text):
        keydef = CustomTextKey(sheetname)
        return CustomText(
            row_id=keydef.row_id, key=keydef.key, Text=text, Name=keydef.key
        )


class CutsceneText(SheetParseData):
    __sheetname__: str = CUTSCENE
    __speakerpos__: int = 4

    @staticmethod
    def from_sheet_and_text(sheetname, text):
        keydef = CutsceneKey(sheetname)
        return CutsceneText(
            row_id=keydef.row_id,
            key=keydef.key,
            Text=text,
            Name=f"{keydef.patch_num} {keydef.expansion} Cutscenes [{keydef.key}]",
            expansion=keydef.expansion,
        )

    @classmethod
    def get_speaker(cls, text):
        return _scrub.get_speaker(text, cls.__speakerpos__)

class XivApiClient:
    """Wrapper for xivapi calls to provide common FFXIV data access patterns"""

    _client: httpx.Client = None

    def __init__(self):
        self.base_url: str = "https://v2.xivapi.com"
        self.base_api_path: str = "/api"
        self.game_version: str = "latest"
        self._client = httpx.Client(base_url=self.base_url, timeout=30)

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def close(self):
        self._client.close()
        self._client = None

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

        transient_fields = data.get("transient", {})
        if transient_fields:
            for field_name in transient_fields:
                processed_data[field_name] = transient_fields[field_name]

        return processed_data

    def _call_get_api(self, url, params=None) -> dict:
        """makes the async api call"""

        LOGGER.debug(f'calling api {url}, params {params}')

        response = self._client.get(f"{self.base_api_path}/{url}", params=params)
        response.raise_for_status()

        data = response.json()
        return data

    def _process_sheet_rows[T: XivModel](
        self, data: list, model_class: type[T] = None
    ) -> Iterator[T | dict]:

        for item_data in data:
            if not item_data:
                continue

            processed_data = self._flatten_item_data(item_data)

            if model_class:
                try:
                    yield model_class.model_validate(processed_data)
                    LOGGER.info(f"Processed {model_class.__name__} sheet data for {processed_data.get("row_id")}")
                except ValidationError as e:
                    row_id = item_data.get("row_id")
                    LOGGER.error(f"Error with model for {model_class.__name__} {row_id}. Skipping.")
                    LOGGER.debug(f'Error detail:', exc_info=e)
            else:
                yield processed_data

    def sheets(self) -> List[str]:

        res = self._call_get_api(f"sheet")

        return [row["name"] for row in res["sheets"]]

    def sheet[T: XivModel](
        self, model_class: type[T] | str, rows: Optional[List[int]] = None
    ) -> Iterator[T | dict]:
        rows_param = ",".join(str(id) for id in rows) if rows else None

        is_model_query = not isinstance(model_class, str)
        sheet_name = (
            model_class.get_sheet_name()
            if is_model_query
            else urllib.parse.quote(model_class, safe="")
        )
        fields = model_class.get_fields_str() if is_model_query else "*"
        transient_fields = None
        if is_model_query and model_class.__transient__:
            transient_fields = model_class.__transient__.get_fields_str()

        params = {
            "fields": fields,
            "transient": transient_fields,
            "limit": 500,
            "after": 0
        }
        start = 0
        limit = 500  # xivapi max limit
        has_more = True
        prev_results = None

        while has_more:

            params["after"] = start

            data = self._call_get_api(
                f"sheet/{sheet_name}",
                params=params,
            )
            rows = data.get("rows", [])

            if not rows:
                break

            if prev_results and prev_results[0]["row_id"] == rows[0]["row_id"]:
                raise "Received same API response"

            for item in self._process_sheet_rows(
                rows, model_class if is_model_query else None
            ):
                yield item

            if len(rows) < limit:
                has_more = False

            # use last row_id as the start of next batch
            start = rows[-1]["row_id"]
            prev_results = rows


    def get_sheet_data_as_text(self, sheet_name, get_speaker_func) -> str:

        sheet_rows = []

        for item in self.sheet(sheet_name):
            sheet_rows.append(tuple(item.values()))

        return _scrub.parse_speaker_lines(sheet_rows, get_speaker_func)

    def search[T: XivModel](self, model_class: type[T], query) -> Iterator[T]:

        data = self._call_get_api(
            "search",
            {
                "query": query,
                "sheets": model_class.__name__,
                "fields": model_class.get_fields_str(),
            },
        )

        rows = data.get("results", [])

        for item in self._process_sheet_rows(rows, model_class):
            yield item

    def search_one[T: XivModel](self, model_class: type[T], query) -> T | None:

        for item in self.search(model_class, query):
            return item


class XivApiClientManager:
    client: XivApiClient = None

    @classmethod
    def connect(cls):
        cls.client = XivApiClient()

    @classmethod
    def close(cls):
        cls.client.close()


class XivDataAccess:
    _sheets: dict = None

    @classmethod
    def client(cls):
        return XivApiClientManager.client

    @classmethod
    def get_all(cls, model_class, row=None):
        if model_class == Quest:
            return cls._get_quests(row)

        elif issubclass(model_class, SheetParseData):
            return cls._get_sheet_text_data(model_class, row)

        return cls.client().sheet(model_class, [row] if row else None)

    @classmethod
    def get_sheet_names(cls, name):
        """
        Gets the sheet names that start with 'name'
        """

        if not cls._sheets:
            with Timer("get_sheets"):
                cls._sheets = {"quest": [], CUSTOM: [], CUTSCENE: []}
                for sheet in cls.client().sheets():
                    if sheet.startswith("quest/"):
                        cls._sheets["quest"].append(sheet)
                    if sheet.startswith("custom/"):
                        cls._sheets[CUSTOM].append(sheet)
                    if sheet.startswith("cut_scene/"):
                        cls._sheets[CUTSCENE].append(sheet)

        return cls._sheets[name]

    @classmethod
    def _get_sheet_text_data(cls, model_class: type[SheetParseData], rows=None):
        count = 0
        LOGGER.debug(f'loading data for {model_class.__name__}')
        for sheet_name in cls.get_sheet_names(model_class.__sheetname__):

            # the sheet data will be the quest text
            text = cls.client().get_sheet_data_as_text(sheet_name, lambda s: model_class.get_speaker(s))

            yield model_class.from_sheet_and_text(sheet_name, text)

            count += 1
            if rows and count >= rows:
                break

    @classmethod
    def _get_quests(cls, rows=None):

        for quest_model in cls.client().sheet(Quest, [rows] if rows else None):

            # folder num is part of the key
            # example key: ChrHdy399_04784
            # folder:               |047|
            folder_num = quest_model.Id[-5:-2]
            sheet_name = f"quest/{folder_num}/{quest_model.Id}"
            # the sheet data will be the quest text
            quest_text = cls.client().get_sheet_data_as_text(sheet_name, _scrub.get_speaker)

            quest_model.Text = quest_text

            yield quest_model

