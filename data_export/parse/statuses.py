from data_export.settings import OUTPUT_PATH
from . import _scrub, _shared

OUTPUT_FILE = "statuses.txt"

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
            "datatype": "STATUS"
        }


class StatusIterator(_shared.FileIterator):
    GAME_FILE = "Status.csv"
    SERDE = StatusReader


def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        with _shared.open_csv_for_iteration(StatusIterator.GAME_FILE) as ifh:    
            for item in StatusIterator(ifh):
                fh.write(serialize(item))



def serialize(data: dict):

    return f"""
---------------------------------------------------------------------
{data["name"]}

{data["text"]}

"""
