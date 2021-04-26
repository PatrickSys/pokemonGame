from FightEngine import fight
from pokemon.Pokemon import Pokemon



if __name__ == '__main__':

    # Create Pokemon
    Charizard = Pokemon('Chard', 'Fire', ['Flamethrower', 'Fly', 'Blast Burn', 'Fire Punch'],
                         12,  8)
    Blastoise = Pokemon('Blastoise', 'Water', ['Water Gun', 'Bubblebeam', 'Hydro Pump', 'Surf'],
                        10, 10)

    fight(Charizard, Blastoise)