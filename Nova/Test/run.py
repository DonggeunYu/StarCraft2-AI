import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer, Human
from Nova import main

# StarCraftII Start
run_game(maps.get("AbyssalReefLE")), [
    Bot(Race.Protoss, main(title=1)),
    Computer(Race.Protoss, Difficulty.Easy)],
    realtime=False)
