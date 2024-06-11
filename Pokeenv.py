from poke_env import AccountConfiguration, Player, ShowdownServerConfiguration, RandomPlayer, cross_evaluate
from poke_env.data import GenData
import asyncio
from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.player.battle_order import BattleOrder
import websocket
import sys
from tabulate import tabulate


''' Account config '''

sys.path.append("../src")


# Testing single battles
async def Battle_test():
    await Thatsalotofdmg.battle_against(randomplayer, n_battles = 100)
    print(f"Max damage player won {Thatsalotofdmg.n_won_battles} / 100 battles")

asyncio.run(Battle_test())


# Testing Cross evaluation battles

'''async def Cross_eval():
    cross_evaluation = await cross_evaluate(players, n_challenges=100)
    cross_evaluation

    table = [["-"] + [p.username for p in players]]
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])
    print(tabulate(table))

asyncio.run(Cross_eval())
'''
# Testing Max damage player

class OofbigDMG(Player):
    def choose_move(self, battle):
        if battle.available_moves:
            # Goes through moves to find one with highest base power
            GGez = max(battle.available_moves, key=lambda move: move.base_power)

            if battle.can_dynamax:
                return self.create_order(GGez, dynamax=True) # self.create_order takes in either moves or a pokemon as input. Move objects can have additional parameters (dynamax, terrastal, etc)
            
            # Creates order of highest power moves
            return self.create_order(GGez) # Formats the choice of highest power move
        else:
            # If no attacking move, switch out
            return self.choose_random_move(battle) # Chooses either a valid move or swithces out of battle, and always guaranets a valid return order

# PLayer creation
randomplayer = RandomPlayer()
Thatsalotofdmg = OofbigDMG()

players = [randomplayer, Thatsalotofdmg]

# Method for battling with 'battle_against' is asyncrounous
# Therefore need 'await' option
