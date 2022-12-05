from lib.file.saveloadmap import MAPS_DIRECTORY, load_map, save_map
from lib.agents.agent import *
from lib.stars import *
import numpy as np
from pathlib import Path
from game import start_game




if __name__ == "__main__":    
    reps = int(input("how many repititions per map?"))
    MAPS_DIRECTORY = "./greedy_vs_slicing_maps"
    for i in range(1, 1001):
        for _ in range(0, reps): 
            map_name = "map{}".format(i)
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
            agents.append(SlicingAgent(star_map, random_star_index(), len(agents)))
            # agents.append(StupidAgent(star_map, random_star_index()))
            # agents.append(StupidAgent(star_map, random_star_index()))

            game_folder = ""
            j = 1
            while(True):
                game_folder = "game{}".format(j)
                if not Path("{}/{}".format(path_name, game_folder)).resolve().exists():
                    Path("{}/{}".format(path_name, game_folder)).mkdir(parents=True, exist_ok=True)
                    save_map(star_map, "{}/{}".format(path_name, game_folder), "start")
                    break
                j += 1

            print("Game{}".format(i))
            start_game(agents, star_map)

            save_map(star_map, "{}/{}".format(path_name, game_folder), "result")
            with open("{}/{}/{}".format(path_name, game_folder, "statistics.csv"), "w") as f:
                f.write("{}, {}\n".format("agent_type", "nodes_taken"))
                for agent in agents:
                    cnt = 0
                    for st in star_map.stars:
                        if st.owner == agent.agent_number:
                            cnt += 1
                    f.write("{}, {}\n".format(type(agent).__name__, cnt))


