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

    def do_attack(self, move, contrincant):
        miss_chance = random.randint(0, 100)
        crit_chance = random.randint(0, 100)
        crit = 1


        if move.get_pp() == 0:
            print("no PP left")
            return

        if move.get_category() == "healing":
            self.bars += 2

        move.set_pp(move.get_pp()-1)
        if miss_chance <= move.get_accuracy():
            if crit_chance <= 6:
                crit = 2
                print("\nCritical Strike! ")


            damage = abs(crit * ((self.attack * move.power * 50) - ((contrincant.hp / 4.5) * (contrincant.defense * 35)))) / 52500

            #print(damage, "here")
            if move.get_type() in contrincant.get_weaknesses():
                print("\nIt's supper effective!")
                damage *= 1.5

            if move.get_type() in contrincant.get_strengths():
                print("\nIt's not very effective...")
                damage *= 0.5

            #print(damage, " dmg\n")
            #print(((crit * ((self.attack * move.power * 50) - ((contrincant.hp / 4.5) * (contrincant.defense * 35)))) / 52500), "real")
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


    return Pokemon(name, types, moves, hp, attack, defense, speed, strengths, weaknesses)
