from ._tools import Timer
from typing import Iterator, Type
from . import model, _scrub, xivclient
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.INFO)

md = _scrub.md

def get_expansion_number(name: str):
    if name:
        exp = model.EXPANSIONS_LOOKUP.get(name.lower(), None)
        return exp.num if exp else None

    return None


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
                    if (
                        not result.text or not result.text.strip()
                    ):  # ignore items without text to search
                        continue

                    LOGGER.debug(f"succesfully mapped {cls.__name__}: {data.row_id}")
                    yield result
                except Exception as e:
                    LOGGER.error("Failed to map data into search model", exc_info=e)
                    raise

            else:
                LOGGER.debug(f"skipping model for {cls.__name__}: {data.row_id}")

    @classmethod
    def get_data(cls, row=None) -> Iterator[xivclient.XivModel]:
        return xivclient.XivDataAccess.get_all(cls.DATA_CLASS, row)

    @classmethod
    def get_key(cls, data: xivclient.XivModel):
        name = cls.get_name(data) or ""

        if name:
            return name.lower().replace(" ", "_")

        return str(data.row_id)

    @classmethod
    def get_name(cls, data):
        return data.Name or ""

    @classmethod
    def get_text(cls, data):
        return data.Description

    @classmethod
    def get_pretty_text(cls, data: xivclient.XivModel):
        return md.p(cls.get_text(data))

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
            row_id=data.row_id,
            key=cls.get_key(data),
            title=cls.get_name(data),
            text=cls.get_pretty_text(data),  # if this is empty should raise error
            expansion=cls.get_expansion(data),
            speakers=cls.get_speakers(data),
            meta=cls.get_meta(data),
            datatype=model.DataType.from_type_name(cls.DATA_TYPE),
        )


class TextFileDataAdapter(DataAdapter):
    speaker_pos = 3

    @classmethod
    def get_speakers(cls, data):
        return None

    @classmethod
    def get_pretty_text(cls, data):
        return _scrub.parse_speaker_lines(data._sheet_rows, cls.speaker_pos)


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
    def get_text(cls, data):
        return data.Description or "No description given"

    @classmethod
    def get_meta(cls, data: xivclient.Item):
        # if data.ItemUICategory:
        #     return model.ItemMeta(
        #         category=data.ItemUICategory.Name or "",
        #     )
        return None


class MountAdapter(DataAdapter):
    DATA_CLASS = xivclient.Mount
    DATA_TYPE: str = model.DataTypes.MOUNT

    @classmethod
    def get_name(cls, data: xivclient.Mount):
        return data.Singular.title()

    @classmethod
    def get_text(cls, data):
        return f"{data.Description} {data.DescriptionEnhanced} {data.Tooltip}"

    @classmethod
    def get_pretty_text(cls, data):

        tooltip = ""
        if data.Tooltip:
            tooltip = md.blockquote(data.Tooltip)

        return tooltip + md.p(data.Description) + md.p(data.DescriptionEnhanced)


class FishAdapter(DataAdapter):
    DATA_CLASS = xivclient.FishParameter
    DATA_TYPE: str = model.DataTypes.FISH

    @classmethod
    def get_name(cls, data: xivclient.FishParameter):
        return data.Item.Name

    @classmethod
    def get_text(cls, data: xivclient.FishParameter):
        return data.Text


class FateAdapter(DataAdapter):
    DATA_CLASS = xivclient.Fate
    DATA_TYPE: str = model.DataTypes.FATE


class FateEventAdapter(DataAdapter):
    DATA_CLASS = xivclient.FateEvent
    DATA_TYPE: str = model.DataTypes.FATE_EVENT

    @classmethod
    def get_name(cls, data):
        return None

    @classmethod
    def get_text(cls, data: xivclient.FateEvent):

        lines = [line for line in data.Text if line]

        return "\n".join(lines)


class TripleTriadCardAdapter(DataAdapter):
    DATA_CLASS = xivclient.TripleTriadCard
    DATA_TYPE: str = model.DataTypes.TRIPLETRIAD


