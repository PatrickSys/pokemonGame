import random
import FightEngine
from pokemon.Pokemon import get_pokemon_data


# Returns a random pokemon as IA creation,
# takes probability of stronger or weaker pokemon than the user
def int_poke(user_pokemon):
    poke_number = random.randint(1, 898)
    pokemon = get_pokemon_data(poke_number)

    if pokemon['moves'] == 0:
        return int_poke(user_pokemon)

    if user_pokemon_is_legend(user_pokemon, pokemon):
        return int_poke(user_pokemon)

    if stronger_pokemon_chance(user_pokemon, pokemon):
        if check_avantage(pokemon, user_pokemon):
            return poke_number
        else:
            return int_poke(user_pokemon)

    elif equal_pokemon_chance(user_pokemon, pokemon):
        if check_avantage(pokemon, user_pokemon):
            return poke_number
        else:
            return int_poke(user_pokemon)
    else:
        if check_avantage(pokemon, user_pokemon):
            return poke_number
        else:
            return int_poke(user_pokemon)


def check_avantage(ia_pokemon, user_pokemon):
    return ia_pokemon['types'][0]['type']['name'] or ia_pokemon['types'][1]['type'][
        'name'] in user_pokemon.get_weaknesses()


def stronger_pokemon_chance(user_pokemon, ia_pokemon):
    return random.randint(0, 100) > 30 and ia_pokemon['base_experience'] > user_pokemon.get_base_xp()


def equal_pokemon_chance(user_pokemon, ia_pokemon):
    return random.randint(0, 100) > 30 and user_pokemon.get_base_xp() + 20 > ia_pokemon[
        'base_experience'] > user_pokemon.get_base_xp() - 20


def user_pokemon_is_legend(user_pokemon, ia_pokemon):
    return user_pokemon.get_base_xp() > 250 != ia_pokemon['base_experience'] < 250


def ia_turn(pokemon, contrincant):
    int_move = 0
    max_damage = 0
    counter = 0
    for x in pokemon.moves:

        damage = abs(((pokemon.get_attack() * pokemon.moves[counter].power * 50) - (
                (contrincant.hp / 4.5) * (contrincant.defense * 35)))) / 72500
        if FightEngine.move_is_strong_against(x, contrincant):
            damage *= 2
        if FightEngine.move_is_weak_against(x, contrincant):
            damage *= 0.5
        if damage > max_damage:
            actual_max = counter
            int_move -= int_move
            int_move += actual_max
            max_damage = damage

        counter += 1
    return FightEngine.turn(pokemon, pokemon.get_moves()[int_move], contrincant)
