import cv2
import sc2
import numpy as np
from sc2 import position
from sc2.bot_ai import BotAI

class MapInfo():
    def __init__(self):
        self.map_array = self._map_array()

    def _map_array(self):
        map = np.zeros((self._game_info.map_size[0], self._game_info.map_size[1], 3))
        for i in range(0, self._game_info.map_size[0]):
            for j in range(0, self._game_info.map_size[1]):
                map[i][j][0] = BotAI.get_terrain_height(position.Point2(position.Pointlike((i, j))))

        return map