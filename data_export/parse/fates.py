from data_export.settings import OUTPUT_PATH
from . import _scrub, _shared

OUTPUT_FILE = "fates.txt"
DATATYPE = "fate"

class FateReader(_shared.GameTypeRowAdapter):

    NAME = "Name"
    DESCRIPTION = "Description"
    KEY = "#"
    LOCATION = "Location"
    
    @classmethod
    def read_record(cls, row: dict):        
        return {
            "name": row[cls.NAME],
            "text": _scrub.sanitize_text(row[cls.DESCRIPTION]),
            "key": row[cls.KEY],
            "datatype": DATATYPE,
            "meta": {                
                "location": row[cls.LOCATION],
            }
            # "id": _shared.get_id(),
        }

class FatesIterator(_shared.FileIterator):
    GAME_FILE = "Fate.csv"
    ADAPTER = FateReader


def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        for item in FatesIterator():
            fh.write(serialize(item))



def serialize(data: dict):

    return f"""
---------------------------------------------------------------------
[FATE]

{data["name"]} ({data["meta"]["location"]})

{data["text"]}

"""
