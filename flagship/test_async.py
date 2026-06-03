import asyncio
from asyncua import Client

async def test():
    url = "opc.tcp://localhost:4840"
    async with Client(url=url) as client:
        print("Connected successfully!")
        root = client.get_root_node()
        print(f"Root node: {root}")

asyncio.run(test())