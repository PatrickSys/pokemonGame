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

    def get_name(self):
        return self.name

    def get_accuracy(self):
        return self.accuracy

    def get_pp(self):
        return self.pp

    def get_priority(self):
        return self.priority

    def get_power(self):
        return self.power

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
