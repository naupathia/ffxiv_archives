from pydantic import ValidationError, BaseModel
from ._tools import Timer
import urllib
import httpx
from pydantic.fields import FieldInfo
from typing import Iterator, List, Any, Optional, Type

import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.INFO)

# Language constants
ENGLISH_LANG = "en"
JAPANESE_LANG = "ja"
ALT_LANGUAGES = [JAPANESE_LANG]
API_URL = "https://v2.xivapi.com/api"

CUTSCENE = "cut_scene"
CUSTOM = "custom"
BATCH_SIZE = 500  # max api limit is 500


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


class SheetKey:
    def __init__(self, sheet_name: str):
        # example sheet name: cut_scene/034/VoiceMan_03401
        tokens = sheet_name.split("/")

        self.folder = tokens[1]
        self.key = tokens[2]
        self.row_id = int(self.key.split("_")[1])
        self.name = self.key
        self.expansion = None


class CutsceneKey(SheetKey):
    def __init__(self, sheet_name: str):
        super().__init__(sheet_name)
        # example sheet name: cut_scene/034/VoiceMan_03401
        expansion = self.folder
        expansion_num = int(expansion[:2])

        patch_num = f"{expansion_num}.{expansion[2]}"
        self.expansion = expansion_name_from_number(expansion_num)
        self.name = f"{patch_num} {self.expansion} Cutscenes"


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

    _japanese: Any

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
    JournalCategory: Optional["JournalCategory"]


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
    PlaceName: Optional["PlaceName"]
    JournalGenre: Optional["JournalGenre"]
    PreviousQuest: List["PreviousQuest"]

    _sheet_name: Optional[str] = None
    _sheet_rows: Optional[list] = []


class Item(XivModel):
    """Item model for xivapy"""

    Name: str
    Description: Optional[str] = ""
    # ItemUICategory: Optional[ItemUICategory] = None


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


class FateEvent(XivModel):
    Text: list


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
    """Represents sheet data from xivapi"""

    key: str
    Name: str

    _sheet_name: Optional[str] = None
    _sheet_rows: Optional[list] = []
    _expansion: Optional[str] = None
    __key_type__: Type = None

    @classmethod
    def from_sheet_and_text(cls, sheetname, text):
        keydef = cls.__key_type__(sheetname)
        result = cls(
            row_id=keydef.row_id,
            key=keydef.key,
            Name=keydef.name,
        )
        result._sheet_rows = text
        result._sheet_name = sheetname
        result._expansion = keydef.expansion

        return result


class AkatsukiNoteString(XivModel):
    Text: str


class NameField(BaseModel):
    Name: Optional[str] = None


class MYCWarResultNotebook(XivModel):
    Description: str
    Name: str
    Quest: Quest


class MKDLore(XivModel):
    Name: str
    Description: str


class VVDNotebookContents(XivModel):
    Name: str
    Description: str


class CustomTalk(XivModel):
    Name: Optional[str] = None
    MainOption: Optional[str] = None


class CustomText(SheetParseData):

    Name: Optional[str] = None
    Type: Optional[str] = None

    __sheetname__: str = CUSTOM
    __key_type__ = SheetKey


class CutsceneText(SheetParseData):
    __sheetname__: str = CUTSCENE
    __key_type__ = CutsceneKey


class Balloon(XivModel):
    Dialogue: str


class NpcYell(XivModel):
    Text: str


class EventIdData(BaseModel):
    Name: str


class LevelData(BaseModel):
    EventId: EventIdData = None


class Adventure(XivModel):
    Description: str
    Impression: str
    Level: LevelData
    PlaceName: PlaceName


class DescriptionString(BaseModel):
    Text: Optional[str] = None


class DescriptionPage(XivModel):
    subrow_id: Optional[int]
    Text: List[DescriptionString]


class WKSPioneeringTrailString(XivModel):
    DevelopmentLogName: str
    DevelopmentLogText: str
    DevelopmentLogDescription: str


class WKSMissionText(XivModel):
    Text: str


