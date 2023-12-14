from data_export.settings import DATA_PATH, OUTPUT_PATH
import csv
from . import scrub

NAME = "Name"
DESCRIPTION = "Description"
ICON = "Icon"
KEY = "#"
CATEGORY = "ItemUICategory"

FIELD_ALIASES = {
    NAME: "name",
    DESCRIPTION: "text",
    ICON: "icon",
    KEY: "key"
}

def iter_items():
        
    for item in scrub.iter_csv_dict(f"{DATA_PATH}\\Item.csv"):
        result = _parse_item(item)
        if result and result["name"]:
            yield result
    
    

def dump_items_text_file():

    with open(f"{OUTPUT_PATH}\\items.txt", "w+", encoding="UTF-8") as fh:
            
        for result in iter_items():
            _dump_str(fh, result)


def _parse_item(row) -> dict:
    return {
        "name": row[NAME],
        "text": scrub.sanitize_text(row[DESCRIPTION]),
        "icon": row[ICON],
        "key": row[KEY],
        "datatype": "ITEM",
        "subtype": row[CATEGORY]
    }

def _dump_str(fh, data: dict):

    dumpstr = f"""
---------------------------------------------------------------------
{data["name"]} ({data["subtype"]})

{data["text"]}
"""

    fh.write(dumpstr)
    fh.write("\n")
