from typing import Iterator, Type
from . import model, _scrub, xivclient
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)


class HtmlBuilder:

    @classmethod
    def h1(cls, text):
        return f'<h1>{text}</h1>\n\n'

    @classmethod
    def p(cls, text):
        return f'<p>{text}</p>\n\n'
        
    @classmethod
    def br(cls):
        return '<br/>\n'
    
    @classmethod
    def replace_new_lines(cls, text):
        return _scrub.replace_new_lines(text)
    
def get_expansion_number(name: str): 
    if name:
        exp = model.EXPANSIONS_LOOKUP.get(name.lower(), None)
        return exp.num if exp else None
    
    return None

html = HtmlBuilder


class TextLinesParser:

    speaker_pos = 3
    pretty_text = None 
    search_text = None
    speakers = None

    def __init__(self, speaker_pos = 3):
        self.speaker_pos = speaker_pos        
    
    def parse_text(self, textlines):
        pretty, search, speakers = _scrub.parse_speaker_lines(textlines, lambda x: _scrub.get_speaker(x, self.speaker_pos))
        self.pretty_text = pretty
        self.search_text = search 
        self.speakers = speakers
    
    def get_search_text(self, textlines):
        
        if self.search_text is None: 
            self.parse_text(textlines)

        return self.search_text

    def get_pretty_text(self, textlines):
        
        if self.pretty_text is None: 
            self.parse_text(textlines)

        return self.pretty_text

    def get_speakers(self, textlines):
        
        if self.speakers is None: 
            self.parse_text(textlines)

        return self.speakers

class DataAdapter:
    DATA_CLASS: Type[xivclient.XivModel] = None
    DATA_TYPE: str = model.DataTypes.QUEST

    @classmethod
    def get_all(cls, row=None) -> Iterator[model.SearchItem]:

        for data in cls.get_data(row):
            try:
                result = cls.map_model(data)
                if not result.text_clean or not result.text_clean.strip():  # ignore items without text to search
                    continue
                yield result
            except Exception as e:
                LOGGER.error("Failed to map data into search model", exc_info=e)

    @classmethod
    def get_data(cls, row=None) -> Iterator[xivclient.XivModel]:
        return xivclient.XivDataAccess.get_all(cls.DATA_CLASS, row)

    @classmethod
    def get_key(cls, data: xivclient.XivModel):
        return str(data.row_id)
    
    @classmethod
    def get_name(cls, data: xivclient.XivModel):
        return data.Name or ""
    
    @classmethod
    def get_pretty_text(cls, data: xivclient.XivModel):
        return html.p(cls.get_search_text(data))
    
    @classmethod
    def get_search_text(cls, data: xivclient.XivModel):
        return data.Description or ""

    @classmethod
    def get_meta(cls, data: xivclient.XivModel):
        return None
    
    @classmethod
    def get_expansion(cls, data: xivclient.XivModel):
        name = cls.get_expansion_name(data)
        if name:
            return model.EXPANSIONS_LOOKUP.get(name, None)
        
        return None
    
    @classmethod
    def get_expansion_name(cls, data: xivclient.XivModel):
        return None
    
    @classmethod
    def get_speakers(cls, data: xivclient.XivModel):
        return None
    
    @classmethod
    def map_model(cls, data: xivclient.XivModel) -> model.SearchItem:

        return model.SearchItem(
            _id=f"{cls.DATA_TYPE}-{data.row_id}",            
            row_id=data.row_id,
            key=cls.get_key(data),
            name=cls.get_name(data),
            text_html=cls.get_pretty_text(data),
            text_clean=cls.get_search_text(data),
            expansion=cls.get_expansion(data),
            speakers=cls.get_speakers(data),
            meta=cls.get_meta(data),
            datatype=cls.DATA_TYPE
        )


