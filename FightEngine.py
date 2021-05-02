import sys
import time
import numpy as np
import IA

from pokemon.Pokemon import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def ident(tabs):
    identation = ""
    for i in range(tabs):
        identation = identation + '\t'
    return identation


# Print fight information
def print_header(pokemon, contrincant):
    print(
        bcolors.HEADER + "------------------------------------------POKEMON FIGHT!------------------------------------------\n" + bcolors.ENDC)
    print_versus(pokemon, contrincant)
    print_types(pokemon, contrincant)
    print_stat(f"HP/{ident(1)}", pokemon.get_hp(), f"{ident(4)}{contrincant.get_hp()}")
    print_stat("ATTACK/", pokemon.get_attack(), f"{ident(4)}{contrincant.get_attack()}")
    print_stat("DEFENSE/", pokemon.get_defense(), f"{ident(4)}{contrincant.get_defense()}")
    print_stat("SPEED/\t", pokemon.get_speed(), f"{ident(4)}{contrincant.get_speed()}")
    time.sleep(.2)


def print_versus(pokemon, contrincant):
    print(
        bcolors.WARNING + f"{ident(6)} {pokemon.get_name()} {ident(4)}" + bcolors.ENDC + bcolors.FAIL + "VS" + bcolors.WARNING +
        f"{ident(3)} {contrincant.get_name()}" + bcolors.ENDC)


def print_types(pokemon, contrincant):
    print(f"{bcolors.OKCYAN} TYPE/ {bcolors.ENDC} {ident(4)}", ', '.join(pokemon.get_types()), ident(6),
          ', '.join(contrincant.get_types()))


def print_stat(stat_name, pokemon_stat, contrincant_stat):
    print(f"{bcolors.OKCYAN} {stat_name} {bcolors.ENDC} {ident(4)}", pokemon_stat, ident(4), ' ', contrincant_stat)


# Delay printing
def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)


def print_health(pokemon, contrincant):
    print(f"\n{pokemon.get_name()}", f"HEALTH\t{bcolors.OKGREEN}{pokemon.get_health()}{bcolors.ENDC}".rjust(
        60 - len(pokemon.get_name()) -20, ' '))
    print(f"{contrincant.get_name()}", f"HEALTH\t{bcolors.OKGREEN}{contrincant.get_health()}{bcolors.ENDC}".rjust(
        60 - len(contrincant.get_name()) -20, ' '), '\n')


def print_moves(pokemon):
    print(f"Go {pokemon.get_name()}!")
    print(f'\n{moves_name_and_pp(pokemon)}\n')


def moves_name_and_pp(pokemon):
    moves = ''

    for i in range(len(pokemon.moves)):
        moves += f"[{pokemon.get_moves()[i].get_name()}][{print_in_color_on_low_pp(pokemon.get_moves()[i])} PP] \t"

    return moves


def print_in_color_on_low_pp(move):
    if no_pp_left(move):
        return move_in_red(move)

    if pp_at_50_percent(move):
        return move_in_yellow(move)
    else:
        return move.get_pp()


def pp_at_50_percent(move):
    return move.get_pp() < (move.get_total_pp() * 50 / 100)


def move_in_red(move):
    return f"{bcolors.FAIL}{move.get_pp()}{bcolors.ENDC}"


def move_in_yellow(move):
    return f"{bcolors.WARNING}{move.get_pp()}{bcolors.ENDC}"


def ask_move(pokemon):
    print_moves(pokemon)
    return int(input('Pick a move: '))


def calculate_move_effectiveness(move, contrincant):
    modifier = 1

    for i in range(len(contrincant.get_types())):
        if move_is_strong_against(move, contrincant):
            modifier *= 2

        if move_is_weak_against(move, contrincant):
            modifier *= 0.5

    return modifier


def do_attack(pokemon, move, contrincant):

    waste_pp(move)

    if move_heals(move):
        pokemon.set_bars(pokemon.get_bars() + move.get_healing()/15)
        pokemon.set_health(pokemon.convert_bars_to_health())

    if move_doesnt_miss(move):
        crit = move_crits()

        # damage calculation
        damage = abs(crit * ((pokemon.get_attack() * move.power * 50) - (
                (contrincant.hp / 4.5) * (contrincant.defense * 35)))) / 72500

        # calculates move damage multiplier based on efectiveness
        damage_modifier = calculate_move_effectiveness(move, contrincant)
        damage *= damage_modifier

        if damage_modifier > 1:
            print("\nIt's super effective!")
        elif damage_modifier < 1:
            print("\nIt's not very effective...")
        effect_damage(damage, contrincant)


    else:
        return pokemon.attack_missed()


# Allow two pokemon to fight each other
def user_turn(pokemon, contrincant):
    index = ask_move(pokemon)
    move = pokemon.get_moves()[index - 1]

    while no_pp_left(move):
        print(f"\n{bcolors.WARNING}No PP left!{bcolors.ENDC}")
        index = ask_move(pokemon)
        move = pokemon.get_moves()[index - 1]
    return turn(pokemon,move,contrincant)


def turn(pokemon, move, contrincant):
    delay_print(f"\n{pokemon.get_name()} used {move.get_name()}!")
    time.sleep(.1)

    # Determine damage
    do_attack(pokemon, move, contrincant)
    time.sleep(.5)

    # Check to see if Pokemon fainted
    if contrincant.get_bars() <= 0:
        print_health(pokemon, contrincant)
        delay_print("\n..." + contrincant.get_name() + ' fainted.')
        return -1


def ia_is_faster_than_pokemon(pokemon, ia):
    return ia.get_speed() > pokemon.get_speed()


def fight(pokemon, contrincant):

    print_header(pokemon, contrincant)


    # Continue while pokemon still have health
    if ia_is_faster_than_pokemon(pokemon, contrincant):
        ia_attacks_first(pokemon, contrincant)
    else:
        attack_turns(pokemon, contrincant)




def ia_attacks_first(pokemon, contrincant):
    money = np.random.choice(5000)
    while pokemon.is_not_dead() and contrincant.is_not_dead():

        print_health(pokemon, contrincant)
        if IA.ia_turn(contrincant, pokemon) == -1:
            delay_print(f"\nYou paid ${money}.\n")
            break

        print_health(pokemon, contrincant)

        if user_turn(pokemon, contrincant) == -1:
            delay_print(f"\nOpponent paid you ${money}.\n")







def attack_turns(pokemon, contrincant):
    money = np.random.choice(5000)
    while pokemon.is_not_dead() and contrincant.is_not_dead():

        print_health(pokemon, contrincant)
        if user_turn(pokemon, contrincant) == -1:
            delay_print(f"\nOpponent paid you ${money}.\n")
            break

        print_health(pokemon, contrincant)

        if IA.ia_turn(contrincant, pokemon) == -1:
            delay_print(f"\nYou paid ${money}.\n")

