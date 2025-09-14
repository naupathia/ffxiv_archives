from ..settings import OUTPUT_PATH
from . import _scrub, _shared

OUTPUT_FILE = "cutscenes.txt"
DATATYPE = "cutscene"


class CutsceneIterator(_shared.DirIterator):
    def __init__(self) -> None:
        super().__init__("cut_scene")

    def _process_file(self, filepath, dirname):
        file_name = filepath.stem

        def get_speaker(description):
            description_tokens = description.split("_")

            try:
                return description_tokens[4]
            except IndexError:
                return ""

        contents = _scrub.parse_speaker_transcript_file(
            filepath, get_speaker=get_speaker
        )
        filenum = file_name[-5:]

        patch_num = dirname[1] + "." + dirname[2]

        result = {
            "name": f"Cutscenes {patch_num}.{filenum}",
            "text": contents,
            "datatype": DATATYPE,
            "expansion": self.get_expansion(dirname[1]).lower(),
            "meta": {
                "filename": file_name,
                "patch": patch_num,
            }
        }

        return result
    
    def get_expansion(self, number):
        if(number == "2"):
            return "A Realm Reborn"
        if(number == "3"):
            return "Heavensward"
        if(number == "4"):
            return "Stormblood"
        if(number == "5"):
            return "Shadowbringers"
        if(number == "6"):
            return "Endwalker"
        if(number == "7"):
            return "Dawntrail"
        
        return ""


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
