from data_export.settings import OUTPUT_PATH
from . import _scrub, _shared

OUTPUT_FILE = "statuses.txt"
DATATYPE ="status"

class StatusReader(_shared.GameTypeRowAdapter):

    NAME = "Name"
    DESCRIPTION = "Description"
    ICON = "Icon"
    KEY = "#"

    @classmethod
    def read_record(cls, row: dict):
        return {
            "key": row[cls.KEY],
            "name": row[cls.NAME],
            "text": _scrub.sanitize_text(row[cls.DESCRIPTION]),
            "datatype": DATATYPE,
            # "id": _shared.get_id(),
        }


class StatusIterator(_shared.FileIterator):
    GAME_FILE = "Status.csv"
    ADAPTER = StatusReader


def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:    
        for item in StatusIterator():
            fh.write(serialize(item))



def serialize(data: dict):

    return f"""
---------------------------------------------------------------------
[STATUS EFFECT]

{data["name"]}

{data["text"]}

"""
