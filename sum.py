import numpy as np

for j in [1, 201, 401, 601, 801]: 
    agent1_sum = 0
    agent2_sum = 0

    for i in range(j, j + 200):
        map_name = "map{}".format(i)


        with open( "./maps/{}/game3/statistics.csv".format(map_name), "r") as f:
            agent=f.readline()
            line = f.readline()
            agent1_name, agent1_num = line.split(',')
            line = f.readline()
            agent2_name, agent2_num = line.split(',')

            agent1_num = int(agent1_num)
            agent2_num = int(agent2_num)
            agent1_sum += int(agent1_num)
            agent2_sum += int(agent2_num)
            
            if agent1_num * 2 < agent2_num or agent2_num * 2 < agent1_num:
                print(map_name, agent1_num - agent2_num)
            # if agent1_num < agent2_num:
                # print(map_name, agent2_num - agent1_num)


  

    print(agent1_name)
    print(agent1_sum / 200)
    print(agent2_name)
    print(agent2_sum / 200)
    print()

# 200 node maps average
# 127.6 Greedy
# 72.4  Random

# 400 node maps average
# 261.495 Greedy
# 138.505 Random


# 600
# 395.42 Greedy
# 204.58 Random

# 800
# 530.16 Greedy
# 269.84 Random

# 1000
# 664.42 Greedy
# 335.58 Random



