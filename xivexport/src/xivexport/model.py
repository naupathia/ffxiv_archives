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

def expansion_name_from_number(number: int):
    if number == 2:
        return "A Realm Reborn"
    if number == 3:
        return "Heavensward"
    if number == 4:
        return "Stormblood"
    if number == 5:
        return "Shadowbringers"
    if number == 6:
        return "Endwalker"
    if number == 7:
        return "Dawntrail"
    
    return ""


class CutsceneKey:
    def __init__(self, sheet_name: str):        
        # example sheet name: cut_scene/034/VoiceMan_03401
        tokens = sheet_name.split('/')
        expansion = tokens[1]
        expansion_num = int(expansion[:2])

        self.key = tokens[2]
        self.row_id = int(self.key.split('_')[1])
        self.patch_num = f'{expansion_num}.{expansion[2]}'
        self.expansion = expansion_name_from_number(expansion_num)


class CustomTextKey:
    def __init__(self, sheet_name: str):        
        # example sheet name: custom/009/RegYok6BreathBetween_00906
        tokens = sheet_name.split('/')

        self.key = tokens[2]
        self.row_id = int(tokens[1])

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

class Quest(SearchItem):
    datatype: str = DataTypes.QUEST
    journal_genre: str = None
    issuer: str = None
    place_name: str = None
    previous_quest: str = None
    
    def as_plain_text(self):

        return f"""
---------------------------------------------------------------------
[QUEST]
 
{self.name}
Issuer: {self.issuer} [{self.place_name}]
Journal: {self.journal_genre} [{self.expansion}]

{self.text}

"""

class Item(SearchItem):
    datatype: str = DataTypes.ITEM
    category: str = None

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

