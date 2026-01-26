from typing import Any, Optional
from pydantic import BaseModel, Field

class DataTypes:
    QUEST = 'quest'
    ITEM = 'item'
    CUTSCENE = 'cutscene'
    FATE = 'fate'
    FATE_EVENT = 'fate event'
    FISH = 'fish'
    MOUNT = 'mount'
    STATUS = 'status'
    TRIPLETRIAD = 'triple triad card'
    CUSTOM = 'custom'
    CODEX = 'unending codex'
    BALLOON = 'balloon'
    NPCYELL = 'npc yell'
    LOOKOUT = 'lookout'


class Expansion (BaseModel):
    num: int 
    name: str
    abbr: str

EXPANSIONS = (
    Expansion(num=1, name="A Realm Reborn", abbr="ARR"),
    Expansion(num=2, name="Heavensward", abbr="HW"),
    Expansion(num=3, name="Stormblood", abbr="STB"),
    Expansion(num=4, name="Shadowbringers", abbr="SHB"),
    Expansion(num=5, name="Endwalker", abbr="EW"),
    Expansion(num=6, name="Dawntrail", abbr="DT")
)

EXPANSIONS_LOOKUP = {
    e.name.lower() : e
    for e in EXPANSIONS
}


class SearchItem(BaseModel):
    row_id: int
    key: str
    name: str 
    text_html: str 
    text_clean: str
    datatype: str
    expansion: Optional[Expansion] = None
    speakers: Optional[list] = None
    meta: Optional[object] = None

    def remote_id(self):
        return f"{self.datatype}_{self.key}_{self.row_id}"
    
    def get_doc_id(self):
        return f"{self.datatype}-{self.row_id}"
    
    def as_plain_text(self):

        return f"""
---------------------------------------------------------------------
[{self.datatype.upper()}]

{self.name}

{self.text_html}

"""

class QuestMeta(BaseModel):
    journal_genre: Optional[str] = None
    issuer: Optional[str] = None
    place_name: Optional[str] = None
    previous_quest: Optional[str] = None
    filename: Optional[str] = None

class Quest(SearchItem):
    datatype: str = DataTypes.QUEST
    
    def as_plain_text(self):

        return f"""
---------------------------------------------------------------------
[QUEST]
 
{self.name} [{self.key}]
Issuer: {self.meta.issuer} [{self.meta.place_name}]
Journal: {self.meta.journal_genre} [{self.expansion.name}]

{self.text_html}

"""

class ItemMeta(BaseModel):
    category: str = None


