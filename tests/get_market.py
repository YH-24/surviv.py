from survivpy import Client
import asyncio

client = Client()

async def main():
    items = await client.get_market(limit=3)
    print([item.name for item in items])

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