class StatusAdapter(DataAdapter):
    DATA_CLASS = xivclient.Status
    DATA_TYPE: str = model.DataTypes.STATUS


class CutsceneAdapter(TextFileDataAdapter):
    DATA_CLASS = xivclient.CutsceneText
    DATA_TYPE: str = model.DataTypes.CUTSCENE
    speaker_pos = 4

    @classmethod
    def get_expansion_name(cls, data):
        return data._expansion

    @classmethod
    def get_key(cls, data: xivclient.XivModel):
        return data._sheet_name


class CustomTextAdapter(TextFileDataAdapter):
    DATA_CLASS = xivclient.CustomText
    DATA_TYPE: str = model.DataTypes.CUSTOM

    @classmethod
    def get_name(cls, data: xivclient.CustomText):
        return data.Type or None

    @classmethod
    def get_key(cls, data: xivclient.CustomText):
        return data.Name


class UnendingCodexAdapter(DataAdapter):
    DATA_CLASS = xivclient.AkatsukiNoteString
    DATA_TYPE: str = model.DataTypes.CODEX

    @classmethod
    def format_headers(cls, headers):
        if headers:
            return '\n'.join((md.h3(h) for h in headers)) + md.br()

        return ""

    @classmethod
    def get_all(cls, row=None):

        # Unending codex is all in one big file, with text split into the rows
        # we want to extract separate models for each "entry" in the journal

        entry = model.UnendingCodexEntry()
        for row in super().get_data(row):
            if not row.Text:
                continue

            # the only way to check what is text vs title is to see if there is punctuation
            if "." in row.Text:
                entry.text = row.Text

                yield model.SearchItem(
                    row_id=row.row_id,
                    key=f"{row.row_id}",
                    title=entry.title,
                    text=cls.format_headers(entry.headers) + md.p(entry.text),
                    datatype=model.DataType.from_type_name(cls.DATA_TYPE),
                )

                entry = model.UnendingCodexEntry()

            else:
                entry.add_header(row.Text)


class BalloonAdapter(DataAdapter):
    DATA_CLASS = xivclient.Balloon
    DATA_TYPE: str = model.DataTypes.BALLOON

    @classmethod
    def get_name(cls, data):
        return None

    @classmethod
    def get_text(cls, data):
        return data.Dialogue


class NpcYellAdapter(DataAdapter):
    DATA_CLASS = xivclient.NpcYell
    DATA_TYPE: str = model.DataTypes.NPCYELL

    @classmethod
    def should_include_model(cls, data):
        return data.Text != "0"

    @classmethod
    def get_name(cls, data):
        return None

    @classmethod
    def get_text(cls, data):
        return data.Text


class AdventureAdapter(DataAdapter):
    DATA_CLASS = xivclient.Adventure
    DATA_TYPE: str = model.DataTypes.LOOKOUT

    @classmethod
    def get_meta(cls, data: xivclient.Adventure):
        return {"place_name": data.PlaceName.Name if data.PlaceName else None}

    @classmethod
    def get_name(cls, data: xivclient.Adventure):
        return data.Level.EventId.Name

    @classmethod
    def get_pretty_text(cls, data: xivclient.Adventure):
        return md.p(data.Impression) + md.h3("Description") + md.p(data.Description)


class DescriptionPageAdapter(DataAdapter):
    DATA_CLASS = xivclient.DescriptionPage
    DATA_TYPE: str = model.DataTypes.SYSTEM_DESCRIPTION

    @classmethod
    def should_include_model(cls, data):
        return cls.get_name(data)

    @classmethod
    def get_name(cls, data: xivclient.DescriptionPage):
        return next((t.Text for t in data.Text if t.Text), "")

    @classmethod
    def get_text(cls, data: xivclient.DescriptionPage):
        if len(data.Text) > 1:
            return "\n".join((t.Text for t in data.Text[1:] if t.Text))

        return data.Text[0].Text

    @classmethod
    def get_pretty_text(cls, data: xivclient.DescriptionPage):
        if len(data.Text) > 1:
            return md.br().join((md.p(t.Text) for t in data.Text[1:] if t.Text))

        return md.p(data.Text[0].Text)


