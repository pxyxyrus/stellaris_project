




for j in [1, 201, 401, 601, 801]: 
    greedy_sum = 0
    default_sum = 0

    for i in range(j, j + 200):
        map_name = "map{}".format(i)


        with open( "./maps/{}/game1/statistics.csv".format(map_name), "r") as f:
            f.readline()
            line = f.readline()
            _, greedy_num = line.split(',')
            line = f.readline()
            _, default_num = line.split(',')
            print(greedy_num, default_num)

            greedy_sum += int(greedy_num)
            default_sum += int(default_num)

    print(greedy_sum)  
    print(default_sum)

    print(greedy_sum / 200)
    print(default_sum / 200)

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



