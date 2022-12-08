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



def gen_mean(all_maps_dir: str):
    lines_to_write = []
    for j in [200, 400, 600, 800, 1000]: 
        agent1_mean = 0
        agent2_mean = 0
        agent1_name = ""
        agent2_name = ""
        cnt = 0
        with open( "{}/statistics{}.csv".format(all_maps_dir, j), "r") as f:
            print(f.readline())
            agent1_name, agent2_name = f.readline().strip().split(",")

            for line in f:
                agent1_num, agent2_num = line.split(',')
                agent1_mean += int(agent1_num)
                agent2_mean += int(agent2_num)
                cnt += 1


        agent1_mean /= cnt
        agent2_mean /= cnt

        lines_to_write.append("{} stars statistic\n".format(j))
        lines_to_write.append("{} mean : {}\n".format(agent1_name, agent1_mean))
        lines_to_write.append("{} mean : {}\n\n".format(agent2_name, agent2_mean))
        

    with open("{}/mean.txt".format(all_maps_dir, j), "w") as f:
        f.writelines(lines_to_write)



def gen_stats_when_agent_won(all_maps_dir: str): 
    lines_to_write = []
    for j in [200, 400, 600, 800, 1000]:
        agent1_name = ""
        agent2_name = ""
        agent1_win_agent1_mean = 0
        agent1_win_agent2_mean = 0
        agent2_win_agent1_mean = 0
        agent2_win_agent2_mean = 0
        agent1_win_count = 0
        agent2_win_count = 0
        with open( "{}/statistics{}.csv".format(all_maps_dir, j), "r") as f:
            print(f.readline())
            agent1_name, agent2_name = f.readline().strip().split(",")
            
            for line in f:                
                agent1_num, agent2_num = line.split(',')
                agent1_num = int(agent1_num)
                agent2_num = int(agent2_num)
                if agent1_num > agent2_num:
                    agent1_win_agent1_mean += agent1_num
                    agent1_win_agent2_mean += agent2_num
                    agent1_win_count += 1
                elif agent1_num < agent2_num:
                    agent2_win_agent1_mean += agent1_num
                    agent2_win_agent2_mean += agent2_num
                    agent2_win_count += 1

        agent1_win_agent1_mean /= agent1_win_count
        agent1_win_agent2_mean /= agent1_win_count

        agent2_win_agent1_mean /= agent2_win_count
        agent2_win_agent2_mean /= agent2_win_count

        lines_to_write.append("{} stars statistic\n".format(j))
        lines_to_write.append("{} win statistics\n".format(agent1_name))
        lines_to_write.append("{} games\n".format(agent1_win_count))
        lines_to_write.append("{} mean : {}\n".format(agent1_name, agent1_win_agent1_mean))
        lines_to_write.append("{} mean : {}\n".format(agent2_name, agent1_win_agent2_mean))
        lines_to_write.append("diff: {}\n\n".format(agent1_win_agent1_mean - agent1_win_agent2_mean))

        lines_to_write.append("{} win statistics\n".format(agent2_name))
        lines_to_write.append("{} games\n".format(agent2_win_count))
        lines_to_write.append("{} mean : {}\n".format(agent1_name, agent2_win_agent1_mean))
        lines_to_write.append("{} mean : {}\n".format(agent2_name, agent2_win_agent2_mean))
        lines_to_write.append("diff: {}\n\n".format(agent2_win_agent2_mean - agent2_win_agent1_mean))

    with open("{}/win_stats.txt".format(all_maps_dir, j), "w") as f:
        f.writelines(lines_to_write)




if __name__ == "__main__":
    all_maps_dir = input("all_maps_dir? ")
    # generate_csv(all_maps_dir)
    gen_mean(all_maps_dir)
    gen_stats_when_agent_won(all_maps_dir)
    