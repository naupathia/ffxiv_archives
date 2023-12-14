from data_export.settings import DATA_PATH, OUTPUT_PATH
import csv
from . import scrub

NAME = "Item"
DESCRIPTION = "Text"
KEY = "#"

def iter_items():
        
    for item in scrub.iter_csv_dict(f"{DATA_PATH}\\FishParameter.csv"):
        result = _parse_item(item)
        if result and result["name"]:
            yield result
    
    

def dump_text_file():

    with open(f"{OUTPUT_PATH}\\fishes.txt", "w+", encoding="UTF-8") as fh:
            
        for result in iter_items():
            _dump_str(fh, result)


def _parse_item(row) -> dict:
    return {
        "name": row[NAME],
        "text": row[DESCRIPTION],
        "key": row[KEY],
        "datatype": "FISH"
    }

def _dump_str(fh, data: dict):

    dumpstr = f"""
---------------------------------------------------------------------
{data["name"]}

{data["text"]}
"""

    fh.write(dumpstr)
    fh.write("\n")
