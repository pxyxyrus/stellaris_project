import numpy as np
from pathlib import Path


# map_dir = "./greedy_vs_slicing_maps"
# map_dir = "./greedy_vs_stupid_maps"
# map_dir = "./slicing_vs_stupid_maps"

def generate_csv(all_maps_dir: str):
    for j in [1, 201, 401, 601, 801]: 
        stats = []
        agent_names_added = False

        agent1_sum = 0
        agent2_sum = 0

        stats.append('Map Size {}\n'.format(j + 199))

        
        for i in range(j, j + 200):
            map_name = "map{}".format(i)
            current_map_dir = "{}/{}".format(all_maps_dir, map_name)

            k = 1
            while True:
                game_name = "game{}".format(k)
                game_dir = "{}/{}".format(current_map_dir, game_name)
                print(game_dir)
                if Path(game_dir).resolve().exists():
                    with open( "{}/statistics.csv".format(game_dir), "r") as f:
                        f.readline()
                        line = f.readline()
                        agent1_name, agent1_num = line.split(',')
                        agent1_num = int(agent1_num)
                        
                        line = f.readline()
                        agent2_name, agent2_num = line.split(',')
                        agent2_num = int(agent2_num)

                        if not agent_names_added:
                            agent_names_added = True
                            stats.append("{}, {}\n".format(agent1_name, agent2_name))
                        stats.append("{}, {}\n".format(agent1_num, agent2_num))


                        agent1_sum += agent1_num
                        agent2_sum += agent2_num
                else:
                    break

                k += 1
        

        with open( "{}/statistics{}.csv".format(all_maps_dir, j+199), "w") as f2:
            f2.writelines(stats)



if __name__ == "__main__":
    all_maps_dir = input("all_maps_dir? ")
    generate_csv(all_maps_dir)
    