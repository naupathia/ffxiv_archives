from data_export.settings import OUTPUT_PATH
from . import _scrub, _shared
from ._scrub import SPEAKER_MAPS, SPEAKER_SKIPS

OUTPUT_FILE = "customtext.txt"
DATATYPE = "CUSTOM"


class CustomDirIterator(_shared.DirIterator):
    def __init__(self) -> None:
        super().__init__("custom")

    def _process_file(self, filepath, dirname):
        file_name = filepath.stem
        contents = parse_speaker_transcript_file(filepath)

        result = {
            "filename": file_name,
            "name": file_name,
            "text": contents,
            "datatype": DATATYPE,
            # "id": _shared.get_id(),
        }

        return result


def parse_speaker_transcript_file(file_path):
    speaker_lines = []
    parsed = []
    previous_speaker = ""
    was_answer = False

    for line in _scrub.iter_csv_rows(file_path):
        # print(line)

        text = line[2]
        description = line[1]
        tokens = description.split("_")
        current_speaker = ("_").join(tokens[3:])

        try:
            group_field = tokens[-2]
        except IndexError:
            group_field = ""

        try:
            group_num = int(group_field)
        except ValueError:
            group_num = 0

        try:
            line_field = tokens[-1]
        except IndexError:
            line_field = ""

        try:
            line_num = int(line_field)
            current_speaker = ("_").join(tokens[3:-1])
        except ValueError:
            line_num = 0

        if group_field == "000":
            current_speaker = ("_").join(tokens[3:-2])

            if current_speaker == "A1":
                was_answer = True
                line_num = line_num + 1
                current_speaker = f"{current_speaker}_Q{line_num}00"

        if was_answer and group_num > 0:
            current_speaker = ("_").join(tokens[3:-2])
            current_speaker = f"{current_speaker}_A{group_num}"
            

        if previous_speaker and previous_speaker != current_speaker:
            if speaker_lines and previous_speaker not in SPEAKER_SKIPS:
                dialogue = " ".join(speaker_lines)
                speaker_name = SPEAKER_MAPS.get(previous_speaker, previous_speaker)
                parsed.append(f"{speaker_name}: {dialogue}")
                parsed.append("")

            speaker_lines = []

        if text:
            speaker_lines.append(_scrub.sanitize_text(text))

        previous_speaker = current_speaker
        
    if speaker_lines and previous_speaker not in SPEAKER_SKIPS:
        dialogue = " ".join(speaker_lines)
        speaker_name = SPEAKER_MAPS.get(previous_speaker, previous_speaker)
        parsed.append(f"{speaker_name}: {dialogue}")
        parsed.append("")

    return "\n".join(parsed)


def dump_text_file():
    with open(f"{OUTPUT_PATH}\\{OUTPUT_FILE}", "w+", encoding="UTF-8") as fh:
        for quest in CustomDirIterator():
            fh.write(serialize(quest))


def serialize(record):
    return f"""
---------------------------------------------------------------------
[CUSTOM]
{record["name"]}

{record["text"]}

"""
