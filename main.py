import IA
from FightEngine import fight
from pokemon.Pokemon import *

if __name__ == '__main__':

    pokemon = create_user_pokemon()
    contrincant = create_pokemon(IA.int_poke())

    fight(pokemon, contrincant)


