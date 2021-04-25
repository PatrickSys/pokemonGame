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
    time.sleep(2)


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


# Allow two pokemon to fight each other

def fight(pokemon, contrincant):
    print_header(pokemon, contrincant)

    # Consider type advantages
    version = ['Fire', 'Water', 'Grass']
    for i, k in enumerate(version):
        if pokemon.types == k:
            # Both are same type
            if contrincant.types == k:
                string_1_attack = '\nIts not very effective...'
                string_2_attack = '\nIts not very effective...'

            # Pokemon2 is STRONG
            if contrincant.types == version[(i + 1) % 3]:
                contrincant.attack *= 2
                contrincant.defense *= 2
                pokemon.attack /= 2
                pokemon.defense /= 2
                string_1_attack = '\nIts not very effective...'
                string_2_attack = '\nIts super effective!\n'

            # Pokemon2 is WEAK
            if contrincant.types == version[(i + 2) % 3]:
                pokemon.attack *= 2
                pokemon.defense *= 2
                contrincant.attack /= 2
                contrincant.defense /= 2
                string_1_attack = '\nIts super effective!'
                string_2_attack = '\nIts not very effective...'

    # Now for the actual fighting...
    # Continue while pokemon still have health

    while (pokemon.bars > 0) and (contrincant.bars > 0):
        # Print the health of each pokemon
        print_health(pokemon, contrincant)
        print_moves(pokemon)

        index = int(input('Pick a move: '))
        delay_print(f"\n{pokemon.name} used {pokemon.moves[index - 1]}!")
        time.sleep(1)
        delay_print(string_1_attack)

        # Determine damage
        contrincant.bars -= pokemon.attack
        contrincant.health = ""

        # Add back bars plus defense boost
        for j in range(int(contrincant.bars + .1 * contrincant.defense)):
            contrincant.health += "="

        time.sleep(1)
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
        time.sleep(1)
        delay_print(string_2_attack)

        # Determine damage
        pokemon.bars -= contrincant.attack
        pokemon.health = ""

        # Add back bars plus defense boost
        for j in range(int(pokemon.bars + .1 * pokemon.defense)):
            pokemon.health += "="

        time.sleep(1)
        print_health(pokemon, contrincant)
        time.sleep(.5)

        # Check to see if Pokemon fainted
        if pokemon.bars <= 0:
            delay_print("\n..." + pokemon.name + ' fainted.')
            break

    money = np.random.choice(5000)
    delay_print(f"\nOpponent paid you ${money}.\n")
