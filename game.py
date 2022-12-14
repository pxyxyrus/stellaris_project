from lib.file.saveloadmap import MAPS_DIRECTORY, load_map
from lib.agents.agent import *
from lib.file.saveloadmap import save_map
from lib.stars import *
import numpy as np
from pathlib import Path
from visualize import visualize_starmap
import time


# Basic idea 

# 1. Create an star map
# 2. Create agents
# 3. for each agent -> call play
# 4. agents will do a unit action which is traveling "1" edge length
# 5. Stop when all of the stars are taken


def start_game(agents: list[Agent], star_map: StarMap, visualize=False):
    if len(agents) == 0:
        raise Exception("There is no agent to play the game.")

    print("Start!")
    while(not star_map.is_all_stars_owned()):
        for ag in agents:
            result = ag.play()
            if star_map.is_all_stars_owned():
                break
            if result:
                if visualize:
                    visualize_starmap(star_map, star_map.get_star_position())
                    time.sleep(0.05)
    
    if visualize:
        visualize_starmap(star_map, star_map.get_star_position(), True)
    print("End!")




if __name__ == "__main__":
    map_name = input("type in the map name\n")
    map_dir = map_name
    path_name = MAPS_DIRECTORY + "/" + map_dir
    star_map = load_map(path_name, map_name=map_name)
    agents = []
        
    starting_star_indices = []
    def random_star_index():
        while(True):
            ridx = np.random.randint(0, len(star_map.stars))
            if ridx in starting_star_indices:
                continue
            else:
                starting_star_indices.append(ridx)
                return ridx

    agents.append(GreedyAgent(star_map, random_star_index(), len(agents)))
    agents.append(StupidAgent(star_map, random_star_index(), len(agents)))
    # agents.append(StupidAgent(star_map, random_star_index(), len(agents)))
    # agents.append(StupidAgent(star_map, random_star_index(), len(agents)))

    game_folder = ""
    i = 1
    while(True):
        game_folder = "game{}".format(i)
        if not Path("{}/{}".format(path_name, game_folder)).resolve().exists():
            Path("{}/{}".format(path_name, game_folder)).mkdir(parents=True, exist_ok=True)
            save_map(star_map, "{}/{}".format(path_name, game_folder), "start")
            break
        i += 1


    start_game(agents, star_map, True)

    save_map(star_map, "{}/{}".format(path_name, game_folder), "result")


