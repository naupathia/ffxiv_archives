import re

SPEAKER_SKIPS = ("SEQ", "TODO", "SYSTEM")
SPEAKER_MAPS = {
    "CRYSTALEXARCH": "CRYSTAL EXARCH",
    "MYSTERYVOICE": "CRYSTAL EXARCH",
    "MYSTERIOUSPERSON": "ZERO",
    "WUKLAMAT": "WUK LAMAT",
    "GULOOLJA": "GULOOL JA",
    "GULOOLJAJA": "GULOOL JA JA",
    "GRAHATIA": "GRAHA TIA",
}

RE_UNICODE = re.compile(r"[^\x00-\x7F]+")
RE_SPEAKER_ALIAS = re.compile(r"\(-(.*?)-\)")
RE_ANSWER = re.compile(r"^A\d*$")
RE_QUESTION = re.compile(r"^Q\d*$")


class MarkdownBuilder:

    @classmethod
    def h3(cls, text):
        return f"### {text}\n"

    @classmethod
    def p(cls, text):
        return f"{text}\n\n"

    @classmethod
    def br(cls):
        return "\n\n"

    @classmethod
    def blockquote(cls, text: str):
        return "> " + "\n> ".join(text.splitlines()) + "\n\n"

    @classmethod
    def replace_new_lines(cls, text):
        return text


md = MarkdownBuilder


def get_col_value(row, col_name):

    value = row[col_name].values[0]

    return str(value)


def is_int(text):
    try:
        int(text)
        return True
    except:
        return False


def get_speaker(tokens, pos=3, use_speaker_range=False):
    if not tokens or len(tokens) < pos:
        return ""

    if use_speaker_range and len(tokens) > pos + 1:
        speaker = "_".join((t for t in tokens[pos:-1] if not is_int(t)))
        speaker = speaker or tokens[pos]
    else:
        speaker = tokens[pos]

    return SPEAKER_MAPS.get(speaker) or speaker


def parse_speaker_lines(row_iterator, speaker_pos=3, use_speaker_range=False):

    speaker = ""
    speaker_lines = []
    speaker_lines_jp = []
    line_num = None
    prev_line_num = None
    index = 1

    lines = []
    jp_lines = []

    def add_lines():
        nonlocal lines, speaker, speaker_lines, index, speaker_lines_jp, jp_lines
        if speaker_lines and speaker not in SPEAKER_SKIPS:
            lines.append(md.h3(speaker) + create_paragraph(speaker_lines))
            jp_lines.append(md.h3(speaker) + create_paragraph(speaker_lines_jp))

        speaker_lines = []
        speaker_lines_jp = []
        index = 1

    for row in row_iterator:

        _, description, text, jp_values = row.values()
        _, _, jp_text = jp_values.values()

        if not description:
            continue
        
        text = text or ''
        jp_text = jp_text or '' # not sure why some text is null for jp

        tokens = description.split("_")
        next_speaker = get_speaker(tokens, speaker_pos, use_speaker_range)
        line_num = None

        if len(tokens) > speaker_pos + 1:
            try:
                line_num = int(tokens[-1])
            except ValueError:
                line_num = None

        text, line_speaker = remove_speaker_aliases(text)

        if line_speaker:
            next_speaker = line_speaker

        if speaker and speaker != next_speaker:
            add_lines()

        # if speaker is the same but line number has jumped to next 10, add extra line break
        elif (
            line_num
            and prev_line_num
            and line_num > prev_line_num + 1
            and line_num % 10 == 0
        ):
            # add the lines as if new speaker is beginning
            add_lines()

        if is_answer(next_speaker) and line_num:
            text = f"{index}: {text}"
            jp_text = f"{index}: {jp_text}"
            index += 1

        speaker_lines.append(text)
        speaker_lines_jp.append(jp_text)
        speaker = next_speaker
        prev_line_num = line_num

    add_lines()

    return md.br().join(lines), md.br().join(jp_lines)


def is_answer(text):
    return RE_ANSWER.match(text)


def create_paragraph(speaker_lines):
    if not speaker_lines:
        return ""

    return "\n\n".join(speaker_lines)


def remove_speaker_aliases(line):
    matches = RE_SPEAKER_ALIAS.search(line)
    if matches:
        return RE_SPEAKER_ALIAS.sub("", line), matches.group(0)

    return line, None


def remove_non_ascii(text_string):
    if not text_string:
        return text_string

    # Encode to ASCII, ignoring errors, then decode back to a string
    # return text_string.encode("ascii", errors="ignore").decode("ascii")
    return re.sub(r"[^\x00-\x7F]+", " ", text_string)


def clean_text(text_string):
    if not text_string:
        return text_string

    return remove_non_ascii(text_string).replace("\n", " ")
