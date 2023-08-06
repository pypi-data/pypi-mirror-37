
class Room:

    description = "This is a default room description. Be sure to come up " \
                  "with something better for this or your players will be " \
                  "bored AF."

    # name of the room
    name = 'Default Room'

    # The dungeon that the room belongs to
    dungeon = None

    # a mapping from player names to player objects
    players = None

    # a mapping of thing ids to things
    things = None

    # map from room id to the room object
    connected_rooms = None

    # an array of the commands that you want to open up to the players
    commands = None

    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.players = {}
        self.things = {}
        self.connected_rooms = {}
        self.commands = [
            'pick_up',
            'drop',
            'describe_room',
            'list_things',
            'describe_thing',
            'go_to',
            'show_commands',
        ]
        self.commands += self.register_commands()
        self.init_room()

    def init_room(self):
        pass

    def register_commands(self):
        return []

    def connect_room(self, other_room):
        self.connected_rooms[other_room.name] = other_room
        other_room.connected_rooms[self.name] = self

    def disconnect_room(self, other_room):
        del self.connected_rooms[other_room.name]

    def broadcast(self, message, name=None):
        if name is not None:
            message = '{}: {}'.format(name, message)
        for player in self.players.values():
            player.tell(message)

    def kill_player(self, player):
        self.remove_player(player)
        self.dungeon.kill_player(player)

    def remove_player(self, player):
        del self.players[player.name]
        if player.carrying:
            self.drop(player)

    def add_player(self, player):
        self.players[player.name] = player
        player.tell('Welcome to the {} room'.format(self.name))
        self.describe_room(player)
        # self.describe_room(player)
        player.current_room = self

    def pick_up(self, player, thing_id):

        # Returns True if successfully picked up, False otherwise
        if thing_id not in self.things:
            player.tell('No such thing with id {}'.format(thing_id))
            return False
        else:
            thing = self.things[thing_id]
            player.carrying = thing
            thing.carried_by = player
            del self.things[thing_id]
            self.after_pick_up(player)
            player.tell('You have now picked up {}'.format(thing_id))
            return True

    def pick_up_describe(self):
        return """Pick up a thing by its ID"""

    def drop(self, player):
        if player.carrying is not None:
            thing = player.carrying
            player.carrying = None
            thing.carried_by = None
            self.things[thing.id] = thing
            self.broadcast('{} dropped {}'.format(player.name, thing.id))
        else:
            player.tell('You aint carrying nothin')

    def drop_describe(self):
        return "Drop the item you are currently carrying"

    def show_commands(self, player):
        desc_str = 'Room Commands:\n'
        for command in self.commands:
            desc_str += '{} - {}\n'.format(
                command,
                getattr(self, command + '_describe')(),
            )
        player.tell(desc_str)

    def show_commands_describe(self):
        return "Show all commands that are available to the room"

    def describe_room(self, player):
        desc_str = self.description
        desc_str += '\nContains {} players and {} items\n'.format(
            len(self.players), len(self.things)
        )
        # desc_str += '\nThings in room:\n'
        # for thing in self.things.values():
        #     desc_str += thing.id + ' ' + thing.description + '\n'

        desc_str += 'This room has doors to the following rooms:\n'
        for room_id in self.connected_rooms:
            desc_str += '{}\n'.format(room_id)
        player.tell(desc_str)

    def describe_room_describe(self):
        return """Describe all objects, things"""

    def list_things(self, player):
        msg = 'Things:\n'
        for thing in self.things:
            msg += '{}\n'.format(thing)
        player.tell(msg)

    def list_things_describe(self):
        return 'List all things that may be picked up in the room'

    def describe_thing(self, player, thing_id):
        player.tell(self.things[thing_id].long_description())

    def describe_thing_describe(self):
        return "List all things that are in the room"

    def go_to(self, player, other_room_name):
        self.remove_player(player)
        self.connected_rooms[other_room_name].add_player(player)

    def go_to_describe(self):
        return "Select a room to leave to"

    def after_pick_up(self, player):
        # called after a user pick something up
        pass

    def add_thing(self, thing):
        self.things[thing.id] = thing
