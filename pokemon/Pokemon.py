import random
import requests
import json

# Create the class
from pokemon.moves import Moves


class Pokemon:

    def set_health(self):
        health = ''
        for i in range(self.bars):
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
        self.bars = 20  # Amount of health bars
        self.health = self.set_health()
        self.speed = speed


def create_pokemon():
    # Ask the pokemon to be made
    pokemon_required = str(input("Which pokemon is selected?\t")).lower()

    # Get API data for the pokemon
    resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_required}")
    pokemon = json.loads(resp.text)

    # Start getting wanted data
    name = pokemon['name'].capitalize()
    print(name)

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

    hp = pokemon['stats'][0]['base_stat']
    attack = pokemon['stats'][1]['base_stat']
    defense = pokemon['stats'][2]['base_stat']
    speed = pokemon['stats'][5]['base_stat']

    return Pokemon(name, types, moves, hp, attack, defense, speed)
