import sys
import time
import numpy as np
from multipledispatch import dispatch

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
    print(bcolors.HEADER + "---------------------POKEMON FIGHT!---------------------" + bcolors.ENDC)
    print_versus(pokemon, contrincant)
    print_stat("TYPE/", pokemon.types, contrincant.types)
    print_stat("ATTACK/", pokemon.attack, f"\t{contrincant.attack}")
    print_stat("DEFENSE", pokemon.defense, f"\t{contrincant.defense}")
    print_stat("LVL/  ", 3 * (1 + np.mean([pokemon.attack, pokemon.defense])),
               3 * (1 + np.mean([contrincant.attack, contrincant.defense])))
    time.sleep(.2)


@dispatch(str, str, str)
def print_centered(message, arg1, arg2):
    print(f"{message}\t{arg1}\t{arg2}".center(80))


@dispatch(str)
def print_centered(message):
    print(f"{message}".center(90))


def print_versus(pokemon, contrincant):
    print(bcolors.WARNING + f"{ident(4)}{pokemon.name}{ident(2)}" + bcolors.ENDC + bcolors.FAIL + "VS" + bcolors.WARNING +
          f"{ident(2)}{contrincant.name}" + bcolors.ENDC)


def print_stat(stat_name, pokemon_stat, contrincant_stat):
    print(bcolors.OKCYAN + f"{stat_name}"+ bcolors.ENDC + f"{ident(3)}{pokemon_stat}{ident(5)}{contrincant_stat}")


# Delay printing
def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)


def print_health(pokemon, contrincant):
    print(f"\n{pokemon.name}", f"HEALTH\t{bcolors.OKGREEN}{pokemon.health}{bcolors.ENDC}".rjust(45-len(pokemon.name), ' '))
    print(f"{contrincant.name}", f"HEALTH\t{bcolors.OKGREEN}{contrincant.health}{bcolors.ENDC}".rjust(45-len(contrincant.name), ' '),'\n')


def print_moves(pokemon):
    print(f"Go {pokemon.name}!")
    print(f'\n[{pokemon.moves[0]}]\t[{pokemon.moves[1]}]')
    print(f'[{pokemon.moves[2]}]\t[{pokemon.moves[3]}]\n')


def reduce_health(pokemon, attack):

    damage=""

    for i in range (attack):
        damage += '='


    pokemon.bars -= pokemon.attack
    pokemon.health = pokemon.set_health()

# Allow two pokemon to fight each other

def fight(pokemon, contrincant):
    print_header(pokemon, contrincant)

    # TODO Consider type advantages

    # Continue while pokemon still have health

    while (pokemon.bars > 0) and (contrincant.bars > 0):

        # Print the health of each pokemon
        print_health(pokemon, contrincant)
        print_moves(pokemon)

        index = int(input('Pick a move: '))
        delay_print(f"\n{pokemon.name} used {pokemon.moves[index - 1]}!")
        time.sleep(.1)

        # Determine damage
        reduce_health(contrincant, pokemon.attack)


        time.sleep(.1)
        print_health(pokemon, contrincant)
        time.sleep(.5)

        # Check to see if Pokemon fainted
        if contrincant.bars <= 0:
            delay_print("\n..." + contrincant.name + ' fainted.')
            break

        # Pokemon2s turn

        print_moves(contrincant)

        index = int(input('Pick a move: '))
        delay_print(f"\n{contrincant.name} used {contrincant.moves[index - 1]}!")
        time.sleep(.1)

        # Determine damage
        reduce_health(pokemon, contrincant.attack)


        time.sleep(.1)
        print_health(pokemon, contrincant)
        time.sleep(.5)

        # Check to see if Pokemon fainted
        if pokemon.bars <= 0:
            delay_print("\n..." + pokemon.name + ' fainted.')
            break

    money = np.random.choice(5000)
    delay_print(f"\nOpponent paid you ${money}.\n")
