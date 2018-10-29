import  sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.buff_id import BuffId
from sc2.ids.effect_id import EffectId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.ability_id import AbilityId

import numpy as np
import random

np.set_printoptions(threshold=np.nan)


class bot(sc2.BotAI):

    def __init__(self):
        print("Start")

    async def on_step(self, iteration: int):
        await self.print_unit()
        await  self.draw_points()
        await self._client.send_debug()  # this is important, otherwise nothing will be drawn

    async def print_unit(self):
        self.combinedActions = []
        map_size = self.game_info.map_size
        game_map = np.zeros((map_size[0], map_size[1]))

        for marine in self.units(UnitTypeId.MARINE):
            #units = self.known_enemy_units[0]
            game_map[int(marine.position[0])][int(marine.position[1])] = 1
            for i in self.known_enemy_units: # 적 유닛을 찾는다.
                if i.name == "Baneling":# 특정 유닛일 경우
                    self.combinedActions.append(marine.attack(i))
            if self.already_pending_upgrade(UpgradeId.STIMPACK) == 1 and not marine.has_buff(BuffId.STIMPACK) and marine.health > 10:
                self.combinedActions.append(marine(AbilityId.EFFECT_STIM))

        for enemy in self.known_enemy_units:
            game_map[int(enemy.position[0])][int(enemy.position[1])] = 2

        #print(game_map)
        await self.do_actions(self.combinedActions)

    async def draw_points(self):
        all_points = [
            Point2((x, y))
            for x in range(self._game_info.pathing_grid.width)
            for y in range(self._game_info.pathing_grid.height)
            if self._game_info.pathing_grid[(x, y)] == 0
        ]
        for point in all_points:
            height = self.get_terrain_height(point)
            # create the bottom left and top right corner of the rectangle we want to draw
            # use height + 0.01 to draw over the map, not at the same height or it wont show
            location3d1 = Point3((point.x - 0.25, point.y - 0.25, self.terrain_to_z_height(height) + 0.01))
            location3d2 = Point3((point.x + 0.25, point.y + 0.25, self.terrain_to_z_height(height) + 0.01))
            r = 100  # red
            g = 50  # green
            b = 50  # blue
            self._client.debug_box_out(location3d1, location3d2, Point3((r, g, b)))

    def terrain_to_z_height(self, h):
        # this is a custom function i wrote to get the right z heights :D
        # it is really weird, maybe you can fix it in another way
        # the height of the terrain and the z coordinate of a point are two
        # different things, thats why this is needed
        if h > 143:
            return h - 131
        elif h == 143:
            return 12
        elif 140 < h < 143:
            return h - 131
        elif h == 140:
            return 10
        elif 138 < h < 140:
            return h - 130
        elif h == 138:
            return 8
        elif 135 < h < 138:
            return h - 129.5
        elif h == 135:
            return 6
        elif 133 < h < 135:
            return h - 129
        elif h == 133:
            return 4
        elif 130 < h < 133:
            return h - 128.5
        elif h == 130:
            return 2
        elif h < 130:
            return h - 128
        else:
            print("didnt know what to do with height {h}")
            return 15

def main():
    sc2.run_game(sc2.maps.get("DefeatZerglingsAndBanelings"),[
        Bot(Race.Terran, bot()),
        Computer(Race.Zerg, Difficulty.VeryHard)
    ], realtime=True)


if __name__ == "__main__":
    main()