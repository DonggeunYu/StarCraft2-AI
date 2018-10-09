import sc2
from sc2.constants import (
    BARRACKS,
    BUNKER,
    COMMANDCENTER,
    ENGINEERINGBAY,
    FACTORY,
    FUSIONCORE,
    GHOSTACADEMY,
    MISSILETURRET,
    ORBITALCOMMAND,
    PLANETARYFORTRESS,
    REACTOR,
    REFINERY,
    SENSORTOWER,
    SUPPLYDEPOT,
    TECHLAB)

from buildings import build
class Nova(build):
    def __init__(self):
        print("hello")
        self.commandcenters = None
        self.supplydepots = None
    
    async def on_step(self, iteration):
        self.time = (self.state.game_loop/22.4) / 60

        self.commandcenters = self.units(COMMANDCENTER)
        self.supplydepots = self.units(SUPPLYDEPOT)
        await self.build_supplydepot()