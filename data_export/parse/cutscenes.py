from data_export.settings import OUTPUT_PATH
from . import _scrub, _shared

OUTPUT_FILE = "cutscenes.txt"
DATATYPE = "CUTSCENE"

class CutsceneIterator(_shared.DirIterator):

    def __init__(self) -> None:
        super().__init__("cut_scene")

    def _process_file(self, filepath, dirname):
        file_name = filepath.stem
        contents = _scrub.parse_speaker_transcript_file(filepath, 4)
        filenum = file_name[-5:]

        patch_num = dirname[1] + "." + dirname[2]
        result = {
            "filename": file_name,
            "patch": patch_num,
            "name": f"Cutscenes {patch_num}.{filenum}",
            "text": contents,
            "datatype": DATATYPE,
            # "id": _shared.get_id(),
        }

        return result

def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:    
        for quest in CutsceneIterator():
            fh.write(serialize(quest))
            

def serialize(record):
   
   return f"""
---------------------------------------------------------------------
[CUTSCENE]
{record["name"]}

{record["text"]}

"""