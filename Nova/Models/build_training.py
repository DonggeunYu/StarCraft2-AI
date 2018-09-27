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
import cv2
import random
import numpy as np
from PIL import Image
import csv

class main(sc2.BotAI):
    def __init__(self):
        print("Start StarCraft II")
        self.supply_cnt = 0
        self.supply_position = []


    def on_end(self, game_result):
        print('--- on_end called ---')
        print(game_result)


    async def on_step(self, iteration):
        self.time = (self.state.game_loop / 22.4) / 60

        await self.distribute_workers()
        await self.build_worker()
        await self.build_supplydepot()


    async def build_worker(self):
        commandcenters = self.units(COMMANDCENTER).ready.noqueue
        if commandcenters.exists and len(self.units(SCV)) < 25:
            if self.can_afford(SCV):
                await self.do(random.choice(commandcenters).train(SCV))


    def distance(self, a, b):
        return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5


    async def build_supplydepot(self):
        commandcenters = self.units(COMMANDCENTER).ready
        if commandcenters.exists:
            if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                    game_data = np.zeros((self.game_info.map_size[1], self.game_info.map_size[0], 3), np.uint8)

                    minerals_commandcenter_distance = []
                    min_cnt = {}
                    for minerals in self.state.mineral_field:
                        minerals_commandcenter_distance.append(
                            self.distance(minerals.position, self.units(COMMANDCENTER).first.position))

                        min_cnt.update({str(minerals_commandcenter_distance[-1]): (
                        int(minerals.position[0]), int(minerals.position[1]))})

                    minerals_commandcenter_distance.sort()
                    min_cnt_first = min_cnt[str(minerals_commandcenter_distance[0])]
                    min_cnt_second = min_cnt[str(minerals_commandcenter_distance[1])]
                    min_cnt_third = min_cnt[str(minerals_commandcenter_distance[2])]

                    gas_cnt_first = ()
                    gas_data_first = 1000
                    gas_cnt_second = ()

                    for vespen in self.state.vespene_geyser:
                        vespen_commandcenter_distance = self.distance(vespen.position,
                                                                      self.units(COMMANDCENTER).first.position)

                        if gas_data_first >= vespen_commandcenter_distance:
                            gas_cnt_second = gas_cnt_first
                            gas_cnt_first = (int(vespen.position[0]), int(vespen.position[1]))
                            gas_data_first = vespen_commandcenter_distance

                    a = [min_cnt_first, min_cnt_second, min_cnt_third, gas_cnt_first, gas_cnt_second]
                    random_ = random.choices(a)

                    await self.build(SUPPLYDEPOT, near=position.Point2(position.Pointlike(random_[0])).towards(self.game_info.map_center, -3))


                    if self.units(SUPPLYDEPOT) and len(self.units(SUPPLYDEPOT)) > self.supply_cnt:
                        self.supply_cnt += 1
                        print(self.supply_cnt)
                        if self.supply_cnt >= 5:
                            print('Game End')
                            await self._client.leave()

                        supply_temp = []
                        for i in self.units(SUPPLYDEPOT):
                            supply_temp.append(i.position)

                        supply_temp_append = (list(set(supply_temp) - set(self.supply_position)))[0]

                        cv2.rectangle(game_data, (min_cnt_first[0], min_cnt_first[1]),
                                      (min_cnt_first[0] + 1, min_cnt_first[1] + 1),
                                      (255, 255, 255), 1)
                        cv2.rectangle(game_data, (min_cnt_second[0], min_cnt_second[1]),
                                      (min_cnt_second[0] + 1, min_cnt_second[1] + 1),
                                      (255, 255, 255), 1)
                        cv2.rectangle(game_data, (min_cnt_third[0], min_cnt_third[1]),
                                      (min_cnt_third[0] + 1, min_cnt_third[1] + 1),
                                      (255, 255, 255), 1)
                        cv2.rectangle(game_data, (gas_cnt_first[0], gas_cnt_first[1]),
                                      (gas_cnt_first[0] + 1, gas_cnt_first[1] + 1),
                                      (255, 255, 0), 1)
                        cv2.rectangle(game_data, (gas_cnt_second[0], gas_cnt_second[1]),
                                      (gas_cnt_second[0] + 1, gas_cnt_second[1] + 1),
                                      (255, 255, 0), 1)



                        self.supply_position = supply_temp
                        fields = [self.units(COMMANDCENTER).first.position,
                                min_cnt_first,
                                min_cnt_second,
                                min_cnt_third,
                                gas_cnt_first,
                                gas_cnt_second,
                                supply_temp_append]

                        with open(r'SUPPLYDEPOT.csv', 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow(fields)


                     # flip horizontally to make our final fix in visual representation:
                    flipped = cv2.flip(game_data, 0)
                    resized = cv2.resize(flipped, dsize=None, fx=2, fy=2)

                    cv2.imshow('Intel', resized)
                    cv2.waitKey(1)


abc = 0
while(abc < 100):
    print('-----------------------------------', abc, '-----------------------------------')
    run_game(maps.get("AbyssalReefLE"), [
        Bot(Race.Terran, main()),
        Computer(Race.Zerg, Difficulty.Easy)], realtime=True)
    abc += 1
