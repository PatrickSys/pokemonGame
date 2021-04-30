import sys
import time
import numpy as np


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
    print(bcolors.HEADER + "------------------------------------------POKEMON FIGHT!------------------------------------------\n" + bcolors.ENDC)
    print_versus(pokemon, contrincant)
    print_types(pokemon, contrincant)
    print_stat(f"HP/{ident(1)}", pokemon.hp, f"{ident(4)}{contrincant.hp}")
    print_stat("ATTACK/", pokemon.attack, f"{ident(4)}{contrincant.attack}")
    print_stat("DEFENSE/", pokemon.defense, f"{ident(4)}{contrincant.defense}")
    print_stat("SPEED/\t", pokemon.speed, f"{ident(4)}{contrincant.speed}")
    time.sleep(.2)



def print_versus(pokemon, contrincant):
    print(bcolors.WARNING + f"{ident(6)} {pokemon.name} {ident(4)}" + bcolors.ENDC + bcolors.FAIL + "VS" + bcolors.WARNING +
          f"{ident(3)} {contrincant.name}" + bcolors.ENDC)

def print_types(pokemon, contrincant):
    print(f"{bcolors.OKCYAN} TYPE/ {bcolors.ENDC} {ident(4)}", ', '.join(pokemon.types), ident(6),', '.join(contrincant.types))

def print_stat(stat_name, pokemon_stat, contrincant_stat):
    print(f"{bcolors.OKCYAN} {stat_name} {bcolors.ENDC} {ident(4)}", pokemon_stat, ident(4),' ', contrincant_stat)


# Delay printing
def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)


def print_health(pokemon, contrincant):
    print(f"\n{pokemon.get_name()}", f"HEALTH\t{bcolors.OKGREEN}{pokemon.get_health()}{bcolors.ENDC}".rjust(45-len(pokemon.get_name()), ' '))
    print(f"{contrincant.get_name()}", f"HEALTH\t{bcolors.OKGREEN}{contrincant.get_health()}{bcolors.ENDC}".rjust(45-len(contrincant.get_name()), ' '),'\n')


def print_moves(pokemon):
    print(f"Go {pokemon.get_name()}!")
    print(f'\n[{pokemon.moves[0].get_name()}][{pokemon.moves[0].get_pp()} PP]\t[{pokemon.moves[1].get_name()}][{pokemon.moves[1].get_pp()} PP]')
    print(f'[{pokemon.moves[2].get_name()}][{pokemon.moves[2].get_pp()} PP]\t[{pokemon.moves[3].get_name()}][{pokemon.moves[3].get_pp()} PP]\n')


def ask_move(pokemon):
    print_moves(pokemon)
    return int(input('Pick a move: '))

# Allow two pokemon to fight each other

def turn(pokemon, contrincant):

    index = ask_move(pokemon)
    delay_print(f"\n{pokemon.name} used {pokemon.moves[index - 1].get_name()}!")
    time.sleep(.1)

    # Determine damage
    pokemon.do_attack(pokemon.moves[index - 1], contrincant)
    time.sleep(.1)

    print_health(pokemon, contrincant)
    time.sleep(.5)


    # Check to see if Pokemon fainted
    if contrincant.get_bars() <= 0:
        delay_print("\n..." + contrincant.get_name() + ' fainted.')
        return -1


def contrincant_is_faster_than_pokemon(pokemon, contrincant):
    return contrincant.get_speed() > pokemon.get_speed()



def fight(pokemon, contrincant):
    print_header(pokemon, contrincant)


    # Take speed in count, if so swap turns TODO is this ok?
    if contrincant_is_faster_than_pokemon(pokemon, contrincant):
        swap = pokemon
        pokemon = contrincant
        contrincant = swap

    # Continue while pokemon still have health

    while (pokemon.get_bars() > 0) and (contrincant.get_bars() > 0):

        if turn(pokemon, contrincant) or turn(contrincant, pokemon) == -1:
            break






    money = np.random.choice(5000)
    delay_print(f"\nOpponent paid you ${money}.\n")
