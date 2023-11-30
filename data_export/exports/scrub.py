from data_export.settings import SPEAKER_SKIPS
import csv
import pathlib

def get_col_value(row, col_name):

    value = row[col_name].values[0]

    return str(value)


def iter_dir_files(dir_path):
    
    dir = pathlib.Path(dir_path)

    for f in dir.iterdir():
        if f.is_dir():

            for file_path in f.iterdir():

                yield file_path


def get_speaker(description, speaker_pos=3): 
    description_tokens = description.split('_')
    
    try:
        return description_tokens[speaker_pos]
    except IndexError:
        return ''


def parse_speaker_transcript(file_path, speaker_pos=3):

    speaker_lines = []
    parsed = []
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
                
            if speaker in SPEAKER_SKIPS:
                continue

            if previous_speaker and previous_speaker != speaker:

                if speaker_lines:
                    parsed.append({"speaker": previous_speaker, "text": " ".join(speaker_lines)})
                    speaker_lines = []

            if text:
                speaker_lines.append(text)
            
            previous_speaker = speaker

    return parsed 

def flatten_speaker_dialogue(transcript):

    result = []
    for lines in transcript:
        speaker = lines["speaker"]
        result.append(f"{speaker}:")
        result.append(lines["text"])

    return ' '.join(result)


def print_speaker_dialogue(transcript):

    result = []
    for lines in transcript:
        speaker = lines["speaker"]
        text = lines["text"]
        result.append(f"{speaker}: {text}")

    return '\n\n'.join(result)