class MYCWarResultNotebookAdapter(DataAdapter):
    DATA_CLASS = xivclient.MYCWarResultNotebook
    DATA_TYPE = model.DataTypes.BOZJA_NOTES


class MKDLoreAdapter(DataAdapter):
    DATA_CLASS = xivclient.MKDLore
    DATA_TYPE = model.DataTypes.OCCULT_RECORD


class VVDNotebookContentsAdapter(DataAdapter):
    DATA_CLASS = xivclient.VVDNotebookContents
    DATA_TYPE = model.DataTypes.VARIANT_DUNGEON


class WKSPioneeringTrailStringAdapter(DataAdapter):
    DATA_CLASS = xivclient.WKSPioneeringTrailString
    DATA_TYPE = model.DataTypes.CE_DEVELOPMENT_LOG

    @classmethod
    def get_name(cls, data):
        return data.DevelopmentLogText + ": " + data.DevelopmentLogName

    @classmethod
    def get_text(cls, data):
        return data.DevelopmentLogDescription


class WKSMissionTextAdapter(DataAdapter):
    DATA_CLASS = xivclient.WKSMissionText
    DATA_TYPE = model.DataTypes.CE_MISSION

    @classmethod
    def get_name(cls, data):
        return f"Cosmic Exploration Mission {data.row_id}"

    @classmethod
    def get_text(cls, data):
        return data.Text


class SpearfishingItemAdapter(DataAdapter):
    DATA_CLASS = xivclient.SpearfishingItem
    DATA_TYPE = model.DataTypes.FISH

    @classmethod
    def get_name(cls, data):
        return data.Item.Name

    @classmethod
    def get_pretty_text(cls, data):
        return md.blockquote(data.Description) + md.p(data.Item.Description)


class SnipeTalkAdapter(DataAdapter):
    DATA_CLASS = xivclient.SnipeTalk
    DATA_TYPE = model.DataTypes.SNIPE_TALK

    @classmethod
    def should_include_model(cls, data):
        return data.Text and data.Name.Name

    @classmethod
    def get_name(cls, data):
        return None

    @classmethod
    def get_text(cls, data):
        return data.Name.Name + " " + data.Text

    @classmethod
    def get_pretty_text(cls, data):
        return md.h3(data.Name.Name) + md.p(data.Text)


class CompanionAdapter(DataAdapter):
    DATA_CLASS = xivclient.Companion
    DATA_TYPE = model.DataTypes.MINION

    @classmethod
    def get_name(cls, data: xivclient.Companion):
        return data.Singular.title()

    @classmethod
    def get_text(cls, data):
        return f"{data.Description} {data.DescriptionEnhanced} {data.Tooltip}"

    @classmethod
    def get_pretty_text(cls, data):

        tooltip = ""
        if data.Tooltip:
            tooltip = md.blockquote(data.Tooltip)

        return tooltip + md.p(data.Description) + md.p(data.DescriptionEnhanced)


class LeveAdapter(DataAdapter):
    DATA_CLASS = xivclient.Leve
    DATA_TYPE = model.DataTypes.LEVE

    @classmethod
    def get_meta(cls, data: xivclient.Leve):
        return {"place_name": data.PlaceNameIssued and data.PlaceNameIssued.Name}


__all__ = [
    CustomTextAdapter,
    CutsceneAdapter,
    MountAdapter,
    CompanionAdapter,
    FishAdapter,
    FateAdapter,
    FateEventAdapter,
    TripleTriadCardAdapter,
    # StatusAdapter, # not needed
    ItemAdapter,
    UnendingCodexAdapter,
    DescriptionPageAdapter,
    BalloonAdapter,
    NpcYellAdapter,
    AdventureAdapter,
    MYCWarResultNotebookAdapter,
    MKDLoreAdapter,
    VVDNotebookContentsAdapter,
    WKSPioneeringTrailStringAdapter,
    WKSMissionTextAdapter,
    SpearfishingItemAdapter,
    SnipeTalkAdapter,
    LeveAdapter,
    QuestAdapter,
]
