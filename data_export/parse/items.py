
from data_export.settings import OUTPUT_PATH
from . import _shared, _scrub

OUTPUT_FILE = "items.txt"

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
            "icon": row[cls.ICON],
            "key": row[cls.KEY],
            "datatype": "ITEM",
            "subtype": row[cls.CATEGORY]
        }



class ItemIterator(_shared.FileIterator):
    GAME_FILE = "Item.csv"
    SERDE = ItemReader


def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        with _shared.open_csv_for_iteration(ItemIterator.GAME_FILE) as ifh:    
            for item in ItemIterator(ifh):
                fh.write(serialize(item))

def serialize(data: dict):

    dumpstr = f"""
---------------------------------------------------------------------
{data["name"]} ({data["subtype"]})

{data["text"]}

"""