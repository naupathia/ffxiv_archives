
from data_export.settings import OUTPUT_PATH
from . import _shared, _scrub

OUTPUT_FILE = "items.txt"
DATATYPE ="item"

class ItemReader(_shared.GameTypeRowAdapter):

    NAME = "Name"
    DESCRIPTION = "Description"
    ICON = "Icon"
    KEY = "#"
    CATEGORY = "ItemUICategory"

    @classmethod
    def read_record(cls, row: dict):
        return {
            "name": row[cls.NAME],
            "text": _scrub.sanitize_text(row[cls.DESCRIPTION]),
            "key": row[cls.KEY],
            "datatype": DATATYPE,
            "meta": {                
                "category": row[cls.CATEGORY],
            }
            # "id": _shared.get_id(),
        }



class ItemIterator(_shared.FileIterator):
    GAME_FILE = "Item.csv"
    ADAPTER = ItemReader


def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        for item in ItemIterator():
            fh.write(serialize(item))

def serialize(data: dict):

    return f"""
---------------------------------------------------------------------
[ITEM]

{data["name"]} ({data["meta"]["category"]})

{data["text"]}

"""
