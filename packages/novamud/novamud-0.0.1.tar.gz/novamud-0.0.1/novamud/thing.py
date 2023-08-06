
# global counter for things
count = 0


class Thing:

    id = None
    name = 'Thing'
    description = 'you need to describe the thing'
    # the player currently holding the thing
    held_by = None

    def __init__(self):
        global count
        count += 1
        self.id = '{}_{}'.format(self.name, count)

    def picked_up_by(self, player):
        pass

    def dropped_by(self, player):
        pass
