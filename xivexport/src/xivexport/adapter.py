from typing import Iterator, Type
from . import model, _scrub, xivclient
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel(logging.DEBUG)


class DataAdapter:
    DATA_CLASS: Type[xivclient.XivModel] = None

    @classmethod
    def get_all(cls, row=None) -> Iterator[model.SearchItem]:

        for data in cls.get_data(row):
            try:
                result = cls.map_model(data)
                if not result.text:  # ignore items without text to search
                    continue
                yield result
            except Exception as e:
                LOGGER.error("failed to map data into search model", exc_info=e)

    @classmethod
    def get_data(cls, row=None) -> Iterator[xivclient.XivModel]:
        return xivclient.XivDataAccess.get_all(cls.DATA_CLASS, row)

    @classmethod
    def map_model(cls, data: xivclient.XivModel) -> model.SearchItem:
        pass


class QuestAdapter(DataAdapter):
    DATA_CLASS = xivclient.Quest

    @classmethod
    def map_model(cls, data: xivclient.Quest) -> model.SearchItem:

        key = data.Id or ""

        prev_quest = data.PreviousQuest[0] if data.PreviousQuest else None

        return model.Quest(
            row_id=data.row_id,
            name=data.Name or "",
            key=key,
            expansion=data.Expansion.Name.lower() if data.Expansion.Name else None,
            text=data.Text or "",
            meta=model.QuestMeta(
                previous_quest=prev_quest and prev_quest.Name,
                issuer=data.IssuerStart and data.IssuerStart.Singular,
                place_name=data.PlaceName and data.PlaceName.Name,
                journal_genre=data.JournalGenre and data.JournalGenre.Name,
                filename=key,
            ),
        )


class ItemAdapter(DataAdapter):
    DATA_CLASS = xivclient.Item

    @classmethod
    def map_model(cls, data: xivclient.Item) -> model.SearchItem:

        return model.Item(
            row_id=data.row_id,
            key=str(data.row_id),
            name=data.Name or "",
            text=data.Description or data.Name,
            meta=model.ItemMeta(
                category=data.ItemUICategory.Name or "",
            ),
        )


class MountAdapter(DataAdapter):
    DATA_CLASS = xivclient.Mount

    @classmethod
    def map_model(cls, data: xivclient.Mount) -> model.SearchItem:

        text = (
            f"{data.Description}\n\n{data.DescriptionEnhanced}\n\nTooltip:\n{data.Tooltip}"
            if data.Tooltip
            else f"{data.Description}\n\n{data.DescriptionEnhanced}"
        )

        return model.Mount(
            row_id=data.row_id,
            key=str(data.row_id),
            text=text,
            name=data.Singular.title(),
        )


class FishAdapter(DataAdapter):
    DATA_CLASS = xivclient.FishParameter

    @classmethod
    def map_model(cls, data: xivclient.FishParameter) -> model.SearchItem:

        return model.Fish(
            row_id=data.row_id,
            key=str(data.row_id),
            name=data.Item.Name,
            text=data.Text,
        )


class FateAdapter(DataAdapter):
    DATA_CLASS = xivclient.Fate

    @classmethod
    def map_model(cls, data: xivclient.Fate) -> model.SearchItem:

        return model.Fate(
            row_id=data.row_id,
            key=str(data.row_id),
            name=data.Name,
            text=data.Description,
        )


class TripleTriadCardAdapter(DataAdapter):
    DATA_CLASS = xivclient.TripleTriadCard

    @classmethod
    def map_model(cls, data: xivclient.TripleTriadCard) -> model.SearchItem:

        return model.TripleTriadCard(
            row_id=data.row_id,
            key=str(data.row_id),
            name=data.Name,
            text=data.Description,
        )


class StatusAdapter(DataAdapter):
    DATA_CLASS = xivclient.Status

    @classmethod
    def map_model(cls, data: xivclient.Status) -> model.SearchItem:

        return model.Status(
            row_id=data.row_id,
            key=str(data.row_id),
            name=data.Name,
            text=data.Description,
        )


class CutsceneAdapter(DataAdapter):
    DATA_CLASS = xivclient.CutsceneText

    @classmethod
    def map_model(cls, data: xivclient.CutsceneText) -> model.SearchItem:

        return model.Cutscene(
            row_id=data.row_id,
            key=data.key,
            name=data.Name,
            text=data.Text,
            expansion=data.expansion.lower() if data.expansion else None,
        )


class CustomTextAdapter(DataAdapter):
    DATA_CLASS = xivclient.CustomText

    @classmethod
    def map_model(cls, data: xivclient.CustomText) -> model.SearchItem:

        return model.CustomText(
            row_id=data.row_id, key=data.key, name=data.Name, text=data.Text
        )


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
