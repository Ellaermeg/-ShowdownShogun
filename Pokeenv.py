from poke_env import AccountConfiguration, Player, ShowdownServerConfiguration, RandomPlayer, cross_evaluate
from poke_env.data import GenData
import asyncio
from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.player.battle_order import BattleOrder
import websocket
import sys
import numpy as np
from tabulate import tabulate


''' Testing different methods '''

sys.path.append("../src")

# Team preview with type based heuristics:
def teampreview_preformance(pokemon_a, pokemon_b):
    # Evaluate starting pokemon based on its type advantage against others
    a_on_b = b_on_a = -np.inf
    for type_ in pokemon_a.types:
        if type_:
            a_on_b = max(
                a_on_b,
                type_.damage_multiplier(
                    *pokemon_b.types, type_chart=GenData.from_gen(9).type_chart
            ),
        )

    for type_ in pokemon_b.types:
        if type_:
            b_on_a = max(
                b_on_a,
                type_.damage_multiplier(
                    *pokemon_a.types, type_chart=GenData.from_gen(8).type_chart
                ),
            )
    # Preformance metric based on difference between the two types
    return a_on_b - b_on_a


#Max damage player creation
class OofbigDMG(Player):
    def choose_move(self, battle):
        if battle.available_moves:
            # Goes through moves to find one with highest base power
            GGez = max(battle.available_moves, key=lambda move: move.base_power)

            if battle.can_tera:
                return self.create_order(GGez, terastallize=True) # self.create_order takes in either moves or a pokemon as input. Move objects can have additional parameters (dynamax, terrastal, etc)
            
            # Creates order of highest power moves
            return self.create_order(GGez) # Formats the choice of highest power move
        else:
            # If no attacking move, switch out
            return self.choose_random_move(battle) # Chooses either a valid move or swithces out of battle, and always guaranets a valid return order


# Max damage with team preview:
class OofbigDMGWithTeampreview(OofbigDMG):
    def teampreview(self, battle):
        mon_performance = {}

        # For each of our pokemons
        for i, mon in enumerate(battle.team.values()):
            # We store their average performance against the opponent team
            mon_performance[i] = np.mean(
                [
                    teampreview_preformance(mon, opp)
                    for opp in battle.opponent_team.values()
                ]
            )

        # We sort our mons by performance
        ordered_mons = sorted(mon_performance, key=lambda k: -mon_performance[k])

        # We start with the one we consider best overall
        # We use i + 1 as python indexes start from 0
        #  but showdown's indexes start from 1
        return "/team " + "".join([str(i + 1) for i in ordered_mons])


# PLayer creation
randomplayer = RandomPlayer(max_concurrent_battles=0)
player1 = OofbigDMG(max_concurrent_battles=0)
max_damage_player = OofbigDMGWithTeampreview(max_concurrent_battles=0)
players = [randomplayer,player1,max_damage_player]

# Implementing teams

team_1 = """
Probopass @ Rocky Helmet  
Ability: Magnet Pull  
Tera Type: Fighting  
EVs: 252 HP / 252 Def / 4 SpD  
Bold Nature  
IVs: 0 Atk  
- Body Press  
- Flash Cannon  
- Stealth Rock  
- Thunder Wave  

Iron Crown @ Weakness Policy  
Ability: Quark Drive  
Tera Type: Water  
EVs: 80 HP / 252 SpA / 176 Spe  
Timid Nature  
IVs: 20 Atk  
- Calm Mind  
- Agility  
- Stored Power  
- Tachyon Cutter  

Sinistcha @ Heavy-Duty Boots  
Ability: Heatproof  
Tera Type: Fairy  
EVs: 252 HP / 160 Def / 96 Spe  
Bold Nature  
IVs: 0 Atk  
- Calm Mind  
- Matcha Gotcha  
- Shadow Ball  
- Strength Sap  

Grimmsnarl (M) @ Light Clay  
Ability: Prankster  
Tera Type: Steel  
EVs: 252 HP / 4 Atk / 252 Def  
Impish Nature  
- Light Screen  
- Reflect  
- Parting Shot  
- Spirit Break  

Kyurem @ Never-Melt Ice  
Ability: Pressure  
Tera Type: Ice  
EVs: 180 Atk / 76 SpA / 252 Spe  
Naughty Nature  
- Dragon Dance  
- Icicle Spear  
- Freeze-Dry  
- Earth Power  

Great Tusk @ Assault Vest  
Ability: Protosynthesis  
Tera Type: Steel  
EVs: 168 Atk / 244 SpD / 96 Spe  
Adamant Nature  
- Headlong Rush  
- Ice Spinner  
- Knock Off  
- Rapid Spin  
"""
team_2 = """
Nothin' Under (Hatterene) @ Assault Vest  
Ability: Magic Bounce  
Tera Type: Water  
EVs: 252 HP / 164 SpA / 68 SpD / 24 Spe  
Modest Nature  
IVs: 0 Atk  
- Psyshock  
- Draining Kiss  
- Mystical Fire  
- Future Sight  

Quarter to Three (Darkrai) @ Expert Belt  
Ability: Bad Dreams  
Tera Type: Poison  
EVs: 4 Def / 252 SpA / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Dark Pulse  
- Sludge Bomb  
- Ice Beam  
- Focus Blast  

This Life (Gliscor) (F) @ Toxic Orb  
Ability: Poison Heal  
Tera Type: Normal  
EVs: 244 HP / 128 Atk / 56 SpD / 80 Spe  
Jolly Nature  
- Earthquake  
- Facade  
- Swords Dance  
- Protect  

Light the Candles (Heatran) @ Eject Pack  
Ability: Flame Body  
Tera Type: Fairy  
EVs: 248 HP / 144 SpA / 116 Spe  
Modest Nature  
IVs: 0 Atk  
- Overheat  
- Earth Power  
- Tera Blast  
- Stealth Rock  

Flowers in a Vase (Ogerpon-Wellspring) (F) @ Wellspring Mask  
Ability: Water Absorb  
Tera Type: Water  
EVs: 252 Atk / 4 SpD / 252 Spe  
Adamant Nature  
- Ivy Cudgel  
- Power Whip  
- Play Rough  
- Trailblaze  

Back at it Again (Zamazenta) @ Chesto Berry  
Ability: Dauntless Shield  
Tera Type: Steel  
EVs: 112 HP / 216 Def / 180 Spe  
Jolly Nature  
- Body Press  
- Crunch  
- Iron Defense  
- Rest    
"""

p1 = OofbigDMG(battle_format="gen9ou", team=team_1, avatar="saturn", max_concurrent_battles=0)
p2 = OofbigDMG(battle_format="gen9ou", team=team_2, avatar="mars", max_concurrent_battles=0)

p3 = OofbigDMGWithTeampreview(battle_format="gen9ou", team=team_1, avatar="cyrus", max_concurrent_battles=0)
p4 = OofbigDMGWithTeampreview(battle_format="gen9ou", team=team_2, avatar="jupiter", max_concurrent_battles=0)

# testing battles with custom teams
async def team_battle_test():
    await p3.battle_against(p4, n_battles=3)
    print(f"player 3 won {p3.n_won_battles} / 3 battles")

asyncio.run(team_battle_test())


# Testing single battles

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

asyncio.run(Cross_eval())