class SpearfishingItem(XivModel):
    Description: str
    Item: Item


class SnipeTalk(XivModel):
    Name: NameField
    Text: str


class CompanionTransient(XivModel):
    Description: str
    DescriptionEnhanced: str
    Tooltip: str


class Companion(XivModel):
    Singular: str
    Description: str
    DescriptionEnhanced: str
    Tooltip: str

    __transient__ = CompanionTransient


class Leve(XivModel):
    Description: str
    Name: str
    PlaceNameIssued: Optional[PlaceName]


class GimmickBill(XivModel):
    Text: str


class GimmickTalk(XivModel):
    Message: str


class XivApiClient:
    """Wrapper for xivapi calls to provide common FFXIV data access patterns"""

    _client: httpx.Client = None
    _sheets: dict = None
    batch_size = BATCH_SIZE

    def __init__(self):
        self.base_url: str = "https://v2.xivapi.com"
        self.base_api_path: str = "/api"
        self.game_version: str = "latest"
        self._client = httpx.Client(base_url=self.base_url, timeout=60)

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def close(self):
        self._client.close()
        self._client = None

    def _flatten_item_data(self, data: Any) -> Any:
        """Extract and flatten row data from API response.

        When reading data from a sheet that is text data, it will be in the form

        {
            "rows": [
                {
                    "row_id": 1,
                    "fields": {
                        "field1": "text",
                        "field2": "text2"
                }
            ]
        }

        This function will "flatten" the dictionary into simple row data:

        [
            {
                "row_id": 1,
                "field1": "text",
                "field2": "text2"
            }
        ]

        It will also extract any "transient" fields lined to add them to the data returned.

        """
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

        if "subrow_id" in data:
            processed_data["subrow_id"] = data["subrow_id"]

        transient_fields = data.get("transient", {})
        if transient_fields:
            processed_data.update(transient_fields)

        return processed_data

    def _call_get_api(self, url, params=None) -> dict:
        """makes the async api call"""

        LOGGER.debug(f"calling api {url}, params {params}")

        response = self._client.get(f"{self.base_api_path}/{url}", params=params)
        response.raise_for_status()

        data = response.json()
        return data

    def _process_sheet_rows[T: XivModel](
        self, data: list, model_class: type[T] = None, lang_data=[]
    ) -> Iterator[T | dict]:

        len_en = len(data)
        len_jp = len(lang_data)

        if len_en != len_jp:
            raise f"Length of English results {len_en} does not match Japanese {len_jp}"

        for item_data, lang_item_data in zip(data, lang_data):
            if not item_data:
                continue

            # LOGGER.debug(f"raw item data from api: {item_data}")

            processed_data = self._flatten_item_data(item_data)
            processed_lang_data = self._flatten_item_data(lang_item_data or {})
            row_id = item_data.get("row_id")

            if model_class:
                try:
                    model = model_class.model_validate(processed_data)

                    try:
                        lang_model = (
                            model_class.model_validate(processed_lang_data)
                            if processed_lang_data
                            else None
                        )
                    except ValidationError as ve:
                        lang_model = None
                        LOGGER.debug(
                            f"Error with Japanese data for {model_class.__name__} {row_id}. Error detail:",
                            exc_info=ve,
                        )

                    model._japanese = lang_model
                    LOGGER.debug(
                        f"Processed {model_class.__name__} sheet data for {processed_data.get("row_id")}"
                    )
                    yield model
                except ValidationError as e:
                    LOGGER.error(
                        f"Error with data for {model_class.__name__} {row_id}. Skipping."
                    )
                    # LOGGER.error(
                    #     f"Error with data for {model_class.__name__} {row_id}.\nInput processed data: {processed_data}\n Error detail:",
                    #     exc_info=e,
                    # )
            else:
                processed_data["ja"] = processed_lang_data
                yield processed_data

    def sheets(self) -> List[str]:

        res = self._call_get_api(f"sheet")

        return [row["name"] for row in res["sheets"]]

    def sheet[T: XivModel](
        self, model_class: type[T] | str, batch_size: int = None
    ) -> Iterator[list]:

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

        start = 0
        limit = batch_size or self.batch_size
        params = {
            "fields": fields,
            "transient": transient_fields,
            "limit": limit,
            "after": start,
        }
        has_more = True
        prev_results = None

        while has_more:

            params["after"] = start
            params["language"] = ENGLISH_LANG
            lang_rows = []

            data = self._call_get_api(
                f"sheet/{sheet_name}",
                params=params,
            )
            rows = data.get("rows", [])

            LOGGER.debug(
                f"received batched sheet response for {sheet_name} - after: {start} - rows: {len(rows)}"
            )

            if not rows:
                break

            if prev_results and prev_results[0]["row_id"] == rows[0]["row_id"]:
                raise "Received same API response"

            params["language"] = JAPANESE_LANG
            data = self._call_get_api(f"sheet/{sheet_name}", params)
            lang_rows = data.get("rows", [])

            for item in self._process_sheet_rows(
                rows, model_class if is_model_query else None, lang_rows
            ):
                yield item

            row_len = len(rows)
            if row_len < limit:
                has_more = False

            # use last row_id as the start of next batch
            start = rows[-1]["row_id"]
            prev_results = rows

    def get_sheet_names(self, name):
        """
        Gets the sheet names that start with 'name'
        """
        if not self.__class__._sheets:
            self.__class__._sheets = {"quest": [], CUSTOM: [], CUTSCENE: []}
            for sheet in self.sheets():
                if sheet.startswith("quest/"):
                    self.__class__._sheets["quest"].append(sheet)
                if sheet.startswith("custom/"):
                    self.__class__._sheets[CUSTOM].append(sheet)
                if sheet.startswith("cut_scene/"):
                    self.__class__._sheets[CUTSCENE].append(sheet)

        LOGGER.debug(
            f"found {len(self.__class__._sheets[name])} records for {name} sheets"
        )
        return self.__class__._sheets[name]


