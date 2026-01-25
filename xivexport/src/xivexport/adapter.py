from typing import Iterator, Type
from . import model, _scrub, xivclient
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)


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
                if not result.textHtml:  # ignore items without text to search
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
        return '<p>' + cls.get_search_text(data) + "</p>"
    
    @classmethod
    def get_search_text(cls, data: xivclient.XivModel):
        return data.Description or ""

    @classmethod
    def get_meta(cls, data: xivclient.XivModel):
        return None
    
    @classmethod
    def get_expansion(cls, data: xivclient.XivModel):
        return None
    
    @classmethod
    def get_speakers(cls, data: xivclient.XivModel):
        return None
    
    @classmethod
    def map_model(cls, data: xivclient.XivModel) -> model.SearchItem:

        return model.SearchItem(            
            row_id=data.row_id,
            key=cls.get_key(data),
            name=cls.get_name(data),
            textHtml=cls.get_pretty_text(data),
            textClean=cls.get_search_text(data),
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
    def get_expansion(cls, data: xivclient.Quest):
        if data.Expansion.Name:
            return model.EXPANSIONS_LOOKUP.get(data.Expansion.Name.lower(), None)
        
        return None
    
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
        return (
            f"{data.Description}\n\n{data.DescriptionEnhanced}\n\nTooltip:\n{data.Tooltip}"
            if data.Tooltip
            else f"{data.Description}\n\n{data.DescriptionEnhanced}"
        )
    
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
    def get_expansion(cls, data: xivclient.CutsceneText):
        if data.expansion:
            return model.EXPANSIONS_LOOKUP.get(data.expansion.lower(), None)
        
        return None
    
    @classmethod
    def get_speakers(cls, data: xivclient.CutsceneText):
        return cls.LINE_PARSER.get_speakers(data.TextLines)

    @classmethod
    def get_search_text(cls, data: xivclient.CutsceneText):
        return cls.LINE_PARSER.get_search_text(data.TextLines)
    
    @classmethod
    def get_pretty_text(cls, data: xivclient.CutsceneText):
        return cls.LINE_PARSER.get_pretty_text(data.TextLines)
    

class CustomTextAdapter(DataAdapter):
    DATA_CLASS = xivclient.CustomText
    DATA_TYPE: str = model.DataTypes.CUSTOM
    LINE_PARSER = TextLinesParser()

    @classmethod
    def get_search_text(cls, data):
        return data.Text

    
    @classmethod
    def get_speakers(cls, data: xivclient.CutsceneText):
        return cls.LINE_PARSER.get_speakers(data.TextLines)

    @classmethod
    def get_search_text(cls, data: xivclient.CutsceneText):
        return cls.LINE_PARSER.get_search_text(data.TextLines)
    
    @classmethod
    def get_pretty_text(cls, data: xivclient.CutsceneText):
        return cls.LINE_PARSER.get_pretty_text(data.TextLines)

__all__ = [
    QuestAdapter,
    MountAdapter,
    FishAdapter,
    FateAdapter,
    TripleTriadCardAdapter,
    StatusAdapter,
    CutsceneAdapter,
    CustomTextAdapter,
    ItemAdapter,
]
