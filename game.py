from cmath import inf
from saveloadmap import MAPS_DIRECTORY, load_map
from agents.agent import *
from saveloadmap import save_map
from stars import *
import numpy as np
from pathlib import Path


# Basic idea 

# 1. Create an star map
# 2. Create agents
# 3. for each agent -> call play
# 4. agents will do a unit action which is traveling "1" edge length
# 5. Stop when all of the stars are taken


def start_game(agents: list[Agent], star_map: StarMap):
    if len(agents) == 0:
        raise Exception("There is no agent to play the game.")
    while(not star_map.is_all_stars_owned()):
        for ag in agents:
            result = ag.play()
            if star_map.is_all_stars_owned():
                break
    
    print(star_map.is_all_stars_owned())

    print("End!")




if __name__ == "__main__":
    map_name = input("type in the map name\n")
    map_dir = map_name
    star_map = load_map(map_dir=map_dir, map_name=map_name)
    agents = []
    
    random_star_index = lambda : np.random.randint(0, len(star_map.stars))

    agents.append(StupidAgent(star_map, random_star_index()))

    path_name = MAPS_DIRECTORY + "/" + map_dir
    game_folder = ""
    i = 1
    while(True):
        game_folder = "game{}".format(i)
        if not Path("{}/{}".format(path_name, game_folder)).resolve().exists():
            Path("{}/{}".format(path_name, game_folder)).mkdir(parents=True, exist_ok=True)
            save_map(star_map, "{}/{}".format(map_dir, game_folder), "start")
            break

    start_game(agents, star_map)

    save_map(star_map, "{}/{}".format(map_dir, game_folder), "result")


