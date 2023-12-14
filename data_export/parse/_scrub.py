
import re
from types import SimpleNamespace
from ._shared import iter_csv_rows

SKIP_LINES = 3
SPEAKER_SKIPS = ("SEQ", "TODO",)

def get_col_value(row, col_name):

    value = row[col_name].values[0]

    return str(value)

def parse_speaker_transcript_file(file_path, speaker_pos=3):

    speaker_lines = []
    parsed = []
    previous_speaker = ''
        
    for line in iter_csv_rows(file_path):

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

def get_speaker(description, speaker_pos=3): 
    description_tokens = description.split('_')
    
    try:
        return description_tokens[speaker_pos]
    except IndexError:
        return ''

RE_HIGHLIGHT = re.compile(r'<Highlight>(.*?)<\/Highlight>')
RE_SPLIT = re.compile(r'<Split\((.*?), ,\d\)\/>')
RE_HESHE = re.compile(r'<If\(PlayerParameter\(4\)\)>(.*?)<Else\/>(.*?)<\/If>')
RE_RACE = re.compile(r'<Switch\(PlayerParameter\(71\)\)><Case\(1\)>(.*?)<\/Case><Case\(2\)>.*?<\/Case><Case\(3\)>.*?<\/Case><Case\(4\)>.*?<\/Case><Case\(5\)>.*?<\/Case><Case\(6\)>.*?<\/Case><Case\(7\)>.*?<\/Case><Case\(8\)>.*?<\/Case><\/Switch>')
RE_TOD = re.compile(r'<If\(LessThan\(PlayerParameter\(11\),12\)\)><If\(LessThan\(PlayerParameter\(11\),4\)\)>.*?<Else\/>.*?<\/If><Else\/><If\(LessThan\(PlayerParameter\(11\),17\)\)>(.*?)<Else\/>.*?<\/If><\/If>')
RE_ITALICS = re.compile(r'<Emphasis>(.*?)<\/Emphasis>')
RE_GRANDCOMPANY = re.compile(r'<If\(GreaterThan\(PlayerParameter\(52\),0\)\)>(.*?)<Else\/><If\(GreaterThan\(PlayerParameter\(53\),0\)\)>(.*?)<Else\/>(.*?)<\/If><\/If>')
RE_CLICKABLE = re.compile(r'<Clickable\((.*?)\)\/>')
RE_VALUE = re.compile(r'<Value>(.*?)<\/Value>')
RE_TIME = re.compile(r'<Time\((.*?)\)\/>')
RE_UIFOREGROUND = re.compile(r'<UIForeground>(.*?)<\/UIForeground>')
RE_UIGLOW = re.compile(r'<UIGlow>(.*?)<\/UIGlow>')
RE_RESETTIME = re.compile(r'<ResetTime>(\d*?)<\/ResetTime>')
RE_SHEETITEM = re.compile(r'<SheetE?n?\((.*?),(.*?)\/>')
RE_INT_PARAM = re.compile(r'IntegerParameter\((\d\d?\d?)\)')
RE_FORMAT = re.compile(r'<Format\((.*?),.*?\)\/>')
RE_TOPLEVELPARAM = re.compile(r'TopLevelParameter\((\d\d?\d?)\)')

IF_START = re.compile(r"<If\(((Equal)?(GreaterThan)?(LessThan)?\(PlayerParameter\((\d\d?)\),(\d\d?\d?)\))?(.*?)\)>")
IF_END = re.compile(r"<\/If>")
ELSE = re.compile(r"<Else\/>")

SWITCH_START = re.compile(r'<Switch\((.*?)\)>')
SWITCH_END = re.compile(r'<\/Switch>')

CASE_START = re.compile(r'<Case\((\d\d?\d?)\)>')
CASE_END = re.compile(r'<\/Case>')

def case_key(match):
    return f"{match.group(1)}"

def if_key(match):
    gname = match.group(5)    
    return f"PP{gname}-{match.group(6)}" if gname else ""

def switch_key(match):
    return ""

PATTERNS = (
    (IF_START,IF_END,ELSE, if_key),
    (SWITCH_START, SWITCH_END,None, switch_key),
    (CASE_START, CASE_END, None, case_key)
)

