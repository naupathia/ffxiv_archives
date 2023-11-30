import pprint
import pathlib
from data_export.settings import DATA_PATH, OUTPUT_PATH
from . import scrub
import pandas as pd
from collections import defaultdict

pd.options.display.max_rows = 10


def get_metadata():
    df = pd.read_csv(
        f"{DATA_PATH}\\Quest.csv",
        skiprows=[0, 2],
        usecols=[
            "#",
            "Name",
            "Id",
            "Expansion",
            "PreviousQuest[0]",
            "Issuer{Start}",
            "PlaceName",
            "JournalGenre",
            "Icon",
        ],
        dtype=str,
        converters=defaultdict(lambda i: str),
        na_filter=False
    )

    print(df)

    df.columns = [
            "key",
            "name",
            "id",
            "expansion",
            "previous_quest",
            "issuer",
            "place_name",
            "journal_genre",
            "icon",
        ]

    print(df)

    return df


def output_quests():
    meta_data = get_metadata()

    dir = pathlib.Path(f"{DATA_PATH}\\quest")

    docs = []

    with open(f"{OUTPUT_PATH}\\quests.txt", "w+", encoding="UTF-8") as fh:
        for file_path in scrub.iter_dir_files(dir):
            file_name = file_path.stem
            contents = scrub.parse_speaker_transcript(file_path)

            row = meta_data.loc[meta_data["id"] == file_name]

            if row.empty:
                continue

            result = row.to_dict('records')[0]
            result["transcript"] = contents
            result["file_name"] = file_name
            result["raw"] = scrub.flatten_speaker_dialogue(contents)
            result["data_type"] = "QUEST"

            fh.write("\n")
            fh.write(
                "---------------------------------------------------------------------"
            )
            fh.write("\n")
            fh.write(result["name"])
            fh.write("\n")
            fh.write("Issuer: ")
            fh.write(result["issuer"])
            fh.write("\n")
            fh.write(result["expansion"])
            fh.write("\n")
            fh.write(result["journal_genre"])
            fh.write("\n")
            fh.write("\n")
            fh.write(scrub.print_speaker_dialogue(result["transcript"]))
            fh.write("\n")

            print(f"processed quest: {file_name}")

            docs.append(result)

    return docs