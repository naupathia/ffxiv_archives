from data_export.settings import OUTPUT_PATH
from . import _scrub, _shared

OUTPUT_FILE = "cutscenes.txt"


class CutsceneIterator(_shared.DirIterator):

    def _process_file(self, filepath):
        file_name = filepath.stem
        contents = _scrub.parse_speaker_transcript_file(filepath, 4)

        result = {
            "filename": file_name,
            "text": contents,
            "datatype": "CUTSCENE"
        }

        return result

def dump_text_file():
    
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:    
        for quest in CutsceneIterator("cutscene"):
            fh.write(serialize(quest))
            

def serialize(record):
   
   return f"""
---------------------------------------------------------------------

{record.text}

"""