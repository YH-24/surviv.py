from aenum import MultiValueEnum
from enum import Enum

class RegionName(Enum):
    NorthAmerica = "na"
    SouthAmerica = "sa"
    Europe = "eu"
    Asia = "as"
    Korea = "kr"

class LeaderboardType(Enum):
    MostKills = "most_kills"
    MostDamage = "most_damage_dealt"
    KillsPerGame = "kpg"
    TotalKills = "kills"
    TotalWins = "wins"

class TimeRange(Enum):
    AllTime = "alltime"
    Daily = "daily"
    Weekly = "weekly"


class TeamMode(Enum):
    Solo = 1
    Duo = 2
    Squad = 4

    All = 7  # ONLY FOR MATCH HISTORY


class GameMode(Enum):
    FiftyVFifty = 3
    FiftyVFiftyLastSacrifice = 14

    All = -1
    Classic = 0
    Desert = 1
    Woods = 2
    Potato = 4
    Savannah = 5
    Cobalt = 7

    Halloween = 6
    Snow = 8
    Valentine = 9
    SaintPatrick = 10
    Eggsplosion = 11
    May4th = 13

    Storm = 15
    Beach = 16
    Contact = 17
    Inferno = 18

class ItemType(MultiValueEnum):
    All = "all"
    Outfit = "outfit", "outfitx"
    Melee = "melee"
    Emote = "emote"
    DeathEffect = "deathEffect"
    Heal = "heal_effect"
    Boost = "boost_effect"

class ItemRarity(MultiValueEnum):
    All = "all"
    Epic = 3
    Mythic = 4
    Legend = 5, 6

