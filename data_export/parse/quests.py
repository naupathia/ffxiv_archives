import pathlib
from data_export.settings import DATA_PATH, OUTPUT_PATH
from . import scrub
import pandas as pd
from collections import defaultdict
from dataclasses import dataclass

pd.options.display.max_rows = 10

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

QUEST_METADATA_COL_ALIASES = [
            "key",
            "name",
            "id",
            "expansion",
            "previous_quest",
            "issuer",
            "place_name",
            "journal_genre",
            "icon",
        ]

@dataclass
class QuestData:
    key: str = None 
    id: str = None 
    name: str = None 
    expansion: str= None 
    previous_quest: str= None  
    issuer: str = None 
    place_name:str = None 
    journal_genre: str = None 
    transcript: dict = None
    filename: str = None 
    raw: str = None 
    datatype: str = None 

def iter_quests():
    dir = pathlib.Path(f"{DATA_PATH}\\quest")
    metadata = _get_metadata()

    for filepath in scrub.iter_dir_files(dir):
        yield _parse_quest_data(metadata, filepath)
        print(f"processed quest: {filepath}")

def dump_quests_text_file():

    with open(f"{OUTPUT_PATH}\\quests.txt", "w+", encoding="UTF-8") as fh:
            
        for result in iter_quests():
            _dump_quest_info(fh, result)


def _parse_quest_data(metadata, filepath) -> QuestData:
    filename = filepath.stem

    row = metadata.loc[metadata["id"] == filename]

    if row.empty:
        return None

    contents = scrub.parse_speaker_transcript(filepath)

    result = row.to_dict('records')[0]
    result["transcript"] = contents
    result["filename"] = filename
    result["raw"] = scrub.flatten_speaker_dialogue(contents)
    result["datatype"] = "QUEST"

    return QuestData(**result)

def _dump_quest_info(fh, quest_data: QuestData):

    dialogue = scrub.format_speaker_dialogue(quest_data.transcript)
    dumpstr = f"""
---------------------------------------------------------------------
{quest_data.name}
Issuer: {quest_data.issuer} [{quest_data.place_name}]
Journal: {quest_data.expansion} [{quest_data.journal_genre}]

{dialogue}
"""

    fh.write(dumpstr)
    fh.write("\n")



def _get_metadata():
    df = pd.read_csv(
        f"{DATA_PATH}\\Quest.csv",
        skiprows=[0, 2],
        usecols=QUEST_METADATA_COLS,
        dtype=str,
        converters=defaultdict(lambda i: str),
        na_filter=False
    )

    df.columns = QUEST_METADATA_COL_ALIASES

    return df

