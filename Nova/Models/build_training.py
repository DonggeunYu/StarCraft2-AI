import sc2
from sc2 import run_game, maps, Race, Difficulty, Result
from sc2.player import Bot, Computer
from sc2 import position
from sc2.constants import ARMORY, BARRACKS, BUNKER, \
 COMMANDCENTER, ENGINEERINGBAY, FACTORY, FUSIONCORE, \
  GHOSTACADEMY, MISSILETURRET, ORBITALCOMMAND, \
   PLANETARYFORTRESS, REACTOR, REFINERY, SENSORTOWER, \
    SUPPLYDEPOT, TECHLAB
from sc2.constants import SCV, MARINE
from sc2.constants import RICHMINERALFIELD
import cv2
import random
import numpy as np
import matplotlib.pyplot as plt

class main(sc2.BotAI):
    def __init__(self):
        print("Start StarCraft II")


    def on_end(self, game_result):
        print('--- on_end called ---')
        print(game_result)


    async def on_step(self, iteration):
        self.time = (self.state.game_loop / 22.4) / 60

        await self.distribute_workers()
        await self.build_worker()
        # await self.build_refinery()
        await self.build_supplydepot()
        await self.intel()
        await self.graph()
        #await self.build_marine()


    async def build_worker(self):
        commandcenters = self.units(COMMANDCENTER).ready.noqueue
        if commandcenters.exists and len(self.units(SCV)) < 25:
            if self.can_afford(SCV):
                await self.do(random.choice(commandcenters).train(SCV))


    def map_cv2(self):
        game_data = np.zeros((self.game_info.map_size[1], self.game_info.map_size[0], 3), np.uint8)

        for unit in self.units().ready:
            pos = unit.position
            # rectangle(img, start, end, color, thickness)
            cv2.rectangle(game_data, (int(pos[0]), int(pos[1])), (int(int(pos[0]) + unit.radius), int(int(pos[1]) + unit.radius)), (255, 255, 255), 1)

        for minerals in self.state.mineral_field:
            minerals_pos = minerals.position
            cv2.rectangle(game_data, (int(minerals_pos[0]), int(minerals_pos[1])), (int(int(minerals_pos[0]) + minerals.radius), int(int(minerals_pos[1]) + unit.radius)), (255, 255, 255), 1)

        # flip horizontally to make our final fix in visual representation:
        flipped = cv2.flip(game_data, 0)
        resized = cv2.resize(flipped, dsize=None, fx=2, fy=2)
        return resized

    def random_location_variance(self, location):
        x = location[0]
        y = location[1]

        #  FIXED THIS
        x += random.randrange(-5,5)
        y += random.randrange(-5,5)

        if x < 0:
            print("x below")
            x = 0
        if y < 0:
            print("y below")
            y = 0
        if x > self.game_info.map_size[0]:
            print("x above")
            x = self.game_info.map_size[0]
        if y > self.game_info.map_size[1]:
            print("y above")
            y = self.game_info.map_size[1]

        go_to = position.Point2(position.Pointlike((x,y)))

        return go_to

    async def build_supplydepot(self):
        commandcenters = self.units(COMMANDCENTER).ready
        if commandcenters.exists:
            if self.can_afford(SUPPLYDEPOT):
                #if len(self.units(SUPPLYDEPOT)) < 1 or len(self.units(BARRACKS)) > 0:
                    min_distance = 100
                    min_cnt = 0
                    cnt = -1

                    for minerals in self.state.mineral_field:
                        minerals_commandcenter_distance = minerals.distance_to(self.units(COMMANDCENTER).first.position)
                        cnt += 1
                        if min_distance > minerals_commandcenter_distance:
                            min_distance = minerals_commandcenter_distance
                            min_cnt = cnt
                    await self.build(SUPPLYDEPOT, near=position.Point2(position.Pointlike((0, 0))))
                    print(self.state.mineral_field[min_cnt].position.towards(position.Point2(position.Pointlike((-10, -10)))))


    async def graph(self):
        data = [self.minerals, self.vespene]
        labels = ['Minerals', 'Vespense']
        plt.cla()
        plt.clf()
        plt.bar(labels, data)
        plt.pause(1e-10)

    async def intel(self):
        # for game_info: https://github.com/Dentosal/python-sc2/blob/master/sc2/game_info.py#L162
        # flip around. It's y, x when you're dealing with an array.

        cv2.imshow('Intel', self.map_cv2())
        cv2.waitKey(1)


    async def build_refinery(self):
        for commandcenter in self.units(COMMANDCENTER).ready:
            vaspenes = self.state.vespene_geyser.closer_than(10.0, commandcenter)
            for vaspene in vaspenes:
                if not self.can_afford(REFINERY):
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker is None:
                    break
                if not self.units(REFINERY).closer_than(1.0, vaspene).exists:
                    await self.do(worker.build(REFINERY, vaspene))


    def build_location():
        return (50, 50)

run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, main()),
    Computer(Race.Zerg, Difficulty.Easy)], realtime=False)
