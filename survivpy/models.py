import re
from time import time

from .utils import *
from .enums import *


class Player:
    def __init__(self, data: dict):
        self.username = data["username"]
        self.icon = data["player_icon"] if data["player_icon"] else "https://i.imgur.com/fyIElFW.png"
        self.banned = data["banned"]

        self.overview = Stats(data)

        self.solo = None
        self.duo = None
        self.squad = None

        self.matches = []

        for mode in data["modes"]:
            if not mode:
                continue
            stats = ModeStats(mode)
            self.__setattr__(f"{stats.mode.name}".lower(), stats)

    def __repr__(self):
        return f"<Player object at 0x{str(hex(id(self))).upper()[2:]} username={self.username}, overview={self.overview}, matches=[{self.matches[-1]}, ...]>"


class Stats:
    def __init__(self, data: dict):
        self.wins = int(data["wins"])
        self.kills = int(data["kills"])

        self.games = int(data["games"])
        self.kills_per_game = float(data["kpg"])

    def __repr__(self):
        return f"<Stats wins={self.wins}, kills={self.kills}, games={self.games}>"


class ModeStats(Stats):
    def __init__(self, data: dict):
        super().__init__(data)

        self.mode = TeamMode(data["teamMode"])

        self.win_percentage = float(data["winPct"])
        self.most_kills = int(data["mostKills"])

        self.most_damage = data["mostDamage"]
        self.average_damage = data["avgDamage"]

        self.average_survived = data["avgTimeAlive"]


class Match:
    def __init__(self, data: dict):
        self.id = data["guid"]
        self.region = data["region"]
        self.map = data["map_id"]
        self.mode = TeamMode(int(data["team_mode"]))
        self.team_size = int(data["team_count"])
        self.team_kills = int(data["team_kills"])

        self.rank = int(data["rank"])
        self.kills = int(data["kills"])
        self.damage_dealt = int(data["damage_dealt"])
        self.damage_taken = int(data["damage_taken"])

        self.end_time = data["end_time"]
        # self.time_alive = int(data["time_alive"])
        self.time_alive_seconds = int(data["time_alive"])

        self.data = None

    def __repr__(self):
        return f"<Match object at 0x{str(hex(id(self))).upper()[2:]} id={self.id}, rank={self.rank}, mode={self.mode.name}>"


class LeaderboardPlayer:
    def __init__(self, data: dict):
        self.username = data["username"]
        self.search_name = data["slug"]
        self.games = int(data["games"])
        self.region = RegionName(str(data["region"]))
        self.value = data["val"]

    def __repr__(self):
        return f"<LeaderboardPlayer username={self.username}, value={self.value}, region={self.region.name}>"


class MarketItem:
    def __init__(self, data: dict = None):
        self.id = int(data["itemId"])
        self.name = data["item"]
        self.maker = data["makr"]
        self.type = ItemType(data["type"])
        self.rarity = ItemRarity(data["rarity"])
        self.level = int(data["levels"])
        self.kills = int(data["kills"])
        self.wins = int(data["wins"])
        self.price = int(data["price"])
        self.time_listed = int(data["timePosted"])
        self.time_left = int(time()*1000) - self.time_listed
        self.done = self.time_left < 86400000

    def __repr__(self):
        return f"<MarketItem name={self.name}, maker={self.maker}, type={self.type.name}, rarity={self.rarity.name}>"


class GameModes:
    def __init__(self, data):
        modes = data["modes"]

        self.solo = [string_enum(mode["mapName"], GameMode, GameMode.Classic) for mode in data["modes"] if
                     int(mode["teamMode"]) == TeamMode.Solo.value]
        self.duo = [string_enum(mode["mapName"], GameMode, GameMode.Classic) for mode in data["modes"] if
                    int(mode["teamMode"]) == TeamMode.Duo.value]
        self.squad = [string_enum(mode["mapName"], GameMode, GameMode.Classic) for mode in data["modes"] if
                      int(mode["teamMode"]) == TeamMode.Squad.value]

    def __repr__(self):
        return f"<GameModes solo={self.solo}, duo={self.duo}, squad={self.squad}>"


class Region:
    def __init__(self, code: str, players: str):
        self.name = RegionName(code)
        self.code = code
        self.players = int(re.sub(r"[^0-9]", "", players))

    def __repr__(self):
        return f"<Region name={self.name.name}, players={self.players}>"


class RegionStats:
    def __init__(self, data: dict):
        self.na = Region
        self.sa = Region
        self.eu = Region
        self.__setattr__("as", Region)
        self.kr = Region

        for code, players in data.items():
            setattr(self, f"{code}", Region(code, players))

    def __repr__(self):
        return f"<RegionStats object at 0x{str(hex(id(self))).upper()[2:]} na={self.na}, sa={self.sa}, eu={self.eu}, as={getattr(self, 'as')}, kr={self.kr},>"

