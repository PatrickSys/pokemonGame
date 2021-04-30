import random
import requests
import json
from pokemon.moves import Moves


class Pokemon:

    def __init__(self, name, types, moves, hp, attack, defense, speed, strengths, weaknesses):
        # save variables as attributes
        self.name = name
        self.types = types
        self.moves = moves
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.bars = 20.0  # Amount of health bars
        self.health = self.set_health()
        self.speed = speed
        self.strengths = strengths
        self.weaknesses = weaknesses

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


    # Attack pokemon function, where manages PP left, calculates damage,
    # crit chance, miss chance, and takes in count types advantages

    def do_attack(self, move, contrincant):

        if no_pp_left(move):
            print("No PP left!")
            return

        waste_pp(move)

        if move_heals(move):
            self.bars += 2

        if move_doesnt_miss(move):
            crit = move_crits()

            # damage calculation
            damage = abs(crit * ((self.attack * move.power * 50) - (
                    (contrincant.hp / 4.5) * (contrincant.defense * 35)))) / 52500

            if move_is_strong_against(move, contrincant):
                print("\nIt's super effective!")
                damage *= 1.5

            if move_is_weak_against(move, contrincant):
                print("\nIt's not very effective...")
                damage *= 0.5

            effect_damage(damage, contrincant)

        else:
            return self.attack_missed()


    # sets health string in correlation with bars attribute
    def set_health(self):
        health = ''
        for i in range(int(self.bars)):
            health += '='
        return health


def no_pp_left(move):
    if move.get_pp() <= 0:
        return True
    else:
        return False


def move_heals(move):
    if "healing" in move.get_category():
        return True
    else:
        return False


def waste_pp(move):
    move.set_pp(move.get_pp() - 1)

# random miss chance
def move_doesnt_miss(move):
    miss_chance = random.randint(0, 100)
    if miss_chance <= move.get_accuracy():
        return True
    else:
        return False

# Calculates random crit chance
def move_crits():
    crit_chance = random.randint(0, 100)
    if crit_chance <= 6:
        print("\nCritical Strike! ")
        return 2
    else:
        return 1


def move_is_strong_against(move, contrincant):
    if move.get_type() in contrincant.get_weaknesses():
        return True
    else:
        return False


def move_is_weak_against(move, contrincant):
    if move.get_type() in contrincant.get_strengths():
        return True
    else:
        return False


def effect_damage(damage, contrincant):
    contrincant.bars -= damage
    contrincant.health = contrincant.set_health()


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


def generate_moves(pokemon):
    moves = []
    for i in range(4):
        for k in range(len(pokemon['moves'])):
            rand = random.randrange(len(pokemon['moves']))
            if pokemon['moves'][rand]['move']['name'] not in moves:
                new_move = Moves.create_mov(pokemon, rand)
                moves.append(new_move)
                break

    return moves


def set_stats(pokemon):
    hp = 3 * (pokemon['stats'][0]['base_stat'])
    attack = pokemon['stats'][1]['base_stat']
    defense = pokemon['stats'][2]['base_stat']
    speed = pokemon['stats'][5]['base_stat']

    return [hp, attack, defense, speed]


def create_pokemon():
    # Ask the pokemon to be created
    pokemon_required = ask_pokemon()

    # Get API data for the pokemon
    pokemon = get_pokemon_data(pokemon_required)

    # Start getting wanted data
    name = pokemon['name'].capitalize()

    # Get pokemon strengths and weaknesses based on it's type
    [types, strengths, weaknesses] = get_weaknessses_and_strengths(pokemon)

    # Array of moves, gets 4 random moves on the pokemon selected
    moves = generate_moves(pokemon)

    # gets return of stats as an array
    [hp, attack, defense, speed] = set_stats(pokemon)

    return Pokemon(name, types, moves, hp, attack, defense, speed, strengths, weaknesses)
