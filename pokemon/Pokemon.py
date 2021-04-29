import random
import requests
import json
from pokemon.moves import Moves


class Pokemon:

    def set_health(self):
        health = ''
        for i in range(int(self.bars)):
            health += '='
        return health

    def __init__(self, name, types, moves, hp, attack, defense, speed):
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

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense




    def do_attack(self, move, contrincant):
        miss_chance = random.randint(0, 100)
        crit_chance = random.randint(0, 100)
        crit = 1

        if miss_chance <= move.get_accuracy():
            if crit_chance <= 6:
                crit = 2
                print("Critical Strike! ")

            damage = abs(crit * (((self.attack * 5) * (move.power * 35)) - ((contrincant.hp / 8) * (contrincant.defense * 30)))) / 50250
            print(damage, " dmg")
            print(((crit * (((self.attack * 5) * (move.power * 35)) - ((contrincant.hp / 8) * (contrincant.defense * 30)))) / 50250), "real")
            effect_damage(damage, contrincant)

        else:
            return self.get_name() + "miss the attack"


def effect_damage(damage, contrincant):

    contrincant.bars -= damage
    contrincant.health = contrincant.set_health()




def create_pokemon():
    # Ask the pokemon to be made
    pokemon_required = str(input("Which pokemon is selected?\t")).lower()

    # Get API data for the pokemon
    resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_required}")
    pokemon = json.loads(resp.text)

    # Start getting wanted data
    name = pokemon['name'].capitalize()

    # Array of types
    types = []

    for i in range(len(pokemon['types'])):
        types.append(pokemon['types'][i]['type']['name'])

    # Array of moves, gets 4 random moves on the pokemon selected

    moves = []
    for i in range(4):
        for k in range(len(pokemon['moves'])):
            rand = random.randrange(len(pokemon['moves']))
            if pokemon['moves'][rand]['move']['name'] not in moves:
                new_move = Moves.create_mov(pokemon, rand)
                moves.append(new_move)
                break

    # stat 0 hp 1 attack 2 defense 5 speed

    hp = 3 * (pokemon['stats'][0]['base_stat'])
    attack = pokemon['stats'][1]['base_stat']
    defense = pokemon['stats'][2]['base_stat']
    speed = pokemon['stats'][5]['base_stat']

    return Pokemon(name, types, moves, hp, attack, defense, speed)
