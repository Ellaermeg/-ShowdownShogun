from poke_env import AccountConfiguration, Player, ShowdownServerConfiguration, RandomPlayer, cross_evaluate
from poke_env.data import GenData
import asyncio
from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.player.battle_order import BattleOrder
import websocket
import sys
from tabulate import tabulate


''' Testing different methods '''

sys.path.append("../src")

#Max damage player creation

class OofbigDMG(Player):
    def choose_move(self, battle):
        if battle.available_moves:
            # Goes through moves to find one with highest base power
            GGez = max(battle.available_moves, key=lambda move: move.base_power)

            if battle.can_terastallize:
                return self.create_order(GGez, terastallize=True) # self.create_order takes in either moves or a pokemon as input. Move objects can have additional parameters (dynamax, terrastal, etc)
            
            # Creates order of highest power moves
            return self.create_order(GGez) # Formats the choice of highest power move
        else:
            # If no attacking move, switch out
            return self.choose_random_move(battle) # Chooses either a valid move or swithces out of battle, and always guaranets a valid return order

# PLayer creation
randomplayer = RandomPlayer()
max_damage_player = OofbigDMG()
players = [randomplayer, max_damage_player]


# Implementing teams

team_1 = """
Baxcalibur @ Heavy-Duty Boots  
Ability: Thermal Exchange  
Tera Type: Dragon  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Icicle Crash  
- Glaive Rush  
- Earthquake  
- Dragon Dance  

Gholdengo @ Choice Specs  
Ability: Good as Gold  
Tera Type: Flying  
EVs: 108 HP / 252 SpA / 148 Spe  
Modest Nature  
IVs: 0 Atk  
- Shadow Ball  
- Make It Rain  
- Power Gem  
- Thunderbolt  

Great Tusk @ Booster Energy  
Ability: Protosynthesis  
Tera Type: Ghost / Water  
EVs: 240 HP / 16 Def / 252 Spe  
Jolly Nature  
- Earthquake  
- Close Combat / Knock Off  
- Rapid Spin  
- Stealth Rock  

Iron Valiant @ Choice Scarf  
Ability: Quark Drive  
Tera Type: Fairy  
EVs: 4 Atk / 252 SpA / 252 Spe  
Naive Nature  
- Moonblast  
- Close Combat  
- Knock Off  
- Trick  

Rotom-Wash @ Leftovers  
Ability: Levitate  
Tera Type: Steel  
EVs: 248 HP / 52 Def / 196 SpD / 12 Spe  
Calm Nature  
IVs: 0 Atk  
- Thunder Wave  
- Hydro Pump  
- Volt Switch  
- Protect  

Kingambit @ Leftovers  
Ability: Supreme Overlord  
Tera Type: Fairy  
EVs: 252 Atk / 4 Def / 252 Spe  
Adamant Nature  
- Kowtow Cleave  
- Tera Blast  
- Sucker Punch  
- Swords Dance  
"""
team_2 = """
Baxcalibur @ Heavy-Duty Boots  
Ability: Thermal Exchange  
Tera Type: Dragon  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Icicle Crash  
- Glaive Rush  
- Earthquake  
- Dragon Dance  

Gholdengo @ Choice Specs  
Ability: Good as Gold  
Tera Type: Flying  
EVs: 108 HP / 252 SpA / 148 Spe  
Modest Nature  
IVs: 0 Atk  
- Shadow Ball  
- Make It Rain  
- Power Gem  
- Thunderbolt  

Great Tusk @ Booster Energy  
Ability: Protosynthesis  
Tera Type: Ghost / Water  
EVs: 240 HP / 16 Def / 252 Spe  
Jolly Nature  
- Earthquake  
- Close Combat / Knock Off  
- Rapid Spin  
- Stealth Rock  

Iron Valiant @ Choice Scarf  
Ability: Quark Drive  
Tera Type: Fairy  
EVs: 4 Atk / 252 SpA / 252 Spe  
Naive Nature  
- Moonblast  
- Close Combat  
- Knock Off  
- Trick  

Rotom-Wash @ Leftovers  
Ability: Levitate  
Tera Type: Steel  
EVs: 248 HP / 52 Def / 196 SpD / 12 Spe  
Calm Nature  
IVs: 0 Atk  
- Thunder Wave  
- Hydro Pump  
- Volt Switch  
- Protect  

Kingambit @ Leftovers  
Ability: Supreme Overlord  
Tera Type: Fairy  
EVs: 252 Atk / 4 Def / 252 Spe  
Adamant Nature  
- Kowtow Cleave  
- Tera Blast  
- Sucker Punch  
- Swords Dance  
"""

p1 = OofbigDMG(battle_format="gen9ou", team=team_1)
p2 = OofbigDMG(battle_format="gen9ou", team=team_2)


# testing battles with custom teams
async def team_battle_test():
    await p1.battle_against(p2, n_battles=3)
    print(f"player 1 won {p1.n_won_battles} / 3 battles")

asyncio.run(team_battle_test())



'''# Testing single battles

async def Battle_test():
    await max_damage_player.battle_against(randomplayer, n_battles = 100)
    print(f"Max damage player won {max_damage_player.n_won_battles} / 100 battles")

asyncio.run(Battle_test())


# Testing Cross evaluation battles

async def Cross_eval():
    cross_evaluation = await cross_evaluate(players, n_challenges=100)
    cross_evaluation

    table = [["-"] + [p.username for p in players]]
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])
    print(tabulate(table))

asyncio.run(Cross_eval())'''
