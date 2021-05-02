import json
import random

import requests

moves_learnt = []


class Moves:

    def __init__(self, accuracy, name, category, type, power, pp, priority, healing):
        self.accuracy = accuracy
        self.name = name
        self.category = category
        self.type = type
        self.power = power
        self.pp = pp
        self.priority = priority
        self.total_pp = pp
        self.healing = healing

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

    def get_total_pp(self):
        return self.total_pp

    def get_healing(self):
        return self.healing


def move_already_learnt(mov_name):
    return mov_name in moves_learnt


def pokemon_can_learn_less_than_4_moves(pokemon):
    return len(pokemon['moves']) < 4


def create_mov(pokemon, rand):
    move = requests.get(pokemon['moves'][rand]['move']['url'])
    mov = json.loads(move.text)

    mov_name = pokemon['moves'][rand]['move']['name'].replace("-", " ")

    if move_already_learnt(mov_name) != pokemon_can_learn_less_than_4_moves(pokemon):
        return create_mov(pokemon, random.randrange(len(pokemon['moves'])))
    moves_learnt.append(mov_name)

    mov_power = mov['power']
    if mov_power is None:
        mov_power = 35
    if mov_power < 35:
        return create_mov(pokemon, random.randrange(len(pokemon['moves'])))
    accuracy = mov['accuracy']

    if accuracy is None:
        accuracy = 100

    category = mov['meta']['category']['name']

    mov_pp = mov['pp']
    mov_priority = mov['priority']
    type = mov['type']['name']
    healing = mov['meta']['healing']
    return Moves(accuracy, mov_name, category, type, mov_power, mov_pp, mov_priority, healing)
