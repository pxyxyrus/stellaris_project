import numpy as np



stats = []
for game in ['game1', 'game2', 'game3']:
    if 'game1':
        stats.append('Greedy vs Stupid\n')
    elif 'game2':
        stats.append('Slicing vs Stupid\n')
    elif 'game3':
        stats.append('Greedy vs Slicing\n')
    stats.append('\n')
    for j in [1, 201, 401, 601, 801]: 
        agent1_sum = 0
        agent2_sum = 0

        stats.append('Map Size {}\n'.format(j + 200))
        max_gap = 0
        max_gap_maps = []
        
        for i in range(j, j + 200):
            map_name = "map{}".format(i)


            with open( "./maps/{}/{}/statistics.csv".format(map_name, game), "r") as f:
                agent=f.readline()
                line = f.readline()
                agent1_name, agent1_num = line.split(',')
                line = f.readline()
                agent2_name, agent2_num = line.split(',')

                agent1_num = int(agent1_num)
                agent2_num = int(agent2_num)
                agent1_sum += agent1_num
                agent2_sum += agent2_num
                
                gap = np.abs(agent1_num - agent2_num)
                if max_gap < gap:
                    max_gap = gap
                    max_gap_maps = [map_name]
                elif max_gap == gap:
                    max_gap_maps.append(map_name)
        

    
        stats.append("Summary\n")
        stats.append("{} {}\n".format(agent1_name, agent1_sum / 200))
        stats.append("{} {}\n".format(agent2_name, agent2_sum / 200))
        stats.append("\n")

        stats.append("Map(s) with biggest gap({})\n".format(max_gap))
        for ll in  max_gap_maps:
            stats.append("{} ".format(ll))  
        stats.append("\n")

with open( "./maps/stats.txt", "w") as f2:
    f2.writelines(stats)


