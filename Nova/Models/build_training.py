import sc2
from sc2 import run_game, maps, Race, Difficulty, Result
from sc2.player import Bot, Computer
from sc2 import position
from sc2.constants import ARMORY, BARRACKS, BUNKER, \
 COMMANDCENTER, ENGINEERINGBAY, FACTORY, FUSIONCORE, \
  GHOSTACADEMY, MISSILETURRET, ORBITALCOMMAND, \
   PLANETARYFORTRESS, REACTOR, REFINERY, SENSORTOWER, \
    SUPPLYDEPOT, TECHLAB
class main(sc2.BotAI):
    def __init__(self):
        print("Start StarCraft II")


    def on_end(self, game_result):
        print('--- on_end called ---')
        print(game_result)


    async def on_step(self, iteration):
        self.time = (self.state.game_loop / 22.4) / 60

        await self.distribute_workers()
        await self.build_supplydepot()


    async def build_supplydepot(self):
        commandcenters = self.units(COMMANDCENTER).ready
        if commandcenters.exists:
            if self.can_afford(SUPPLYDEPOT):
                await self.build(SUPPLYDEPOT, near=commandcenters.first)
# StarCraftII Start
run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, main()),
    Computer(Race.Zerg, Difficulty.Easy)], realtime=False)
