from typing import Optional
from pydantic import BaseModel

class DataTypes:
    QUEST = 'quest'
    CUTSCENE = 'cutscene'    
    ITEM = 'item'
    FISH = 'fish'
    MOUNT = 'mount'
    TRIPLETRIAD = 'triple triad card'
    CUSTOM = 'npc talk'
    CODEX = 'unending codex'
    BALLOON = 'balloon text' 
    NPCYELL = 'npc yell' 
    LOOKOUT = 'lookout' 
    BOZJA_NOTES = 'bozja note' 
    OCCULT_RECORD = 'occult record'
    VARIANT_DUNGEON = 'variant record'
    SNIPE_TALK = 'snipe text'  
    MINION = 'minion' 
    LEVE = 'leve'
    FATE = 'fate'
    FATE_EVENT = 'fate npc'
    CE_DEVELOPMENT_LOG = 'cosmic exploration log'
    CE_MISSION = 'cosmic exploration mission'
    SYSTEM_DESCRIPTION = 'system description'
    GIMMICK_BILL = 'dungeon text'

    # not uploaded currently
    STATUS = 'status'

    
TYPE_CATEGORIES = {
    "collection": [
        DataTypes.BOZJA_NOTES,
        DataTypes.OCCULT_RECORD,
        DataTypes.SYSTEM_DESCRIPTION,
        DataTypes.CODEX,
        DataTypes.LOOKOUT,
        DataTypes.VARIANT_DUNGEON,        
        DataTypes.CE_DEVELOPMENT_LOG
    ],
    "npc dialogue": [
        DataTypes.NPCYELL,
        DataTypes.BALLOON,
        DataTypes.SNIPE_TALK,
        DataTypes.CUSTOM,
        DataTypes.FATE_EVENT
    ],
    "items": [
        DataTypes.FISH,
        DataTypes.TRIPLETRIAD,
        DataTypes.MINION,
        DataTypes.MOUNT,
        DataTypes.ITEM
    ],
    # "system": [
    #     DataTypes.STATUS
    # ],
    "quest": [
        DataTypes.QUEST,
        DataTypes.FATE,
        DataTypes.LEVE,
        DataTypes.CE_MISSION
    ],
    "story": [
        DataTypes.CUTSCENE
    ],
    "environment": [
        DataTypes.GIMMICK_BILL
    ]
}

CATEGORY_LOOKUP = {
    t: k
    for k, v in TYPE_CATEGORIES.items()
    for t in v
}

class Expansion (BaseModel):
    num: int 
    name: str
    abbr: str

class DataType(BaseModel):
    category: str 
    name: str

    @staticmethod
    def from_type_name(name: str):
        return DataType(
            name=name,
            category=CATEGORY_LOOKUP[name]
        )

EXPANSIONS = (
    Expansion(num=1, name="a realm reborn", abbr="ARR"),
    Expansion(num=2, name="heavensward", abbr="HW"),
    Expansion(num=3, name="stormblood", abbr="STB"),
    Expansion(num=4, name="shadowbringers", abbr="SHB"),
    Expansion(num=5, name="endwalker", abbr="EW"),
    Expansion(num=6, name="dawntrail", abbr="DT")
)

EXPANSIONS_LOOKUP = {
    e.name.lower() : e
    for e in EXPANSIONS
}


class SearchItem(BaseModel):
    row_id: int
    key: str
    title: Optional[str] = None 
    text: str 
    datatype: DataType
    expansion: Optional[Expansion] = None
    speakers: Optional[list] = None
    meta: Optional[object] = None

    def plain_meta_data(self):
        if not self.meta:
            return ''
        
        if self.datatype.name == DataTypes.QUEST:
            return f"""
```
Issuer: {self.meta.issuer} [{self.meta.place_name}]
Journal: {self.meta.journal_genre} [{self.expansion.name.title()}]
```
"""
        return ""
    
    def as_plain_text(self):

        return f"""
---

# {self.title or self.datatype.name.title()}

[{self.datatype.name.upper()}]
{self.plain_meta_data()}
{self.text}
"""

class QuestMeta(BaseModel):
    journal_genre: Optional[str] = None
    issuer: Optional[str] = None
    place_name: Optional[str] = None
    previous_quest: Optional[str] = None
    filename: Optional[str] = None

class Quest(SearchItem):
    datatype: str = DataTypes.QUEST

class ItemMeta(BaseModel):
    category: str = None


class UnendingCodexEntry:

    def __init__(self):
        self.title = None
        self.headers = []
        self.text = None

    def add_header(self, text):
        if not self.title:
            self.title = text

        else:
            self.headers.append(text)