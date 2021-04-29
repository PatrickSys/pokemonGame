import json

import requests


class Moves:

    def __init__(self, accuracy, name, category, type, power, pp, priority):
        self.accuracy = accuracy
        self.name = name
        self.category = category
        self.type = type
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

    def set_pp(self, pp):
        self.pp = pp

    def get_category(self):
        return self.category
    def get_type(self):
        return self.type

    def create_mov(pokemon, rand):
        get_moves = requests.get(pokemon['moves'][rand]['move']['url'])
        mov = json.loads(get_moves.text)
        accuracy = mov['accuracy']
        if accuracy is None:
            accuracy = 100
        mov_name = pokemon['moves'][rand]['move']['name']
        category = mov['meta']['category']['name']
        mov_power = mov['power']
        if mov_power is None:
            mov_power = 35
        mov_pp = mov['pp']
        mov_priority = mov['priority']
        type = mov['type']['name']
        print(mov_name, type)
        return Moves(accuracy, mov_name, category, type, mov_power, mov_pp, mov_priority)
