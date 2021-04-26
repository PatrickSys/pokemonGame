from FightEngine import fight
from pokemon.Pokemon import create_pokemon

if __name__ == '__main__':

    pokemon = create_pokemon()
    contrincant = create_pokemon()

    fight(pokemon, contrincant)


