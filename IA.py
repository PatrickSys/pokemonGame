import random
import FightEngine

from pokemon import Pokemon


def int_poke():
    return random.randint(1, 898)


def ia_attack(pokemon, contrincant):
    int_move = 0
    max_damage = 0
    counter = 0
    for x in pokemon.moves:
        if FightEngine.move_is_strong_against(x, contrincant):
            damage = abs(((pokemon.get_attack() * pokemon.moves[counter].power * 50) - (
                    (contrincant.hp / 4.5) * (contrincant.defense * 35)))) / 52500

            if damage > max_damage:
                int_move = counter
        counter = counter + 1
    return FightEngine.turn(pokemon, pokemon.get_moves()[int_move], contrincant)
