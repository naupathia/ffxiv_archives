from ffxiv_archives.settings import SPEAKER_SKIPS, DATA_PATH, OUTPUT_PATH
import csv
import pathlib

def get_col_value(row, col_name):

    value = row[col_name].values[0]

    return str(value)


def iter_dir_contents(dir_path, speaker_pos=3):
    
    dir = pathlib.Path(dir_path)

    for f in dir.iterdir():
        if f.is_dir():

            for file_path in f.iterdir():

                file_name = file_path.stem
                yield file_name, parse_text(file_path, speaker_pos)


def get_speaker(description, speaker_pos=3): 
    description_tokens = description.split('_')
    
    try:
        return description_tokens[speaker_pos]
    except IndexError:
        return ''


def parse_text(file_path, speaker_pos=3):

    lines = []
    skip_count = 3

    with open(file_path, 'rt', encoding="UTF-8") as fh:

        reader = csv.reader(fh)
        previous_speaker = ''
        
        for line in reader:

            if skip_count > 0:
                skip_count -= 1
                continue

            text = line[2]
            description = line[1]
            speaker = get_speaker(description, speaker_pos)

            if previous_speaker != speaker:
                previous_speaker = speaker

                if speaker in SPEAKER_SKIPS:
                    continue

                if previous_speaker:
                    lines.append('\n')
                
                lines.append(speaker + ": ")
                
                
            if speaker in SPEAKER_SKIPS:
                continue

            if text:
                lines.append(text)

    return lines 