def sanitize_text(input: str):

    # GC rank insert
    input = input.replace("<Clickable(<If(GreaterThan(PlayerParameter(52),0))><Sheet(GCRankLimsaMaleText,PlayerParameter(52),8)/><Else/></If><If(GreaterThan(PlayerParameter(53),0))><Sheet(GCRankGridaniaMaleText,PlayerParameter(53),8)/><Else/></If><If(GreaterThan(PlayerParameter(54),0))><Sheet(GCRankUldahMaleText,PlayerParameter(54),8)/><Else/></If>)/>", "_GCRANK_")

    # WOL name
    input = input.replace("ObjectParameter(1)", "_WARRIOR_OF_LIGHT_")

    # choco name
    input = input.replace("ObjectParameter(55)", "_CHOCOBO_")

    # job insert
    input = input.replace("<Sheet(ClassJob,PlayerParameter(68),0)/>", "_JOB_")

    # a/an job insert
    input = input.replace("<If(Equal(PlayerParameter(68),10))>an _JOB_<Else/><If(Equal(PlayerParameter(68),14))>an _JOB_<Else/><If(Equal(PlayerParameter(68),5))>an _JOB_<Else/><If(Equal(PlayerParameter(68),26))>an _JOB_<Else/><If(Equal(PlayerParameter(68),33))>an _JOB_<Else/>a _JOB_</If></If></If></If></If>", "a _JOB_")

    # race insert 
    input = input.replace("<Sheet(Race,PlayerParameter(71),0)/>", "_RACE_")

    # starting city insert 
    input = input.replace("<Sheet(Town,PlayerParameter(70),0)/>", "_CITY_")

    # highlight
    input = RE_HIGHLIGHT.sub(r'\g<1>', input)

    # split
    input = RE_SPLIT.sub(r'\g<1>', input)

    # top level param
    input = RE_TOPLEVELPARAM.sub(r'_TLP\g<1>_', input)

    # value
    input = RE_VALUE.sub(r'\g<1>', input)

    # time
    input = RE_TIME.sub(r'_TIME_', input)

    # reset time
    input = RE_RESETTIME.sub(r'_RESET_', input)

    # ui foreground
    input = RE_UIFOREGROUND.sub(r'', input)

    # ui glow
    input = RE_UIGLOW.sub(r'', input)

    def sheet_repl(match):
        return f"_SHEET_{match.group(1).upper()}_"

    # sheet item
    input = RE_SHEETITEM.sub(sheet_repl, input)

    # int param
    input = RE_INT_PARAM.sub(r'_INT\g<1>_', input)

    # masculine/feminine replacement
    input = RE_HESHE.sub(r'\g<1>', input)

    # race based replacement (hyur default)
    input = RE_RACE.sub(r'\g<1>', input)

    # time of day replacement
    input = RE_TOD.sub(r'\g<1>', input)

    # format
    input = RE_FORMAT.sub(r'\g<1>', input)
    
    # italics
    input = RE_ITALICS.sub(r'*\g<1>*', input)

    # GC based text, 52 = maelstrom, 53 = twin adder, 54 = immortal flames
    input = RE_GRANDCOMPANY.sub(r'[?MAELSTROM: \g<1>] [?TWINADDER: \g<2>] [?IMMORTALFLAMES: \g<3>]', input)

    # clickable
    input = RE_CLICKABLE.sub(r'\g<1>', input)

    input = input.replace("<SheetEn(Item,1,IntegerParameter(1),1,1)/>", "[MAINHAND]")
    input = input.replace("<SheetEn(Item,1,IntegerParameter(2),1,1)/>", "[OFFHAND]")
    input = input.replace("<SheetEn(Item,\d,Integerarameter(\d),\d,\d)/>", "[ITEM]")

    for f_start, f_end, f_mid, f_key in PATTERNS:
        input = parse_syntax_tree(input, f_start, f_end, f_mid, f_key)

    return input

def parse_syntax_tree(input: str, start_pattern, end_pattern, operator_pattern=None, key_format=None):
    """
    parses the custom SE syntax to replace
    """

    m_end = end_pattern.search(input)

    new_input = input

    if m_end:
        end_pos = m_end.start()

        try:
            *_, m_start = start_pattern.finditer(input, 0, end_pos)
        except ValueError:
            print("Unable to find start of statement in " + input[:end_pos])
            print("input string: " + input)
            return input
        
        if m_start:

            start_endpos = m_start.end()
            
            node =SimpleNamespace()
            node.key = None 
            
            if key_format:
                node.key = key_format(m_start)

            node.left = input[start_endpos: end_pos]
            node.right = None

            if operator_pattern:
                m_else = operator_pattern.search(input, start_endpos, end_pos)
                
                if m_else:
                    node.left = input[start_endpos: m_else.start()]
                    node.right = input[m_else.end(): end_pos]

        node_key = f"{node.key}:" if node.key else ""
        node_str = f"[?{node_key} {node.left} :: {node.right}]" if node.right else f"[?{node_key} {node.left}]"

        new_input = input[:m_start.start()] + node_str + input[m_end.end():]
        new_input = parse_syntax_tree(new_input, start_pattern, end_pattern, operator_pattern)


    return new_input
        