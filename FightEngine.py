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
    print(f"\n{pokemon.name}", f"HEALTH\t{bcolors.OKGREEN}{pokemon.health}{bcolors.ENDC}".rjust(45-len(pokemon.name), ' '))
    print(f"{contrincant.name}", f"HEALTH\t{bcolors.OKGREEN}{contrincant.health}{bcolors.ENDC}".rjust(45-len(contrincant.name), ' '),'\n')


def print_moves(pokemon):
    print(f"Go {pokemon.name}!")
    print(f'\n[{pokemon.moves[0].getname()}]\t[{pokemon.moves[1].getname()}]')
    print(f'[{pokemon.moves[2].getname()}]\t[{pokemon.moves[3].getname()}]\n')


# TODO Determine damage mechanics
def determine_damage(pokemon, attack):

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
        delay_print(f"\n{pokemon.name} used {pokemon.moves[index - 1].getname()}!")
        time.sleep(.1)

        # Determine damage
        determine_damage(contrincant, pokemon.attack)


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
        delay_print(f"\n{contrincant.name} used {contrincant.moves[index - 1].getname()}!")
        time.sleep(.1)

        # Determine damage
        determine_damage(pokemon, contrincant.attack)


        time.sleep(.1)
        print_health(pokemon, contrincant)
        time.sleep(.5)

        # Check to see if Pokemon fainted
        if pokemon.bars <= 0:
            delay_print("\n..." + pokemon.name + ' fainted.')
            break

    money = np.random.choice(5000)
    delay_print(f"\nOpponent paid you ${money}.\n")
