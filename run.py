import random
import sys

import sc2
from sc2 import run_game, maps, Difficulty, Race
from sc2.player import Bot, Computer

from __init__ import run_ladder_game

# Load bot
from nova import Nova

bot = Bot(Race.Terran, Nova())

# Start game
if __name__ == "__main__":
    if "--LadderServer" in sys.argv:
        # Ladder game started by LadderManager
        print("Starting ladder game...")
        run_ladder_game(bot)
    else:
        # Local game
        print("Starting local game...")
        random_map = random.choice(
            [
                "AcidPlantLE",
                #"BlueshiftLE",
                #"CeruleanFallLE",
                "DreamcatcherLE",
                #"FractureLE",
                "LostAndFoundLE",
                #"ParaSiteLE",
            ]
        )

        #sc2.run_game(sc2.maps.get(random_map), [bot, Computer(Race.Protoss, Difficulty.CheatVision)], realtime=False)
        run_game(maps.get("AbyssalReefLE"), [bot, Computer(Race.Zerg, Difficulty.Easy)], realtime=False)
