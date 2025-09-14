from typing import AsyncIterator, List, Type
from . import xivclient, model, _scrub


def get_quest_folder_number(key: str):
    key_tokens = key.split("_")
    return key_tokens[1][0:3]


class DataAdapter:
    data_class: Type[xivclient.XivModel]

    @classmethod
    async def get_all(cls, row=None) -> List[model.SearchItem]:
        results = []
        async for data in cls.get_data(row):
            result = await cls.map_model(data)
            results.append(result)
        return results

    @classmethod
    async def get_data(cls, row=None) -> AsyncIterator[xivclient.XivModel]:
        async with xivclient.XivApiClient() as client:
            async for item in client.sheet(cls.data_class, [row] if row else None):
                yield item

    @classmethod
    async def map_model(cls, data: xivclient.XivModel) -> model.SearchItem:
        pass


class QuestAdapter(DataAdapter):
    model_class = xivclient.Quest

    @classmethod
    async def map_model(cls, data: xivclient.Quest) -> model.SearchItem:

        if not data.Name:  # Only include quests with names
            return None

        key = data.Id or ""
        quest_text = ""

        if not key:
            return None

        else:
            quest_folder = get_quest_folder_number(key)
            quest_text = await xivclient.XivDataService.get_sheet_data_as_text(
                f"quest/{quest_folder}/{key}"
            )

        prev_quest = data.PreviousQuest[0] if data.PreviousQuest else {}

        return model.Quest(
            row_id=data.row_id,
            name=data.Name,
            key=key,
            expansion=data.Expansion.Name,
            text=quest_text,
            previous_quest=prev_quest.Name,
            issuer=data.IssuerStart.Singular,
            place_name=data.PlaceName.Name,
            journal_genre=data.JournalGenre.Name,
        )


class ItemAdapter(DataAdapter):
    model_class: xivclient.Item

    @classmethod
    async def map_model(cls, data: xivclient.Item) -> model.SearchItem:

        return model.Item(
            name=data.Name,
            text=_scrub.sanitize_text(data.Description),
            key=data.row_id,
            category=data.ItemUICategory.Name,
        )


class MountAdapter(DataAdapter):
    model_class: xivclient.Mount

    @classmethod
    async def map_model(cls, data: xivclient.Mount) -> model.SearchItem:

        async with xivclient.XivApiClient() as client:
            mount_transient = await client.sheet(
                xivclient.MountTransient, rows=[data.row_id]
            )

        mount_transient = mount_transient[0]

        text = (
            f"{mount_transient.Description}\n{mount_transient.DescriptionEnhanced}\n\n*Tooltip*:\n {mount_transient.Tooltip}"
            if mount_transient.Tooltip
            else mount_transient.Description
        )

        return model.Mount(
            row_id=data.row_id, key=str(data.row_id), text=text, name=data.Name
        )


class FishAdapter(DataAdapter):
    model_class: xivclient.FishParameter

    @classmethod
    async def map_model(cls, data: xivclient.FishParameter) -> model.SearchItem:

        return model.Fish(
            row_id=data.row_id,
            key=str(data.row_id),
            name=data.Item.Name,
            text=data.Text,
        )


class FateAdapter(DataAdapter):
    model_class: xivclient.Fate

    @classmethod
    async def map_model(cls, data: xivclient.Fate) -> model.SearchItem:

        return model.Fate(
            row_id=data.row_id,
            key=str(data.row_id),
            name=data.Name,
            text=data.Description,
        )


class TripleTriadCardAdapter(DataAdapter):
    model_class: xivclient.TripleTriadCard

    @classmethod
    async def map_model(cls, data: xivclient.TripleTriadCard) -> model.SearchItem:

        return model.TripleTriadCard(
            row_id=data.row_id,
            key=str(data.row_id),
            name=data.Name,
            text=data.Description,
        )


class StatusAdapter(DataAdapter):
    model_class: xivclient.Status

    @classmethod
    async def map_model(cls, data: xivclient.Status) -> model.SearchItem:

        return model.Status(
            row_id=data.row_id,
            key=str(data.row_id),
            name=data.Name,
            text=data.Description,
        )


class CutsceneAdapter(DataAdapter):
    model_class: None

    @classmethod
    async def get_data(cls, row=None):

        count = 0

        async with xivclient.XivApiClient() as client:

            for sheet_name in await client.sheets():
                if not sheet_name:
                    continue

                if not sheet_name.startswith("cut_scene"):
                    continue

                # example sheet name: cut_scene/034/VoiceMan_03401
                key = model.CutsceneKey(sheet_name)

                cutscene_text = await client.get_sheet_data_as_text(sheet_name, 4)

                yield xivclient.SheetParseData(
                    row_id=key.row_id,
                    key=key.key,
                    Text=cutscene_text,
                    Name=f"{key.patch_num} {key.expansion} Cutscenes",
                    expansion=key.expansion,
                )

                count += 1

                if count >= row:
                    break

    @classmethod
    async def map_model(cls, data: xivclient.SheetParseData) -> model.SearchItem:

        return model.Cutscene(
            row_id=data.row_id,
            key=data.key,
            name=data.Name,
            text=data.Text,
            expansion=data.expansion,
        )


class CustomTextAdapter(DataAdapter):
    model_class: None

    @classmethod
    async def get_data(cls, row=None):

        count = 0

        async with xivclient.XivApiClient() as client:

            for sheet_name in await client.sheets():
                if not sheet_name:
                    continue

                if not sheet_name.startswith("custom"):
                    continue

                # example sheet name: custom/009/RegYok6BreathBetween_00906
                key = model.CustomTextKey(sheet_name)

                text = await client.get_sheet_data_as_text(sheet_name, 4)

                yield xivclient.SheetParseData(
                    row_id=key.row_id, key=key.key, Text=text, Name=key.key
                )

                count += 1

                if count >= row:
                    break

    @classmethod
    async def map_model(cls, data: xivclient.SheetParseData) -> model.SearchItem:

        return model.CustomText(
            row_id=data.row_id, key=data.key, name=data.Name, text=data.Text
        )
