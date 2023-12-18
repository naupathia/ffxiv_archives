from data_export.settings import OUTPUT_PATH
from . import _scrub, _shared

OUTPUT_FILE = "tripletriadcards.txt"
DATATYPE ="TRIPLETRIADCARD"

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
            "datatype": DATATYPE,
            # "id": _shared.get_id(),
        }



class TripleTriadCardIterator(_shared.FileIterator):
    GAME_FILE = "TripleTriadCard.csv"
    ADAPTER = TripleTriadCardReader


def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:            
        for item in TripleTriadCardIterator():
            fh.write(serialize(item))



def serialize(data: dict):

    return f"""
---------------------------------------------------------------------
[TRIPLE TRIAD CARD]

{data["name"]}

{data["text"]}

"""