class QuestAdapter(DataAdapter):
    DATA_CLASS = xivclient.Quest
    DATA_TYPE: str = model.DataTypes.QUEST
    LINE_PARSER = TextLinesParser()

    @classmethod
    def get_expansion_name(cls, data: xivclient.Quest):
        return data.Expansion.Name.lower() if data.Expansion.Name else None
    
    @classmethod
    def get_key(cls, data: xivclient.XivModel):
        return data.sheet_name
    
    @classmethod
    def get_meta(cls, data: xivclient.Quest):

        prev_quest = data.PreviousQuest[0] if data.PreviousQuest else None
        return model.QuestMeta(
                previous_quest=prev_quest and prev_quest.Name,
                issuer=data.IssuerStart and data.IssuerStart.Singular,
                place_name=data.PlaceName and data.PlaceName.Name,
                journal_genre=data.JournalGenre and data.JournalGenre.Name,
                filename=data.Id or "",
            )
    
    @classmethod
    def get_speakers(cls, data):
        return cls.LINE_PARSER.get_speakers(data.Text)

    @classmethod
    def get_search_text(cls, data):
        return cls.LINE_PARSER.get_search_text(data.Text)
    
    @classmethod
    def get_pretty_text(cls, data):
        return cls.LINE_PARSER.get_pretty_text(data.Text)
    

class ItemAdapter(DataAdapter):
    DATA_CLASS = xivclient.Item
    DATA_TYPE: str = model.DataTypes.ITEM

    @classmethod
    def get_meta(cls, data: xivclient.Item):
        return model.ItemMeta(
                category=data.ItemUICategory.Name or "",
            )


class MountAdapter(DataAdapter):
    DATA_CLASS = xivclient.Mount
    DATA_TYPE: str = model.DataTypes.MOUNT

    @classmethod
    def get_name(cls, data: xivclient.Mount):
        return data.Singular.title()
    
    @classmethod
    def get_pretty_text(cls, data: xivclient.Mount):
        return html.p(html.replace_new_lines(
            f"{data.Description}\n\n{data.DescriptionEnhanced}\n\nTooltip:\n{data.Tooltip}"
            if data.Tooltip
            else f"{data.Description}\n\n{data.DescriptionEnhanced}"
        ))
    
    @classmethod
    def get_search_text(cls, data: xivclient.Mount):
        tooltip = data.Tooltip or ""
        return data.Description + " " + data.DescriptionEnhanced + " " + tooltip


class FishAdapter(DataAdapter):
    DATA_CLASS = xivclient.FishParameter
    DATA_TYPE: str = model.DataTypes.FISH

    @classmethod
    def get_name(cls, data: xivclient.FishParameter):
        return data.Item.Name

    @classmethod
    def get_search_text(cls, data: xivclient.FishParameter):
        return data.Text
    


class FateAdapter(DataAdapter):
    DATA_CLASS = xivclient.Fate
    DATA_TYPE: str = model.DataTypes.FATE


class FateEventAdapter(DataAdapter):
    DATA_CLASS = xivclient.FateEvent
    DATA_TYPE: str = model.DataTypes.FATE_EVENT

    @classmethod
    def get_name(cls, data):
        return "Fate Event Text"

    @classmethod
    def get_pretty_text(cls, data: xivclient.FateEvent):
                
        lines = [_scrub.sanitize_text(line) for line in data.Text if line]

        return html.p(html.br().join(lines))
    
    
    @classmethod
    def get_search_text(cls, data: xivclient.FateEvent):
        
        lines = [_scrub.remove_non_ascii(_scrub.sanitize_text(line)) for line in data.Text if line]

        return ' '.join(lines)


class TripleTriadCardAdapter(DataAdapter):
    DATA_CLASS = xivclient.TripleTriadCard
    DATA_TYPE: str = model.DataTypes.TRIPLETRIAD


class StatusAdapter(DataAdapter):
    DATA_CLASS = xivclient.Status
    DATA_TYPE: str = model.DataTypes.STATUS


class CutsceneAdapter(DataAdapter):
    DATA_CLASS = xivclient.CutsceneText
    DATA_TYPE: str = model.DataTypes.CUTSCENE
    LINE_PARSER = TextLinesParser(4)

    @classmethod
    def get_expansion_name(cls, data):
        return data.expansion.lower()
    
    @classmethod
    def get_speakers(cls, data: xivclient.CutsceneText):
        return cls.LINE_PARSER.get_speakers(data.TextLines)

    @classmethod
    def get_search_text(cls, data: xivclient.CutsceneText):
        return cls.LINE_PARSER.get_search_text(data.TextLines)
    
    @classmethod
    def get_pretty_text(cls, data: xivclient.CutsceneText):
        return cls.LINE_PARSER.get_pretty_text(data.TextLines)
    
    @classmethod
    def get_key(cls, data: xivclient.XivModel):
        return data.sheet_name

