from FightEngine import fight
from pokemon.Pokemon import *

if __name__ == '__main__':

    pokemon = create_user_pokemon()
    contrincant = create_user_pokemon()

    fight(pokemon, contrincant)