class XivApiClientManager:
    client: XivApiClient = None

    @classmethod
    def connect(cls):
        cls.client = XivApiClient()

    @classmethod
    def close(cls):
        cls.client.close()


class XivDataAccess:

    @classmethod
    def client(cls):
        return XivApiClientManager.client

    @classmethod
    def get_all(cls, model_class):
        if model_class == Quest:
            return cls._get_quests()

        if model_class == CustomText:
            return cls._get_custom_text()

        elif issubclass(model_class, SheetParseData):
            return cls._get_sheet_text_data(model_class)

        return cls._get_sheets(model_class)

    @classmethod
    def _get_sheet_text_data(cls, model_class: type[SheetParseData]):
        LOGGER.debug(f"loading data for {model_class.__name__}")

        for sheet_name in cls.client().get_sheet_names(model_class.__sheetname__):
            LOGGER.info(f'processing sheet data for {sheet_name}')

            # the sheet data will be the text contents
            text = list(cls.client().sheet(sheet_name))

            yield model_class.from_sheet_and_text(sheet_name, text)

    @classmethod
    def _get_custom_text(cls):

        custom_text_data = {m.Name: m for m in cls.client().sheet(CustomTalk) if m.Name}

        model: CustomText
        for model in cls._get_sheet_text_data(CustomText):

            # find the metadata
            metadata = custom_text_data.get(model.Name, None)
            model.row_id = metadata.row_id if metadata else model.row_id
            model.Type = metadata.MainOption if metadata else "Custom Talk"

            yield model

    @classmethod
    def _get_quests(cls):

        for quest_model in cls.client().sheet(Quest):

            # folder num is part of the key
            # example key: ChrHdy399_04784
            # folder:               |047|
            folder_num = quest_model.Id[-5:-2]
            sheet_name = f"quest/{folder_num}/{quest_model.Id}"
            # the sheet data will be the quest text
            quest_model._sheet_rows = list(cls.client().sheet(sheet_name))
            quest_model._sheet_name = sheet_name

            yield quest_model

    @classmethod
    def _get_sheets(cls, model_class):
        return cls.client().sheet(model_class)
