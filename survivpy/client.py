import re
import time
import aiohttp
import asyncio

from .enums import *
from .utils import *
from .models import *


class Client:
    """
    A class used to represent a Client

    ...

    Attributes
    ----------
    http : HTTP
        Stores the ClientSession and HTTP config
    Methods
    -------
    search(query: str, time_range = AllTime, game_mode = All)
        Return a Player object from request
    get_matches(query: str, time_range = AllTime, game_mode = All)
        Return a Player object from request
    """

    def __init__(self):
        self.http = self.HTTP()

    async def search(self, query: str, time_range: TimeRange = TimeRange.AllTime, game_mode: GameMode = GameMode.All) -> Player:
        username = query.replace(" ", "-")
        payload = {"slug": f"{username}", "interval": f"{time_range.value}", "mapIdFilter": f"{game_mode.value}"}

        async with self.http._session.post('https://surviv.io/api/user_stats', json=payload) as res:
            if res.status == 200:
                data = await res.json()
                player = Player(data)

                player.matches = await self.get_matches(username)

                return player

    async def get_matches(self, query: str = None, limit: int = 10, team_mode: TeamMode = TeamMode.All) -> list:
        username = query.replace(" ", "-")  # In case user directly calls get_matches() without search()
        payload = {"slug": f"{username}", "count": f"{limit}", "offset": "0", "teamModeFilter": f"{team_mode.value}"}

        async with self.http._session.post('https://surviv.io/api/match_history', json=payload) as res:
            if res.status == 200:
                matches = await res.json()
                return [Match(match) for match in matches]

            return []

    async def get_modes(self) -> GameModes:
        async with self.http._session.get('https://surviv.io/api/site_info?language=en') as res:
            if res.status == 200:
                data = await res.json()

                return GameModes(data)

    async def get_region_stats(self) -> RegionStats:
        async with self.http._session.get('https://surviv.io/api/site_info?language=en') as res:
            if res.status == 200:
                data = (await res.json())["pops"]

                return RegionStats(data)

    async def get_market(self, rarity: ItemRarity = ItemRarity.All, type: ItemType = ItemType.All, limit: int = 25, include_done: bool = False) -> list:
        payload = {"rarity": f"{rarity.value}", "type": f"{type.value}"}

        async with self.http._session.post('https://surviv.io/api/user/market/get_market_available_items', json=payload) as res:
            if res.status == 200:
                items = (await res.json())["items"]
                market_list = []
                for item in items:
                    item = MarketItem(item)
                    if item.done:
                        if include_done:
                            market_list.append(item)

                        continue

                    market_list.append(item)

                return market_list[:limit]

            return []

    async def get_leaderboard(self, time_range: TimeRange = TimeRange.Daily, mode: GameMode = GameMode.Classic, team_mode: TeamMode = TeamMode.Solo, limit: int = 50) -> list:
        payload = {"interval": f"{time_range.value}", "mapId": f"{mode.value}", "maxCount": f"100", "teamMode": f"{team_mode.name}".lower(), "type": f"most_kills"}

        async with self.http._session.post('https://surviv.io/api/leaderboard', json=payload) as res:
            if res.status == 200:
                players = await res.json()
                leaderboard = [LeaderboardPlayer(player) for player in players]

                return leaderboard[:limit]

            return []


    class HTTP:
        def __init__(self):
            async def runner():
                try:
                    self._session = aiohttp.ClientSession(headers=self.headers, cookies=self.cookies)
                except Exception as e:
                    print(e)

            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(runner())

        @property
        def headers(self):
            return {"content-type": "application/json; charset=utf-8", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}

        @property
        def cookies(self):
            return {"app-sid": f"SID_HERE"}
            # Uses a burner account to access market


