import sc2
from sc2 import run_game, maps, Race, Difficulty, Result
from sc2.player import Bot, Computer
from sc2 import position
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
 CYBERNETICSCORE, STARGATE, VOIDRAY, SCV, DRONE, ROBOTICSFACILITY, OBSERVER, \
 ZEALOT, STALKER

class main(sc2.BotAI):
    def __init__(self):
        print("Start StarCraft II")


    def on_end(self, game_result):
        print('--- on_end called ---')
        print(game_result)


    async def on_step(self, iteration):
        self.time = (self.state.game_loop / 22.4) / 60

        await self.distribute_workers()
        await self.build_pylon()
        for probe in self.units(PROBE):
            pos = probe.position
            print(pos)


    async def build_pylon():
        nexsues = self.units(NEXUS).ready
        if nexuses.exists:
            if self.can_afford(PYLON):
                await self.build_pylon()
# StarCraftII Start
run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, main()),
    Computer(Race.Protoss, Difficulty.Easy)], realtime=True)
