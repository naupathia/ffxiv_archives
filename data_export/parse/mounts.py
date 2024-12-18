from data_export.settings import DATA_PATH, OUTPUT_PATH
from . import _scrub, _shared
import pandas as pd
from collections import defaultdict

pd.options.display.max_rows = 10

METADATA_COLS = [
    "#",
    "Description",
    "Tooltip",
]

METADATA_COL_ALIASES = {
    "#": "key",            
    "Description": "text",            
    "Tooltip": "tooltip",
}

OUTPUT_FILE = "mounts.txt"
DATATYPE ="mount"

class MountReader(_shared.GameTypeRowAdapter):

    NAME = "Singular"
    KEY = "#"

    @classmethod
    def read_record(cls, row: dict):
        return {
            "key": row[cls.KEY],
            "name": str(row[cls.NAME]).title(),
            "text": None,
            "datatype": DATATYPE,
            # "id": _shared.get_id(),
        }



class MountIterator(_shared.FileIterator):
    GAME_FILE = "Mount.csv"
    ADAPTER = MountReader

    def __init__(self) -> None:
        super().__init__()

        df = pd.read_csv(
            f"{DATA_PATH}\\MountTransient.csv",
            skiprows=[0, 2],
            usecols=METADATA_COLS,
            dtype=str,
            converters=defaultdict(lambda i: str),
            na_filter=False
        )

        self._metadata = df.rename(columns=METADATA_COL_ALIASES)

    def _process_row(self, row: dict):
        result = super()._process_row(row)
        
        if not result or result["name"] is None:
            return None

        dr = self._metadata.loc[self._metadata["key"] == result["key"]]

        if not dr.empty:
            text = _scrub.get_col_value(dr, "text")
            tooltip = _scrub.get_col_value(dr, "tooltip")
            tooltip = tooltip.replace('\r\n','\n') if tooltip else None
            
            result["text"] = f"{text}\n\n*Tooltip*:\n {tooltip}" if tooltip else text

        return result



def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:   
        for item in MountIterator():
            print(item)
            fh.write(serialize(item))



def serialize(data):

    return f"""
---------------------------------------------------------------------
[MOUNT]

{data["name"]}

{data["text"]}

"""




