import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer, Human

# StarCraftII Start
run_game(maps.get("AbyssalReefLE")), [
    Bot(Race.Protoss, SentdeBot(use_model=False, title=1)),
    Computer(Race.Protoss, Difficulty.Easy)],
    realtime=False)
