import json

import requests


class Moves:

    def __init__(self, accuracy, name, category, power, pp, priority):
        self.accuracy = accuracy
        self.name = name
        self.category = category
        self.power = power
        self.pp = pp
        self.priority = priority

    def getname(self):
        return self.name

    def create_mov(pokemon, rand):
        get_moves = requests.get(pokemon['moves'][rand]['move']['url'])
        mov = json.loads(get_moves.text)
        accuracy = mov['accuracy']
        mov_name = pokemon['moves'][rand]['move']['name']
        category = mov['meta']['category']['name']
        mov_power = mov['power']
        mov_pp = mov['pp']
        mov_priority = mov['priority']
        return Moves(accuracy, mov_name, category, mov_power, mov_pp, mov_priority)
