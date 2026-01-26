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
        return f'<p>{cls.replace_new_lines(text)}</p>\n\n'
        
    @classmethod
    def br(cls):
        return '<br/>\n'
    
    @classmethod
    def replace_new_lines(cls, text):
        if not text:
            return text 
        
        return text.replace('\n', cls.br())
    
html = HtmlBuilder

def get_expansion_number(name: str): 
    if name:
        exp = model.EXPANSIONS_LOOKUP.get(name.lower(), None)
        return exp.num if exp else None
    
    return None

def extract_unique_speakers(text_tuples):
    return set(speaker for speaker, _ in text_tuples)

def prettify_dialogue(text_tuples):
    return html.br().join(
        [
            html.h1(speaker) + html.p(text)
            for speaker, text 
            in text_tuples
        ]
    )

def clean_dialogue(text_tuples):
    text_string = ' '.join([speaker + ' ' + text for speaker, text in text_tuples])
    return _scrub.clean_text(text_string)

class DataAdapter:
    DATA_CLASS: Type[xivclient.XivModel] = None
    DATA_TYPE: str = model.DataTypes.QUEST

    @classmethod
    def should_include_model(cls, data):
        return True

    @classmethod
    def get_all(cls, row=None) -> Iterator[model.SearchItem]:

        for data in cls.get_data(row):
            if cls.should_include_model(data):
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
        return html.p(data.Description)
    
    @classmethod
    def get_search_text(cls, data: xivclient.XivModel):
        return _scrub.clean_text(data.Description)

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

class TextFileDataAdapter(DataAdapter):
    parsed_text = None
    
    @classmethod
    def map_model(cls, data):
        cls.parsed_text = _scrub.parse_speaker_lines(data._sheet_rows)
        return super().map_model(data)
    
    @classmethod
    def get_speakers(cls, data):
        return extract_unique_speakers(cls.parsed_text)

    @classmethod
    def get_search_text(cls, data):
        return clean_dialogue(cls.parsed_text)
    
    @classmethod
    def get_pretty_text(cls, data):
        return prettify_dialogue(cls.parsed_text)

class QuestAdapter(TextFileDataAdapter):
    DATA_CLASS = xivclient.Quest
    DATA_TYPE: str = model.DataTypes.QUEST

    @classmethod
    def get_expansion_name(cls, data: xivclient.Quest):
        return data.Expansion.Name.lower() if data.Expansion.Name else None
    
    @classmethod
    def get_key(cls, data: xivclient.Quest):
        return data._sheet_name
    
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
        return html.p((
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


class CutsceneAdapter(TextFileDataAdapter):
    DATA_CLASS = xivclient.CutsceneText
    DATA_TYPE: str = model.DataTypes.CUTSCENE

    @classmethod
    def get_expansion_name(cls, data):
        return data._expansion.lower() if data._expansion else None
    
    @classmethod
    def get_key(cls, data: xivclient.XivModel):
        return data._sheet_name

class CustomTextAdapter(TextFileDataAdapter):
    DATA_CLASS = xivclient.CustomText
    DATA_TYPE: str = model.DataTypes.CUSTOM
    parsed_text = None

    @classmethod
    def get_name(cls, data: xivclient.CustomText):
        return data.Type or "Custom Text"

    @classmethod
    def get_key(cls, data: xivclient.CustomText):
        return data.Name

class UnendingCodexAdapter(DataAdapter):
    DATA_CLASS = xivclient.AkatsukiNoteString
    DATA_TYPE: str = model.DataTypes.CODEX

    @classmethod
    def format_headers(cls, headers):
        if headers:
            val = html.br().join(headers)
            return html.h1(val)
        
        return ''

    @classmethod
    def get_all(cls, row=None):

        # Unending codex is all in one big file, with text split into the rows
        # we want to extract separate models for each "entry" in the journal 

        entry = model.UnendingCodexEntry()
        for row in super().get_data(row):
            if not row.Text:
                continue 

            # the only way to check what is text vs title is to see if there is punctuation
            if '.' in row.Text:
                entry.text = row.Text

                yield model.SearchItem(
                    row_id=row.row_id,
                    key=f'{row.row_id}',
                    name=entry.title,
                    text_html=cls.format_headers(entry.headers) + html.p(entry.text),
                    text_clean=_scrub.clean_text(entry.text),
                    datatype=cls.DATA_TYPE
                )

                entry = model.UnendingCodexEntry()

            else:
                entry.add_header(row.Text)


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
        return html.p(data.Dialogue)


class NpcYellAdapter(DataAdapter):
    DATA_CLASS = xivclient.NpcYell
    DATA_TYPE: str = model.DataTypes.NPCYELL

    @classmethod
    def should_include_model(cls, data):
        return data.Text != '0'

    @classmethod
    def get_name(cls, data):
        return "NPC Yell"
    
    @classmethod
    def get_search_text(cls, data):
        return _scrub.remove_non_ascii(data.Text)
    
    @classmethod
    def get_pretty_text(cls, data):
        return html.p(data.Text)


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

class DescriptionPageAdapter(DataAdapter):
    DATA_CLASS = xivclient.DescriptionPage
    DATA_TYPE: str = model.DataTypes.DESCRIPTION

    @classmethod
    def get_name(cls, data):
        return next((t.Text for t in data.Text if t.Text))
    
    @classmethod
    def get_search_text(cls, data: xivclient.DescriptionPage):
        return _scrub.remove_non_ascii(' '.join((t.Text for t in data.Text if t.Text)))
    
    @classmethod
    def get_pretty_text(cls, data: xivclient.DescriptionPage):
        if len(data.Text) > 1:
            return html.br().join((html.p(t.Text) for t in data.Text[1:] if t.Text))
        
        return html.p(data.Text[0].Text)

class MYCWarResultNotebookAdapter(DataAdapter):
    DATA_CLASS = xivclient.MYCWarResultNotebook
    DATA_TYPE = model.DataTypes.BOZJA_NOTES

class MKDLoreAdapter(DataAdapter):
    DATA_CLASS = xivclient.MKDLore
    DATA_TYPE = model.DataTypes.OCCULT_RECORD
    
class VVDNotebookContentsAdapter(DataAdapter):
    DATA_CLASS = xivclient.VVDNotebookContents
    DATA_TYPE = model.DataTypes.VARIANT_DUNGEON

__all__ = [
    MountAdapter,
    # FishAdapter,
    FateAdapter,
    FateEventAdapter,
    TripleTriadCardAdapter,
    StatusAdapter,
    CustomTextAdapter,
    ItemAdapter,
    UnendingCodexAdapter,
    BalloonAdapter,
    NpcYellAdapter,
    AdventureAdapter,
    MYCWarResultNotebookAdapter,
    MKDLoreAdapter,
    VVDNotebookContentsAdapter,
    CutsceneAdapter,
    QuestAdapter,
]
