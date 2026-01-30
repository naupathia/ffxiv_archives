import re

SPEAKER_SKIPS = ("SEQ", "TODO", "SYSTEM")
SPEAKER_MAPS = {
    "CRYSTALEXARCH" : "CRYSTAL EXARCH",
    "MYSTERYVOICE" : "CRYSTAL EXARCH",
    "MYSTERIOUSPERSON" : "ZERO",
    "WUKLAMAT": "WUK LAMAT",
    "GULOOLJA": "GULOOL JA",
    "GULOOLJAJA": "GULOOL JA JA",
    "GRAHATIA": "GRAHA TIA",
}

RE_UNICODE = re.compile(r'[^\x00-\x7F]+')

def get_col_value(row, col_name):

    value = row[col_name].values[0]

    return str(value)

def get_speaker(value, pos=3):
    if not value:
        return ""

    value_tokens = value.split("_")

    speaker = value_tokens[pos]
    return SPEAKER_MAPS.get(speaker) or speaker

def parse_speaker_lines(row_iterator, speaker_func = get_speaker):
    
    speaker = ''
    speaker_lines = []

    text_tuples = []

    def add_lines():
        nonlocal speaker, speaker_lines
        if speaker_lines and speaker not in SPEAKER_SKIPS:
            text_tuples.append((speaker, create_paragraph(speaker_lines)))
        
        speaker_lines = []
        
    for line in row_iterator:

        text = line[2] or ""
        description = line[1] or ""
        next_speaker = speaker_func(description)
            
        if speaker and speaker != next_speaker:
            add_lines()

        if text:
            speaker_lines.append(text)
        
        speaker = next_speaker

    add_lines()

    return text_tuples

def create_paragraph(speaker_lines):
    if not speaker_lines:
        return ''
    
    return '\n'.join(speaker_lines)

def remove_non_ascii(text_string):
    if not text_string:
        return text_string
    
    # Encode to ASCII, ignoring errors, then decode back to a string
    # return text_string.encode("ascii", errors="ignore").decode("ascii")
    return re.sub(r'[^\x00-\x7F]+',' ', text_string)

def clean_text(text_string):
    if not text_string:
        return text_string
    
    return remove_non_ascii(text_string).replace('\n', ' ')