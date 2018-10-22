"""
version: 2.1.1
Date: 30.9.2018
made by Jan Dickmann (jan.dickmann@web.de)
this is the result of me trying to make a somewhat decent simple bot,
its not that great yet and has some obvious flaws, but this is what I have for now
thanks to Dentosal for the python-sc2 library that I used to make this bot
https://github.com/Dentosal/python-sc2

also I didn't try to make this pretty or easy to read or easy to understand, if you have a question you can send me an email

documentation is mostly still missing...
2.1.1 fixed a bug that would cause the bot to not act correctly when defending against workerrush if the enemy workers kite far enough away from the mainbase
2.1.0 fixed a bug in the cannonrush defense logic, fixed a bug that a second workerscuot would not get defendet,
        fixed a bug that would cause the bot to crash if it spots an enemy building but no enemy unit and there are no powered cannons spotted (yes a bit weird I know)
        added code that will send a new scv to continue building somethign if the original building scv was killed
2.0.1 just improved the cannonrush defense a little bit so that I hopefully win against "Threewaylover" on the ladder consistently,
        I wanted to improve it anyways since it was not that hard and will be much more effective now (if there are no new crashes xD)
2.0: Rework of the bot, kind of a hotfix, I want to make it as stayable as possible for now, I lose to many games because of crashes
    this is why this version will not do a combat shield push (i get back to that later) but instead just 5 rax marine production
    also the micro will be moved to a external method, not in on_step to make the code easier to read
1.2.2: bugfix
changes(1.2.1): added workerspread to "startsegment"
changes(1.2.0): added self._client.game_step = 1 in "startsegment"
changes: small bugfixes and start second collected attack if first attack fails
changes: replaced all self.do with self.combinedactions.append and execute them at the end of on_step for better performance
(except 2 where "if await self.do(... or self.build" and the 2 self.build but its not so bad because those are not being called often


I didnt test this change a lot yet, so it might still cause bugs, but the performance increase is ridiculous,
a game that took at least 20-30 minutes before (maybe longer) takes less than 1,5 mintues now, it is crazy
"""

import asyncio
import time
import sc2
import random
from sc2.ids.unit_typeid import UnitTypeId
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import *
from sc2.position import *
from sc2.ids.ability_id import AbilityId
from sc2.data import race_worker


