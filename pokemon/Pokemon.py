

# Create the class
class Pokemon:

    def set_health(self):
        health = ''
        for i in range(self.bars):
            health += '='
        return health



    def __init__(self, name, types, moves, attack, defense):
        # save variables as attributes
        self.name = name
        self.types = types
        self.moves = moves
        self.attack = attack
        self.defense = defense
        self.bars = 20  # Amount of health bars
        self.health = self.set_health()



