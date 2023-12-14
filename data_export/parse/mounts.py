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

class MountReader(_shared.GameTypeRowAdapter):

    NAME = "Singular"
    KEY = "#"

    @classmethod
    def read_record(cls, row: dict):
        return {
            "key": row[cls.KEY],
            "name": str(row[cls.NAME]).title(),
            "text": None,
            "datatype": "MOUNT"
        }



class MountIterator(_shared.FileIterator):
    GAME_FILE = "Mount.csv"
    ADAPTER = MountReader

    def __init__(self, fh) -> None:
        super().__init__(fh)

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

            result["text"] = f"{text}\n\n*Tooltip*:\n {tooltip}" if tooltip else text

        return result



def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        with _shared.open_csv_for_iteration(MountIterator.GAME_FILE) as ifh:    
            for item in MountIterator(ifh):
                fh.write(serialize(item))



def serialize(data):

    return f"""
---------------------------------------------------------------------
{data["name"]}

{data["text"]}

"""




