from data_export.settings import OUTPUT_PATH
from . import _scrub, _shared

OUTPUT_FILE = "tripletriadcards.txt"

class TripleTriadCardReader(_shared.GameTypeRowAdapter):

    NAME = "Name"
    DESCRIPTION = "Description"
    ICON = "Icon"
    KEY = "#"

    @classmethod
    def read_record(cls, row: dict):
        return {
            "name": row[cls.NAME],
            "text": _scrub.sanitize_text(row[cls.DESCRIPTION]),
            "key": row[cls.KEY],
            "datatype": "TRIPLETRIADCARD"
        }



class TripleTriadCardIterator(_shared.FileIterator):
    GAME_FILE = "TripleTriadCard.csv"
    SERDE = TripleTriadCardReader


def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        with _shared.open_csv_for_iteration(TripleTriadCardIterator.GAME_FILE) as ifh:    
            for item in TripleTriadCardIterator(ifh):
                fh.write(serialize(item))



def serialize(data: dict):

    return f"""
---------------------------------------------------------------------
{data["name"]}

{data["text"]}

"""
