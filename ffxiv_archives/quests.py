import pathlib
from ffxiv_archives.settings import DATA_PATH, OUTPUT_PATH
from ffxiv_archives import scrub
import pandas as pd


pd.options.display.max_rows = 10

def get_metadata():
    return pd.read_csv(f"{DATA_PATH}\\Quest.csv", usecols=["key", "0", "1", "2", "1513"], dtype=str)

def output_quests():
    meta_data = get_metadata()
    
    dir = pathlib.Path(f"{DATA_PATH}\\quest")

    with open(f"{OUTPUT_PATH}\\quests.txt", "w+", encoding="UTF-8") as fh:

        for file_name, contents in scrub.iter_dir_contents(dir):

            row = meta_data.loc[meta_data["1"] == file_name]
            
            if row.empty:
                continue

            result = {
                "name": scrub.get_col_value(row, "0"),
                "key": file_name,
                "text": ' '.join(contents),
                "expansion": scrub.get_col_value(row, "2"),
                "journal": scrub.get_col_value(row, "1513")
            }

            fh.write('\n')
            fh.write('---------------------------------------------------------------------')
            fh.write('\n')
            fh.write(result["name"])
            fh.write('\n')
            fh.write(result["expansion"])
            fh.write('\n')
            fh.write(result["journal"])
            fh.write('\n')
            fh.write(result["text"])
            fh.write('\n')

            # break
