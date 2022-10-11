import starmap
import star

def load_map(map_name):
    map_name = map_name.replace(" ", "_")
    map_dir = "./maps/{0}".format(map_name)
    path_to_file = "{0}/{1}.map".format(map_dir, map_name)

    with open(path_to_file, "r") as f:
        num_of_stars = int(next(f))
        stars = [None for i in range(0, num_of_stars)]
        for _ in range(0, num_of_stars):
            line = next(f)
            strs = line.split()
            star_num, x, y = int(strs[0]), float(strs[1]), float(strs[2])
            stars[star_num] = star.Star(x, y)
        starMap = starmap.StarMap(stars)
        for line in f:
            strs = line.split()
            star1, star2, distance = int(strs[0]), int(strs[1]), int(strs[2])
            starMap.add_star_path(star1, star2, distance)
    return starMap
