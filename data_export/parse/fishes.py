from data_export.settings import OUTPUT_PATH
from . import _shared

OUTPUT_FILE = "fishes.txt"
DATATYPE ="FISH"

class FishReader(_shared.GameTypeRowAdapter):
   
    NAME = "Item"
    DESCRIPTION = "Text"
    KEY = "#"

    @classmethod
    def read_record(cls, row: dict):
        return {
            "name": row[cls.NAME],
            "text": row[cls.DESCRIPTION],
            "key": row[cls.KEY],
            "datatype": DATATYPE
        }


class FishIterator(_shared.FileIterator):
    GAME_FILE = "FishParameter.csv"
    ADAPTER = FishReader


def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        for item in FishIterator():
            fh.write(serialize(item))


def serialize(data: dict):

    return f"""
---------------------------------------------------------------------
[FISH]

{data["name"]}

{data["text"]}

"""
