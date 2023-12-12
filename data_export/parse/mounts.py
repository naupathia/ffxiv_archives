import pathlib
from data_export.settings import DATA_PATH, OUTPUT_PATH
from . import scrub
import pandas as pd
from collections import defaultdict
from dataclasses import dataclass

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

NAME = "Singular"
KEY = "#"

def iter_items():
    metadata = _get_metadata()

    for item in scrub.iter_csv_dict(f"{DATA_PATH}\\Mount.csv"):
        result = _parse_data(metadata, item)
        if result:
            yield result

def dump_text_file():

    with open(f"{OUTPUT_PATH}\\mounts.txt", "w+", encoding="UTF-8") as fh:
            
        for result in iter_items():
            _dump_quest_info(fh, result)


def _parse_data(metadata, row) -> dict:

    result = {
        "key": row[KEY],
        "name": str(row[NAME]).title(),
        "text": None,
        "datatype": "MOUNT"
    }

    if not result["name"]:
        return None


    dr = metadata.loc[metadata["key"] == result["key"]]

    if not dr.empty:
        text = scrub.get_col_value(dr, "text")
        tooltip = scrub.get_col_value(dr, "tooltip")

        result["text"] = f"{text}\n\n*Tooltip*:\n {tooltip}" if tooltip else text

    return result


def _dump_quest_info(fh, data):

    dumpstr = f"""
---------------------------------------------------------------------
{data["name"]}

{data["text"]}
"""

    fh.write(dumpstr)
    fh.write("\n")



def _get_metadata():
    df = pd.read_csv(
        f"{DATA_PATH}\\MountTransient.csv",
        skiprows=[0, 2],
        usecols=METADATA_COLS,
        dtype=str,
        converters=defaultdict(lambda i: str),
        na_filter=False
    )

    df = df.rename(columns=METADATA_COL_ALIASES)

    print(df)
    return df

