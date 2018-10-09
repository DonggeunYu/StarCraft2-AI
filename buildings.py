import sc2
import numpy as np

from keras.models import load_model
from sc2 import position
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


class build(sc2.BotAI):
    def distance(self, a, b):
        return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

    async def build_supplydepot(self):
        commandcenters = self.units(COMMANDCENTER).ready
        if commandcenters.exists:
            if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
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

                input = [self.units(COMMANDCENTER).first.position[0],
                         self.units(COMMANDCENTER).first.position[1],
                         min_cnt_first[0],
                         min_cnt_first[1],
                         min_cnt_second[0],
                         min_cnt_second[1],
                         min_cnt_third[0],
                         min_cnt_third[1],
                         gas_cnt_first[0],
                         gas_cnt_first[1],
                         gas_cnt_second[0],
                         gas_cnt_second[1]]
                input = np.reshape(input, (1, 12))
                print(input)
                model = load_model('./Model/build_supplydepot_location/model.h5')
                output = model.predict_classes(input)
                print(np.array(output))
                await self.build(SUPPLYDEPOT, near=position.Point2(position.Pointlike()))