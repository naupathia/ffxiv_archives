from data_export.settings import OUTPUT_PATH
from . import _shared

OUTPUT_FILE = "fishes.txt"

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
            "datatype": "FISH"
        }


class FishIterator(_shared.FileIterator):
    GAME_FILE = "FishParameter.csv"
    SERDE = FishReader


def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        with _shared.open_csv_for_iteration(FishIterator.GAME_FILE) as ifh:    
            for item in FishIterator(ifh):
                fh.write(serialize(item))


def serialize(data: dict):

    return f"""
---------------------------------------------------------------------
{data["name"]}

{data["text"]}

"""
