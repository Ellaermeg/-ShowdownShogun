from poke_env import AccountConfiguration, Player, ShowdownServerConfiguration, RandomPlayer
from poke_env.data import GenData
import asyncio
import websocket
import sys


''' Account config '''

sys.path.append("../src")

'''# No authentication required
my_account_config = AccountConfiguration("my_username", None)
player = Player(account_configuration=my_account_config)

# Authentication required
my_account_config = AccountConfiguration("my_username", "super-secret-password")
player = Player(account_configuration=my_account_config, server_configuration=...)'''

# Auto-generated configuration for local use
player = Player()

# Testing out RandomPLayer build

randomplayer = RandomPlayer()
secondplayer = RandomPlayer()

# Method for battling with 'battle_against' is asyncrounous
# Therefore need 'await' option

async def main():
    await randomplayer.battle_against(secondplayer, n_battles=1)

asyncio.run(main())