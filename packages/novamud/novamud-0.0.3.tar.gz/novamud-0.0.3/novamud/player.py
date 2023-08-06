import asyncio


class Player:

    # string name, guaranteed to be unique
    name = None

    # the room that the player is currently in
    current_room = None

    # the python websocket through which you can communicate
    client = None

    # the clothing that the player is currently wearing
    clothing = None

    # what the user is currently carrying
    carrying = None

    def __init__(self, name):
        self.name = name

    async def _tell(self, msg):
        await self.client.send(msg + '\n')

    def tell(self, msg):
        asyncio.ensure_future(self._tell(msg))
