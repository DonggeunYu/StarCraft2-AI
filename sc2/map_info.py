import sc2
import cv2

import numpy as np
from PIL import Image
from sc2 import position

from sc2.bot_ai import BotAI

np.set_printoptions(threshold=np.nan)

class MapInfo:
    def __init__(self, game):
        self.game = game

    async def map_array(self, game):
        self.game = game
        map_size = self.game.game_info.map_size
        map_rams = self.game.game_info.map_ramps
        map = np.zeros((map_size[0], map_size[1], 3))

        for i in range(0, map_size[0]):
            for j in range(0, map_size[1]):
                temp = self.game.get_terrain_height(position.Point2(position.Pointlike((i, j))))
                print(temp, type(temp))
                map[i][j][0] = 100

        for cnt in range(0, len(map_rams)):
            ramps = list(map_rams[cnt]._points)
            for i, j in ramps:
                map[i][j][2] = 255

        cv2.imshow("Map", map)
        cv2.waitKey(1)w