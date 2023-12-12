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
    filename: str = None 
    datatype: str = None 
    text: dict = None
    icon: str = None

def iter_quests():
    dir = pathlib.Path(f"{DATA_PATH}\\quest")
    metadata = _get_metadata()

    for filepath in scrub.iter_dir_files(dir):
        quest_data = _parse_quest_data(metadata, filepath)
        if quest_data:
            yield quest_data

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
    result["filename"] = filename
    result["datatype"] = "QUEST"
    result["text"] = contents

    return QuestData(**result)

def _dump_quest_info(fh, quest_data: QuestData):

    dumpstr = f"""
---------------------------------------------------------------------
{quest_data.name} ({quest_data.filename})
Issuer: {quest_data.issuer} [{quest_data.place_name}]
Journal: {quest_data.journal_genre} [{quest_data.expansion}]

{quest_data.text}
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

    df = df.rename(columns=QUEST_METADATA_COL_ALIASES)

    print(df)
    return df

