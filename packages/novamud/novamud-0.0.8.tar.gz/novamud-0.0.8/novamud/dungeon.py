"""Server for multithreaded (asynchronous) chat application."""
import traceback
import asyncio
import websockets
import sys
from .player import Player


class Dungeon:

    name = 'Default Dungeon'
    description = 'Default description for a default dungeon... did you ' \
                  'forget to add a description?'

    server = None

    name2player = {}

    # the room where players start
    start_room = None

    host = None
    port = None

    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host or '0.0.0.0'
        self.port = port or 8080
        self.init_dungeon()

    def init_dungeon(self):
        pass

    async def get_player_name(self, websocket):
        askname = 'Please enter a name less than 8 chars long'
        await websocket.send(askname)
        while True:
            name = await websocket.recv()
            name = name.strip()
            if name == '':
                # If an empty string is entered, don't say anything
                # also has the added benefit of a keepalive ping working
                # without generating duplicate prompts
                continue
            await websocket.send(askname)
            if name in self.name2player:
                await websocket.send(
                    'Name is already taken, please choose a name that is not '
                    'already chosen. Chosen names are: {}'.format(
                        '\n'.join(self.name2player.keys())
                    )
                )
            elif len(name) == 0:
                await websocket.send('Please do be so kind as to enter a name')
            elif len(name) >= 8:
                await websocket.send('Name is too long')
            else:
                return name

    async def accept_connection(self, websocket, *_):
        print('new connection, waiting for the name')
        name = await self.get_player_name(websocket)
        print('{} has arrived!'.format(name))
        player = Player(name)
        player.client = websocket
        player.tell('Welcome to {}, {}'.format(self.name, player.name))
        player.tell(self.description)
        player.tell('Hope your are ready to start your adventure! '
                    'Hit the enter key to enter the first room and then and '
                    'then call "describe_room" and "show_commands" to get '
                    'started!')
        (await websocket.recv()).strip()
        self.add_player(player)
        while True:
            try:
                cmd = (await websocket.recv()).strip()
                self.process_command(player, cmd)
            except websockets.exceptions.ConnectionClosed:
                self.remove_player(player)
                # breaking here will cause the connection to be closed
                break
            except KeyboardInterrupt as e:
                print(traceback.format_exc())
                break
            except Exception:
                print(traceback.format_exc())
                continue

    def start_dungeon(self):
        if not self.start_room:
            raise RuntimeError('No start room defined')
        print('Server is up and running on {}:{}'.format(self.host, self.port))
        start_server = websockets.serve(
            self.accept_connection, self.host, self.port, timeout=60 * 60
        )

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def add_player(self, player):
        self.name2player[player.name] = player
        self.start_room.add_player(player)

    def remove_player(self, player):
        print('removing', player.name)
        player.current_room.remove_player(player)
        del self.name2player[player.name]

    def broadcast(self, msg, name=None):
        if name is not None:
            msg = '{}: {}'.format(name, msg)
        for player in self.name2player.values():
            player.tell(msg)

    def process_command(self, player, raw_cmd):
        if raw_cmd.strip() == '':
            return
        cmd, args = raw_cmd.split()[0], raw_cmd.split()[1:]
        if cmd == 'say':
            self.tell_room(player, raw_cmd[4:])
        elif cmd == 'say_dungeon':
            self.broadcast(raw_cmd[12:], name=player.name)
        else:
            self.forward_cmd_to_room(player, cmd, args)

    def tell_room(self, player, msg):
        player.current_room.broadcast(msg, name=player.name)

    def forward_cmd_to_room(self, player, cmd, args):
        if cmd in player.current_room.commands:
            getattr(player.current_room, cmd)(player, *args)
        else:
            player.tell('{} not available in room {}'.format(
                cmd, player.current_room.name)
            )

    def kill_player(self, player):
        player.tell('You have died and are being returned to the beginning.')
        player.current_room.remove_player(player)
        self.start_room.add_player(player)
