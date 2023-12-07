import re
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

                if speaker_lines and speaker_lines:
                    dialogue = ' '.join(speaker_lines)
                    parsed.append(f"**{speaker}:** {dialogue}")
                    parsed.append('')
                    speaker_lines = []

            if text:
                speaker_lines.append(sanitize_text(text))
            
            previous_speaker = speaker

    return '\n'.join(parsed)


def sanitize_text(input: str):

    # GC rank insert
    input = input.replace("<Clickable(<If(GreaterThan(PlayerParameter(52),0))><Sheet(GCRankLimsaMaleText,PlayerParameter(52),8)/><Else/></If><If(GreaterThan(PlayerParameter(53),0))><Sheet(GCRankGridaniaMaleText,PlayerParameter(53),8)/><Else/></If><If(GreaterThan(PlayerParameter(54),0))><Sheet(GCRankUldahMaleText,PlayerParameter(54),8)/><Else/></If>)/>", "[GCRANK]")

    # WOL name
    input = input.replace("ObjectParameter(1)", "WARRIOR OF LIGHT")

    # job insert
    input = input.replace("<Sheet(ClassJob,PlayerParameter(68),0)/>", "[JOB]")

    # wtf job insert
    input = input.replace("<If(Equal(PlayerParameter(68),10))>an [JOB]<Else/><If(Equal(PlayerParameter(68),14))>an [JOB]<Else/><If(Equal(PlayerParameter(68),5))>an [JOB]<Else/><If(Equal(PlayerParameter(68),26))>an [JOB]<Else/><If(Equal(PlayerParameter(68),33))>an [JOB]<Else/>a [JOB]</If></If></If></If></If>", "a [JOB]")

    # race insert 
    input = input.replace("<Sheet(Race,PlayerParameter(71),0)/>", "[RACE]")

    # # highlight
    input = re.sub(r'<Highlight>(.*?)<\/Highlight>', r'\g<1>', input)

    # split
    input = re.sub(r'<Split\((.*?), ,\d\)\/>', r'\g<1>', input)

    # masculine/feminine replacement
    input = re.sub(r'<If\(PlayerParameter\(4\)\)>(.*?)<Else\/>(.*?)<\/If>', r'\g<1>', input)

    # race based replacement (hyur default)
    input = re.sub(r'<Switch\(PlayerParameter\(71\)\)><Case\(1\)>(.*?)<\/Case><Case\(2\)>.*?<\/Case><Case\(3\)>.*?<\/Case><Case\(4\)>.*?<\/Case><Case\(5\)>.*?<\/Case><Case\(6\)>.*?<\/Case><Case\(7\)>.*?<\/Case><Case\(8\)>.*?<\/Case><\/Switch>', r'\g<1>', input)

    # time of day replacement
    input = re.sub(r'<If\(LessThan\(PlayerParameter\(11\),12\)\)><If\(LessThan\(PlayerParameter\(11\),4\)\)>.*?<Else\/>.*?<\/If><Else\/><If\(LessThan\(PlayerParameter\(11\),17\)\)>(.*?)<Else\/>.*?<\/If><\/If>', r'\g<1>', input)

    # italics
    input = re.sub(r'<Emphasis>(.*?)<\/Emphasis>', r'*\g<1>*', input)

    # GC based text, 52 = maelstrom, 53 = twin adder, 54 = immortal flames
    input = re.sub(r'<If\(GreaterThan\(PlayerParameter\(52\),0\)\)>(.*?)<Else\/><If\(GreaterThan\(PlayerParameter\(53\),0\)\)>(.*?)<Else\/>(.*?)<\/If><\/If>', r'[?MAELSTROM: \g<1>] [?TWINADDER: \g<2>] [?IMMORTALFLAMES: \g<3>]', input)

    # clickable
    input = re.sub(r'<Clickable\((.*?)\)\/>', r'\g<1>', input)

    input = input.replace("<SheetEn(Item,1,IntegerParameter(1),1,1)/>", "[MAINHAND]")
    input = input.replace("<SheetEn(Item,1,IntegerParameter(2),1,1)/>", "[OFFHAND]")

    # conditional
    input = re.sub(r'<If\(Equal\(PlayerParameter\(.*?\)\)>(.*?)<Else\/><\/If>', r'[?\g<1>]', input)

    # conditional else
    input = re.sub(r'<If\(Equal\(PlayerParameter\((\d\d?)\),(\d\d?)\)\)>(.*?)<Else\/>(.*?)<\/If>', r'[?PP\g<1>=\g<2>: \g<3>] [\g<4>]', input)


    return input