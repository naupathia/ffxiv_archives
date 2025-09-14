from ..settings import OUTPUT_PATH
from . import _scrub, _shared
import pandas as pd
from collections import defaultdict

pd.options.display.max_rows = 10

OUTPUT_FILE = "quests.txt"
DATATYPE = "quest"

QUEST_METADATA_COLS = [
    "#",
    "Name",
    "Id",
    "Expansion",
    "PreviousQuest[0]",
    "Issuer{Start}",
    "PlaceName",
    "JournalGenre",
    "Icon",
]

QUEST_METADATA_COL_ALIASES = {
    "#": "key",
    "Name": "name",
    "Id": "id",
    "Expansion": "expansion",
    "PreviousQuest[0]": "previous_quest",
    "Issuer{Start}": "issuer",
    "PlaceName": "place_name",
    "JournalGenre": "journal_genre",
    "Icon": "icon",
}


class QuestIterator(_shared.DirIterator):
    def __init__(self) -> None:
        super().__init__("quest")

        df = pd.read_csv(
            f"{DATA_PATH}\\Quest.csv",
            skiprows=[0, 2],
            usecols=QUEST_METADATA_COLS,
            dtype=str,
            converters=defaultdict(lambda i: str),
            na_filter=False,
        )

        self._metadata = df.rename(columns=QUEST_METADATA_COL_ALIASES)
        self.item_sort_order = 1

    def _process_file(self, filepath, dirname):
        filename = filepath.stem

        row = self._metadata.loc[self._metadata["id"] == filename]

        if row.empty:
            return None

        def get_speaker(description):
            description_tokens = description.split("_")

            try:
                return description_tokens[3]
            except IndexError:
                return ""

        contents = _shared.DirIterator.parse_speaker_transcript_file(
            filepath, get_speaker=get_speaker
        )

        row_values = row.to_dict("records")[0]

        result = {
            "key": row_values["key"],
            "name": row_values["name"],
            "datatype": DATATYPE,
            "text": contents,
            "expansion": row_values["expansion"].lower(),
            "rank": self.item_sort_order,
            "meta": {
                "previous_quest": row_values["previous_quest"],
                "issuer": row_values["issuer"],
                "place_name": row_values["place_name"],
                "journal_genre": row_values["journal_genre"],
                "filename": filename
            }
        }

        self.item_sort_order += 1

        return result


def dump_text_file():
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        for quest in QuestIterator():
            fh.write(serialize(quest))


def serialize(record):
    return f"""
---------------------------------------------------------------------
[QUEST]

{record["name"]} ({record["meta"]["filename"]})
Issuer: {record["meta"]["issuer"]} [{record["meta"]["place_name"]}]
Journal: {record["meta"]["journal_genre"]} [{record["expansion"]}]

{record["text"]}

"""
