import asyncio
import aiohttp
import sc2
import numpy as np

from sc2.map_info import MapInfo
from sc2.pixel_map import PixelMap
from sc2 import position
from sc2.data import race_gas, race_worker, race_townhalls, ActionResult, Attribute, Race
from sc2 import Race, Difficulty
from sc2.constants import (COMMANDCENTER)
from sc2.ids.unit_typeid import *
from sc2.ids.ability_id import *
from sc2.position import Point2, Point3

from sc2.player import Bot, Computer, Human


# from zerg.zerg_rush import ZergRushBot
# from protoss.cannon_rush import CannonRushBot

class Nova(sc2.BotAI):
    def __init__(self):
        print('-' * 50)
        print("Exe: Start Nova Bot!")
        print('-' * 50)
        self.start = 0

        self._map_info = MapInfo(self
                                 )


    async def on_step(self, iteration):
        #print(self.game_info.map_ramps)

        if self.start == 0:
            await self._map_info.map_array(self)
            self.start = 1


def main():
    print("Exe: Start Game.")
    # sc2.run_game(sc2.maps.get("(2)RedshiftLE"), [
    #     Bot(Race.Zerg, CreepyBot()),
    #     Bot(Race.Protoss, CannonRushBot())
    # ], realtime=False)

    # sc2.run_game(sc2.maps.get("(2)16-BitLE"), [
    #     Bot(Race.Zerg, CreepyBot()),
    #     Bot(Race.Protoss, CannonRushBot())
    # ], realtime=False)

    # sc2.run_game(sc2.maps.get("(2)RedshiftLE"), [
    #     Bot(Race.Zerg, CreepyBot()),
    #     Bot(Race.Protoss, ThreebaseVoidrayBot())
    # ], realtime=False)

    # sc2.run_game(sc2.maps.get("(2)16-BitLE"), [
    #     Bot(Race.Zerg, CreepyBot()),
    #     Bot(Race.Zerg, ZergRushBot())
    # ], realtime=False)

    # sc2.run_game(sc2.maps.get("(2)RedshiftLE"), [
    #     Bot(Race.Zerg, CreepyBot()),
    #     Bot(Race.Zerg, ZergRushBot())
    # ], realtime=False)

    # sc2.run_game(sc2.maps.get("(2)RedshiftLE"), [
    #     Bot(Race.Zerg, CreepyBot()),
    #     Computer(Race.Zerg, Difficulty.Easy)
    # ], realtime=False)

    # sc2.run_game(sc2.maps.get("(2)RedshiftLE"), [
    #     Bot(Race.Zerg, CreepyBot()),
    #     Computer(Race.Random, Difficulty.VeryHard)
    # ], realtime=False)

    # sc2.run_game(sc2.maps.get("(4)DarknessSanctuaryLE"), [
    #     Bot(Race.Zerg, CreepyBot()),
    #     Computer(Race.Random, Difficulty.CheatMoney)
    # ], realtime=False)

    sc2.run_game(sc2.maps.get("CatalystLE"), [
        Bot(Race.Terran, Nova()),
        Computer(Race.Protoss, Difficulty.CheatInsane)
    ], realtime=False)

    # sc2.run_game(sc2.maps.get("(2)RedshiftLE"), [
    #     Human(Race.Protoss),
    #     Bot(Race.Zerg, CreepyBot())
    # ], realtime=True)


if __name__ == '__main__':
    main()