class CustomTextAdapter(DataAdapter):
    DATA_CLASS = xivclient.CustomText
    DATA_TYPE: str = model.DataTypes.CUSTOM
    LINE_PARSER = TextLinesParser()

    @classmethod
    def get_name(cls, data: xivclient.CustomText):
        return data.Type or "Custom Text"

    @classmethod
    def get_search_text(cls, data: xivclient.CustomText):
        return data.Text
    
    @classmethod
    def get_speakers(cls, data: xivclient.CustomText):
        return cls.LINE_PARSER.get_speakers(data.TextLines)

    @classmethod
    def get_search_text(cls, data: xivclient.CustomText):
        return cls.LINE_PARSER.get_search_text(data.TextLines)
    
    @classmethod
    def get_pretty_text(cls, data: xivclient.CustomText):
        return cls.LINE_PARSER.get_pretty_text(data.TextLines)

    @classmethod
    def get_key(cls, data: xivclient.CustomText):
        return data.Name

class UnendingCodexAdapter(DataAdapter):
    DATA_CLASS = xivclient.AkatsukiNoteString
    DATA_TYPE: str = model.DataTypes.CODEX

    @classmethod
    def format_headers(cls, headers):
        if headers:
            val ='\n'.join(headers)
            return html.h1(html.replace_new_lines(val))
        
        return ''

    @classmethod
    def get_all(cls, row=None):

        # Unending codex is all in one big file, with text split into the rows
        # we want to extract separate models for each "entry" in the journal 

        headers = []
        for row in super().get_data(row):
            if not row.Text:
                continue 

            # the only way to check what is text vs title is to see if there is punctuation
            if '.' in row.Text:

                yield model.SearchItem(
                    row_id=row.row_id,
                    key=f'{row.row_id}',
                    name=headers[0],
                    text_html=cls.format_headers(headers[1:]) + html.p(html.replace_new_lines(row.Text)),
                    text_clean=row.Text,
                    datatype=cls.DATA_TYPE
                )

                headers = []

            else:
                headers.append(row.Text)


class BalloonAdapter(DataAdapter):
    DATA_CLASS = xivclient.Balloon
    DATA_TYPE: str = model.DataTypes.BALLOON

    @classmethod
    def get_name(cls, data):
        return "Balloon Text"
    
    @classmethod
    def get_search_text(cls, data):
        return _scrub.remove_non_ascii(data.Dialogue)
    
    @classmethod
    def get_pretty_text(cls, data):
        return html.p(_scrub.replace_new_lines(data.Dialogue))


class NpcYellAdapter(DataAdapter):
    DATA_CLASS = xivclient.Balloon
    DATA_TYPE: str = model.DataTypes.BALLOON

    @classmethod
    def get_name(cls, data):
        return "NPC Yell"
    
    @classmethod
    def get_search_text(cls, data):
        return _scrub.remove_non_ascii(data.Text)
    
    @classmethod
    def get_pretty_text(cls, data):
        return html.p(_scrub.replace_new_lines(data.Text))


class AdventureAdapter(DataAdapter):
    DATA_CLASS = xivclient.Adventure
    DATA_TYPE: str = model.DataTypes.LOOKOUT

    @classmethod
    def get_meta(cls, data: xivclient.Adventure):
        return {
            "place_name": data.PlaceName.Name if data.PlaceName else None
        }

    @classmethod
    def get_name(cls, data: xivclient.Adventure):
        return data.Level.EventId.Name
    
    @classmethod
    def get_search_text(cls, data: xivclient.Adventure):
        return _scrub.remove_non_ascii(data.Description) + " " + _scrub.remove_non_ascii(data.Impression)
    
    @classmethod
    def get_pretty_text(cls, data: xivclient.Adventure):
        return html.p(data.Impression) + html.h1('Description') + html.p(data.Description)


__all__ = [
    MountAdapter,
    FishAdapter,
    FateAdapter,
    FateEventAdapter,
    TripleTriadCardAdapter,
    StatusAdapter,
    CutsceneAdapter,
    CustomTextAdapter,
    ItemAdapter,
    UnendingCodexAdapter,
    BalloonAdapter,
    NpcYellAdapter,
    AdventureAdapter,
    QuestAdapter,
]
