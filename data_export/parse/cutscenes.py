import pathlib
from data_export.settings import DATA_PATH, OUTPUT_PATH
from . import scrub
from dataclasses import dataclass

@dataclass
class CutsceneData:
    filename: str = None 
    transcript: dict = None 
    raw: str = None 
    datatype: str = None


def iter_cutscenes():
    dir = pathlib.Path(f"{DATA_PATH}\\cut_scene")

    for filepath in scrub.iter_dir_files(dir):
        yield _parse_cutscene_data(filepath)
        print(f"processed cutscene: {filepath}")


def dump_cutscene_text_file():

    with open(f"{OUTPUT_PATH}\\cutscenes.txt", "w+", encoding="UTF-8") as fh:
        for result in iter_cutscenes():
            _dump_cutscene_text(fh, result)


def _parse_cutscene_data(filepath) -> CutsceneData:
    
    file_name = filepath.stem
    contents = scrub.parse_speaker_transcript(filepath, 4)

    result = {
        "filename": file_name,
        "transcript": contents,
        "raw": scrub.flatten_speaker_dialogue(contents)
    }
    result["datatype"] = "CUTSCENE"

    return CutsceneData(**result)

def _dump_cutscene_text(fh, cutscene_data: CutsceneData):
   
   contents = scrub.format_speaker_dialogue(cutscene_data.transcript)
   dumpstr = f"""
---------------------------------------------------------------------

{contents}

"""
   
   fh.write(dumpstr)