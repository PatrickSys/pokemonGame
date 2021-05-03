import math
import random
import re

import requests
import json

from pokemon.moves import Moves, create_mov


class Pokemon:

    def __init__(self, name, types, moves, hp, attack, defense, speed, strengths, weaknesses, base_xp):
        # save variables as attributes
        self.name = name
        self.types = types
        self.moves = moves
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.bars = 20.0  # Amount of health bars
        self.health = self.convert_bars_to_health()
        self.speed = speed
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.base_xp = base_xp

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_weaknesses(self):
        return self.weaknesses

    def get_strengths(self):
        return self.strengths

    def get_speed(self):
        return self.speed

    def attack_missed(self):
        return self.get_name() + "missed the attack!"

    def get_bars(self):
        return self.bars

    def set_bars(self, bars):
        self.bars = bars

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health

    def is_not_dead(self):
        return self.bars > 0

    def get_moves(self):
        return self.moves

    def get_types(self):
        return self.types

    def get_base_xp(self):
        return self.base_xp

    # Attack pokemon function, where manages PP left, calculates damage,
    # crit chance, miss chance, and takes in count types advantages

    # sets health string in correlation with bars attribute
    def convert_bars_to_health(self):
        health = ''
        for i in range(int(math.ceil(self.get_bars()))):
            health += '='
        return health


def no_pp_left(move):
    return move.get_pp() <= 0


def move_heals(move):
    return move.get_healing() > 0


def waste_pp(move):
    move.set_pp(move.get_pp() - 1)


# random miss chance
def move_doesnt_miss(move):
    miss_chance = random.randint(0, 100)
    return miss_chance <= move.get_accuracy()


# Calculates random crit chance
def move_crits():
    crit_chance = random.randint(0, 100)
    if crit_chance <= 6:
        print("\nCritical Strike! ")
        return 2
    else:
        return 1


def move_is_strong_against(move, contrincant):
    return move.get_type() in contrincant.get_weaknesses()


def move_is_weak_against(move, contrincant):
    return move.get_type() in contrincant.get_strengths()


def effect_damage(damage, contrincant):
    contrincant.set_bars(contrincant.get_bars() - damage)
    contrincant.set_health(contrincant.convert_bars_to_health())


def ask_pokemon():
    return str(input("Which pokemon is selected?\t")).lower()


def get_pokemon_data(pokemon):
    resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    return json.loads(resp.text)


def get_weaknessses_and_strengths(pokemon):
    # Array of types
    types = []
    strengths = []
    weaknesses = []

    # Start getting pokemon types data
    for i in range(len(pokemon['types'])):
        types.append(pokemon['types'][i]['type']['name'])
        response = requests.get(pokemon['types'][i]['type']['url'])
        damage_relations = json.loads(response.text)

        # Append pokemon type strengths
        for j in range(len(damage_relations['damage_relations']['double_damage_to'])):
            strengths.append(damage_relations['damage_relations']['double_damage_to'][j]['name'])

        # Append pokemon type weaknesses
        for k in range(len(damage_relations['damage_relations']['double_damage_from'])):
            weaknesses.append(damage_relations['damage_relations']['double_damage_from'][k]['name'])

    return [types, strengths, weaknesses]


# and len(pokemon['moves']) > 4

def generate_moves(pokemon):
    moves = []

    for i in range(4):
        for k in range(len(pokemon['moves'])):
            generate_move(pokemon, moves)
            break

    return moves

# Generates random moves for the pokemon given
def generate_move(pokemon, moves):
    rand = random.randrange(len(pokemon['moves']))
    new_move = create_mov(pokemon, rand)
    moves.append(new_move)



def set_stats(pokemon):
    hp = 3 * (pokemon['stats'][0]['base_stat'])
    attack = pokemon['stats'][1]['base_stat']
    defense = pokemon['stats'][2]['base_stat']
    speed = pokemon['stats'][5]['base_stat']

    return [hp, attack, defense, speed]

def create_user_pokemon():
    # Ask the pokemon to be created
    pokemon_input = ask_pokemon()
    return create_pokemon(pokemon_input)

def pokemon_has_no_moves(pokemon):
    return len((pokemon['moves'])) < 1

def create_pokemon(pokemon_required):

    # Get API data for the pokemon
    pokemon = get_pokemon_data(pokemon_required)

    if pokemon_has_no_moves(pokemon):
        return create_pokemon(random.randint(0, 898))

    # Start getting wanted data
    name = pokemon['name'].capitalize()

    # Get pokemon strengths and weaknesses based on it's type
    [types, strengths, weaknesses] = get_weaknessses_and_strengths(pokemon)

    # Array of moves, gets 4 random moves on the pokemon selected
    moves = generate_moves(pokemon)

    # gets return of stats as an array
    [hp, attack, defense, speed] = set_stats(pokemon)

    base_xp = pokemon['base_experience']

    return Pokemon(name, types, moves, hp, attack, defense, speed, strengths, weaknesses, base_xp)
