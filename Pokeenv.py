from poke_env import AccountConfiguration, Player, ShowdownServerConfiguration, RandomPlayer, cross_evaluate
from poke_env.data import GenData
import asyncio
import websocket
import sys
from tabulate import tabulate


''' Account config '''

sys.path.append("../src")

# Testing out RandomPLayer build

randomplayer = RandomPlayer()
secondplayer = RandomPlayer()
thirdplayer = RandomPlayer()

players = [randomplayer, secondplayer,thirdplayer]

# Method for battling with 'battle_against' is asyncrounous
# Therefore need 'await' option


'''async def main():
    await randomplayer.battle_against(secondplayer, n_battles=6)
asyncio.run(main())'''

async def Cross_eval():
    cross_evaluation = await cross_evaluate(players, n_challenges=6)
    cross_evaluation

    table = [["-"] + [p.username for p in players]]
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])
    print(tabulate(table))

asyncio.run(Cross_eval())