class Ramu(sc2.BotAI):
    start = True
    defendet = True
    moveout = False
    rush = False
    wrinit = False
    basespotted = True
    pushedback = False
    defendingworker = 0
    scvs = []
    pullback = []
    pulledback = []
    miningworkers = []
    rallypoint = None
    marines = None
    all_enemy_units = None
    enemy_units = None
    close_enemys = None
    nospam = False
    nospam1 = False
    combinedActions = []
    pushbackinit = False
    cc = None
    barcount = 0

    async def on_step(self, iteration):

        self.combinedActions = []

        self.cc = self.units(UnitTypeId.COMMANDCENTER).first
        cc = self.cc

        if self.start:  # Startsegment
            self._client.game_step = 1
            self.start = False
            self.rallypoint = self.main_base_ramp.top_center
            mineral = self.state.mineral_field.filter(lambda x: x.distance_to(cc) < 12)
            wor = []
            for m in mineral:
                w = self.workers.filter(lambda x: not wor.__contains__(x.tag)).closest_to(m)
                self.combinedActions.append(w.gather(m))
                wor.append(w.tag)

        self.marines = self.units(UnitTypeId.MARINE)
        self.all_enemy_units = self.known_enemy_units.exclude_type([UnitTypeId.LARVA, UnitTypeId.EGG])
        self.enemy_units = (self.all_enemy_units - self.known_enemy_structures.exclude_type(
            [UnitTypeId.BUNKER, UnitTypeId.SPINECRAWLER]))
        self.close_enemys = self.all_enemy_units.filter(lambda x: x.distance_to(cc) < 16)

        for b in self.units(UnitTypeId.BARRACKS):
            if not b.is_ready:
                building = False
                for w in self.workers:
                    if w.order_target == b.position or w.order_target == b.tag:
                        building = True
                        break
                if not building:
                    w = self.workers.filter(lambda x: x.is_gathering or x.is_idle)
                    if w.exists:
                        self.combinedActions.append(w.first(AbilityId.SMART, b))
        for b in self.units(UnitTypeId.SUPPLYDEPOT):
            if not b.is_ready:
                building = False
                for w in self.workers:
                    if w.order_target == b.position or w.order_target == b.tag:
                        building = True
                        break
                if not building:
                    w = self.workers.filter(lambda x: x.is_gathering or x.is_idle)
                    if w.exists:
                        self.combinedActions.append(w.first(AbilityId.SMART, b))

        marines = self.marines
        all_enemy_units = self.all_enemy_units
        enemy_units = self.enemy_units
        close_enemys = self.close_enemys

        if self.workers.amount == 0:
            self.combinedActions.append(cc(AbilityId.LIFT_COMMANDCENTER))

        if self.can_afford(UnitTypeId.SCV) and self.workers.amount < 17 and cc.noqueue:
            self.combinedActions.append(cc.train(UnitTypeId.SCV))

        if (self.supply_left < 3 or (
                self.supply_left < 8 and self.units(UnitTypeId.BARRACKS).amount > 2)) and self.can_afford(
            UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) < 1:
            await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.position.towards(self.rallypoint, 1))

        if self.units(UnitTypeId.SUPPLYDEPOT).exists and (
                self.units(UnitTypeId.BARRACKS).amount < 5 or self.minerals > 350) and self.can_afford(
            UnitTypeId.BARRACKS):
            await self.build(UnitTypeId.BARRACKS, near=cc.position.towards(self.enemy_start_locations[0], 10))

        for rax in self.units(UnitTypeId.BARRACKS).ready.noqueue:
            if (self.minerals > 150 and self.supply_left > 0) or (self.can_afford(UnitTypeId.MARINE) and (
                    self.supply_left > 6 or (
                    self.supply_left > 0 and self.already_pending(UnitTypeId.SUPPLYDEPOT) > 0))):
                self.combinedActions.append(rax.train(UnitTypeId.MARINE))
            else:
                break

        if self.units(UnitTypeId.BARRACKS).exists and self.time < 180 and self.nospam:
            if self.rush:
                self.nospam = False
                self.nospam1 = True
                for b in self.units(UnitTypeId.BARRACKS):
                    self.combinedActions.append(b(AbilityId.RALLY_BUILDING, b.position))
        elif not close_enemys.exists and self.nospam1:
            self.nospam1 = False
            self.nospam = True
            for b in self.units(UnitTypeId.BARRACKS):
                self.combinedActions.append(b(AbilityId.RALLY_BUILDING, self.rallypoint))

        barracksamount = self.units(UnitTypeId.BARRACKS).amount
        if self.barcount < barracksamount:
            self.barcount = barracksamount
            if enemy_units.exists and self.time < 180:
                for b in self.units(UnitTypeId.BARRACKS):
                    self.combinedActions.append(b(AbilityId.RALLY_BUILDING, b.position))
            else:
                for b in self.units(UnitTypeId.BARRACKS):
                    self.combinedActions.append(b(AbilityId.RALLY_BUILDING, self.rallypoint))

        for scv in self.units(UnitTypeId.SCV).idle:
            self.combinedActions.append(scv.gather(self.state.mineral_field.closest_to(cc)))

        if marines.amount > 14 and self.time >= 180 and not self.pushedback and not all_enemy_units(
                UnitTypeId.PHOTONCANNON).filter(lambda x: x.is_powered).exists:
            self.moveout = True

        if not self.moveout and ((enemy_units.exclude_type(
                [UnitTypeId.OVERLORD, UnitTypeId.DRONE, UnitTypeId.PROBE,
                 UnitTypeId.SCV]).exists or enemy_units.exclude_type(
            [UnitTypeId.OVERLORD]).amount > 1) or all_enemy_units(UnitTypeId.PHOTONCANNON).filter(
            lambda x: x.is_powered).exists):
            self.rush = True

        frontmarines = marines.filter(
            lambda x: x.distance_to(self.enemy_start_locations[0]) < self.enemy_start_locations[0].distance_to(
                self.game_info.map_center) - 10)

        if frontmarines.amount > 7 or marines.amount > 22:
            self.pushedback = False
        elif all_enemy_units(UnitTypeId.PHOTONCANNON).filter(
                lambda x: x.is_powered).exists and self.time > 215 and marines.amount < 20:
            self.pushedback = True
        elif self.time > 250 and frontmarines.amount < 6:
            self.pushedback = True
            self.pushbackinit = True
        elif marines.amount > 19 and all_enemy_units(UnitTypeId.PHOTONCANNON).filter(lambda x: x.is_powered).exists:
            self.pushedback = False

        self.micro()

        await self.do_actions(self.combinedActions)

    def micro(self):

        marines = self.marines
        all_enemy_units = self.all_enemy_units
        enemy_units = self.enemy_units
        close_enemys = self.close_enemys
        workers = self.workers
        scvs = self.scvs
        pullback = self.pullback
        repair = self.pulledback
        mining = self.miningworkers

        if close_enemys.exists:
            proxys = self.known_enemy_structures.filter(lambda x: x.distance_to(self.cc) < 15)
            if proxys.exists:
                if proxys(UnitTypeId.HATCHERY).exists:
                    for w in self.workers:
                        self.combinedActions.append(w.attack(all_enemy_units.closest_to(w)))

        if enemy_units.exists and (not self.pushedback or close_enemys.exists):
            for m in marines:
                if not self.basespotted and m.distance_to(self.enemy_start_locations[0]) < 7:
                    self.basespotted = True

                importanttargets = enemy_units.exclude_type(UnitTypeId.OVERLORD)
                if importanttargets.exists:
                    tar = importanttargets.closest_to(m)
                    lowtarg = importanttargets.in_attack_range_of(m).filter(
                        lambda x: (x.health + x.shield) <= (x.health_max + x.shield_max) / 2)
                    if lowtarg.exists:
                        t = lowtarg.first
                        for e in lowtarg:
                            if t.health > e.health:
                                t = e
                        tar = t
                else:
                    tar = enemy_units.closest_to(m)

                if tar.type_id == UnitTypeId.ZEALOT or tar.type_id == UnitTypeId.ZERGLING or tar.type_id == UnitTypeId.DRONE or tar.type_id == UnitTypeId.PROBE or tar.type_id == UnitTypeId.SCV or tar.type_id == UnitTypeId.BANELING:
                    if m.weapon_cooldown == 0:
                        self.combinedActions.append(m.attack(tar))
                    elif m.distance_to(tar) < 4.5:
                        self.combinedActions.append(m.move(m.position.towards(tar.position, distance=-2)))
                    else:
                        self.combinedActions.append(m.move(tar.position))

                elif tar.type_id == UnitTypeId.ADEPT:
                    if m.weapon_cooldown == 0:
                        self.combinedActions.append(m.attack(tar))
                    elif m.distance_to(tar) < 5:
                        self.combinedActions.append(m.move(m.position.towards(tar.position, distance=-2)))
                    else:
                        self.combinedActions.append(m.move(tar.position))
                else:
                    if m.weapon_cooldown == 0 or m.distance_to(tar) < 3:
                        self.combinedActions.append(m.attack(tar))
                    else:
                        self.combinedActions.append(m.move(tar.position))

            # Workerrush/scoutworkerdefense
            if self.defendet:
                if self.defendingworker != 0 and self.workers.find_by_tag(self.defendingworker) is not None:
                    if self.workers.find_by_tag(self.defendingworker).is_attacking:
                        self.combinedActions.append(
                            self.workers.find_by_tag(self.defendingworker).gather(
                                self.state.mineral_field.closest_to(self.cc)))
            enemyworkersattacking = enemy_units(race_worker[self.enemy_race]).filter(
                lambda x: x.distance_to(self.cc) < 16)
            if enemyworkersattacking.exists:  # Defend Workerrush
                self.defendet = False

                if enemyworkersattacking.amount == 1:  # Defend scoutingworker
                    if self.defendingworker == 0 or self.workers.find_by_tag(self.defendingworker) is None:
                        if self.workers.idle.exists:
                            self.defendingworker = self.workers.idle.first.tag
                            self.combinedActions.append(
                                self.workers.find_by_tag(self.defendingworker).attack(enemyworkersattacking.first))
                        elif self.workers.filter(lambda x: x.is_gathering).exists:
                            self.defendingworker = self.workers.filter(lambda x: x.is_gathering).random.tag
                            self.combinedActions.append(
                                self.workers.find_by_tag(self.defendingworker).attack(enemyworkersattacking.first))
                        elif self.workers.exists:
                            self.defendingworker = self.workers.random.tag
                            self.combinedActions.append(
                                self.workers.find_by_tag(self.defendingworker).attack(enemyworkersattacking.first))
                    elif self.workers.find_by_tag(self.defendingworker) is not None:
                        self.combinedActions.append(
                            self.workers.find_by_tag(self.defendingworker).attack(enemyworkersattacking.first))
                elif enemyworkersattacking.amount >= 2:  # actual workerrush
                    if self.wrinit:
                        self.wrinit = False
                        for w in workers:
                            if w.health == 45:
                                if not scvs.__contains__(w.tag):
                                    if pullback.__contains__(w.tag):
                                        pullback.remove(w.tag)
                                        scvs.append(w.tag)
                                    elif repair.__contains__(w.tag):
                                        repair.remove(w.tag)
                                        scvs.append(w.tag)
                                    else:
                                        scvs.append(w.tag)
                        n = 0
                        while n < 4:
                            w = workers.random
                            if scvs.__contains__(w.tag):
                                scvs.remove(w.tag)
                                mining.append(w.tag)
                                n += 1

                    for w in workers:
                        enemy_units_inrange = enemy_units.in_attack_range_of(w)

                        if workers.amount < 8:
                            if len(mining) > 2:
                                scvs.append(mining.pop())
                                scvs.append(mining.pop())

                        if repair.__contains__(w.tag) and w.health >= 35:
                            repair.remove(w.tag)
                            scvs.append(w.tag)

                        if w.health < 10 and len(scvs) + len(repair) > 3:
                            if scvs.__contains__(w.tag):
                                scvs.remove(w.tag)
                                pullback.append(w.tag)
                            if repair.__contains__(w.tag):
                                repair.remove(w.tag)
                                pullback.append(w.tag)

                        if len(scvs) < 4:
                            if not scvs.__contains__(w.tag):
                                if pullback.__contains__(w.tag):
                                    pullback.remove(w.tag)
                                    scvs.append(w.tag)
                                elif repair.__contains__(w.tag):
                                    repair.remove(w.tag)
                                    scvs.append(w.tag)
                                else:
                                    scvs.append(w.tag)

                        if pullback.__contains__(w.tag):
                            if w.distance_to(enemy_units.closest_to(w)) < 1.4:
                                mins = self.state.mineral_field.filter(lambda x: x.distance_to(self.cc) < 10)
                                minfield = mins.first
                                for f in mins:
                                    if f.distance_to(enemy_units.closest_to(w)) > minfield.distance_to(
                                            enemy_units.closest_to(w)):
                                        minfield = f
                                self.combinedActions.append(w.gather(minfield))
                            else:
                                pullback.remove(w.tag)
                                repair.append(w.tag)

                        if repair.__contains__(w.tag):
                            hurtworkers = self.workers.filter(lambda x: x.health < 30 and x != w)

                            if enemy_units_inrange.amount > 1:
                                t = enemy_units_inrange.first
                                for e in enemy_units_inrange:
                                    if t.health > e.health:
                                        t = e

                                self.combinedActions.append(w.attack(t))
                            elif enemy_units_inrange.exists:
                                self.combinedActions.append(w.attack(enemy_units_inrange.first))
                            elif hurtworkers.exists and ((len(repair) < 3 and self.minerals > 10) or (
                                    len(repair) >= 3 and self.minerals > 20)):

                                hurtworkersinrange = hurtworkers.in_attack_range_of(w)

                                if hurtworkersinrange.amount > 1:  # repair low hp scvs first
                                    t = hurtworkersinrange.first
                                    for h in hurtworkersinrange:
                                        if t.health > h.health:
                                            t = h
                                    self.combinedActions.append(
                                        w(AbilityId.EFFECT_REPAIR_SCV,
                                          hurtworkers.closest_to(t)))
                                else:
                                    self.combinedActions.append(
                                        w(AbilityId.EFFECT_REPAIR_SCV,
                                          hurtworkers.closest_to(w)))

                        if scvs.__contains__(w.tag):
                            if self.workers.filter(lambda x: x.health < 15 and x != w).exists and w.distance_to(
                                    enemy_units.closest_to(w)) > 1.5 and self.minerals >= 15:
                                self.combinedActions.append(
                                    w(AbilityId.EFFECT_REPAIR_SCV,
                                      self.workers.filter(lambda x: x.health < 15 and x != w).closest_to(w)))

                            elif enemy_units_inrange.amount > 1:  # when several enemy units in range attack the one with lowest attack
                                target = enemy_units_inrange.first
                                for e in enemy_units_inrange:
                                    if target.health > e.health:
                                        target = e

                                self.combinedActions.append(w.attack(target))
                            else:
                                self.combinedActions.append(w.attack(enemy_units.closest_to(w)))
            else:
                for w in workers:
                    if w.is_attacking:
                        self.combinedActions.append(w.gather(self.state.mineral_field.closest_to(self.cc)))
                self.defendet = True

        elif all_enemy_units.exists and not self.pushedback:
            cannons = all_enemy_units(UnitTypeId.PHOTONCANNON).filter(lambda x: x.is_powered)
            if cannons.exists:
                closestcannon = cannons.closest_to(self.cc)
                pylons = all_enemy_units(UnitTypeId.PYLON).filter(lambda x: x.distance_to(closestcannon) <= 6.5)
                if pylons.exists and pylons.amount == 1 and cannons.amount > 1:
                    tar = pylons.closest_to(closestcannon)
                else:
                    tar = closestcannon
                for m in marines:
                    if m.weapon_cooldown == 0:
                        self.combinedActions.append(m.attack(tar))
                    elif m.distance_to(tar) > 4:
                        self.combinedActions.append(m.move(tar))
            else:
                for m in marines:
                    tar = all_enemy_units.closest_to(m)
                    if m.weapon_cooldown == 0:
                        self.combinedActions.append(m.attack(tar))
                    elif m.distance_to(tar) > 4:
                        self.combinedActions.append(m.move(tar))
        elif self.pushedback:
            if self.pushbackinit:
                self.pushbackinit = False
                for m in marines:
                    self.combinedActions.append(m.attack(self.rallypoint))
        elif self.moveout and not self.basespotted:
            for m in marines:
                tar = self.enemy_start_locations[0]
                self.combinedActions.append(m.attack(tar))
        elif self.moveout and self.basespotted:
            target = Point2((random.randrange(self.game_info.pathing_grid.width),
                             random.randrange(self.game_info.pathing_grid.height)))
            for m in marines.idle:
                self.combinedActions.append(m.attack(target))

        elif self.time < 180:
            for m in marines:
                if m.distance_to(self.rallypoint) > 7:
                    self.combinedActions.append(m.attack(self.rallypoint))


# ---------------------------------------------------------------------------------------------


run_game(maps.get("AcidPlantLE"), [
    Bot(Race.Terran, Ramu()),
    Computer(Race.Zerg, Difficulty.VeryHard)
], realtime=False)
