from data_export.settings import OUTPUT_PATH
from . import _scrub, _shared

OUTPUT_FILE = "statuses.txt"
DATATYPE ="STATUS"

class StatusReader(_shared.GameTypeRowAdapter):

    NAME = "Name"
    DESCRIPTION = "Description"
    ICON = "Icon"
    KEY = "#"

    @classmethod
    def read_record(cls, row: dict):
        return {
            "name": row[cls.NAME],
            "text": _scrub.sanitize_text(row[cls.DESCRIPTION]),
            "icon": row[cls.ICON],
            "key": row[cls.KEY],
            "datatype": DATATYPE
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
{data["name"]}

{data["text"]}

"""
