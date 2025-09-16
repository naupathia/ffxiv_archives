from typing import Any, Optional
from pydantic import BaseModel

class DataTypes:
    QUEST = 'quest'
    ITEM = 'item'
    CUTSCENE = 'cutscene'
    FATE = 'fate'
    FISH = 'fish'
    MOUNT = 'mount'
    STATUS = 'status'
    TRIPLETRIAD = 'card'
    CUSTOM = 'custom'

class SearchItem(BaseModel):
    row_id: int
    key: str
    name: str 
    text: str 
    datatype: str
    expansion: str = None
    rank: int = 0

    def remote_id(self):
        return f"{self.datatype}_{self.key}_{self.row_id}"
    
    def as_plain_text(self):

        return f"""
---------------------------------------------------------------------
[{self.datatype.upper()}]

{self.name}

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
    meta: QuestMeta    
    
    def as_plain_text(self):

        return f"""
---------------------------------------------------------------------
[QUEST]
 
{self.name} [{self.key}]
Issuer: {self.meta.issuer} [{self.meta.place_name}]
Journal: {self.meta.journal_genre} [{self.expansion}]

{self.text}

"""

class ItemMeta(BaseModel):
    category: str = None


class Item(SearchItem):
    datatype: str = DataTypes.ITEM
    meta: ItemMeta

class Cutscene(SearchItem):
    datatype: str = DataTypes.CUTSCENE

class Fate(SearchItem):
    datatype: str = DataTypes.FATE

class Fish(SearchItem):
    datatype: str = DataTypes.FISH

class Mount(SearchItem):
    datatype: str = DataTypes.MOUNT

class Status(SearchItem):
    datatype: str = DataTypes.STATUS

class TripleTriadCard(SearchItem):
    datatype: str = DataTypes.TRIPLETRIAD

class CustomText(SearchItem):
    datatype: str = DataTypes.CUSTOM

