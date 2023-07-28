from survivpy import Client, TimeRange, GameMode
import asyncio

client = Client()

async def main():
    player = await client.search("classyclass", time_range=TimeRange.Daily, game_mode=GameMode.All)
    print(player.username, player.overview)

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
