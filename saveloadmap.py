from stars.star import * 
from stars.starmap import *
# from pathlib import Path


MAPS_DIRECTORY = "./maps"


def load_map(map_dir: str, map_name: str) -> StarMap:
    map_name = map_name.replace(" ", "_")
    map_dir = map_dir if map_dir is not None else MAPS_DIRECTORY + "/" + map_name
    path_to_file = "{0}/{1}.map".format(map_dir, map_name)

    with open(path_to_file, "r") as f:
        num_of_stars = int(next(f))
        stars = [None for _ in range(0, num_of_stars)]
        for i in range(0, num_of_stars):
            line = next(f)
            strs = line.split()
            star_num, x, y = int(strs[0]), float(strs[1]), float(strs[2])
            stars[star_num] = Star(x, y, i)
            if len(strs) > 3 and strs[3] != 'None':
                stars[star_num].owner = int(strs[3])
        star_map = StarMap(stars)
        for line in f:
            strs = line.split()
            star1, star2, distance = int(strs[0]), int(strs[1]), int(strs[2])
            owner = None
            if len(strs) > 3 and strs[3] != 'None':
                owner = int(strs[3])
            star_map.add_star_path(star1, star2, distance, owner)
    return star_map




def save_map(star_map: StarMap, map_dir: str, map_name: str):
    path_to_file = "{0}/{1}.map".format(map_dir, map_name)  
    with open(path_to_file, "w") as f:
        lines_to_write = ["{0}\n".format(star_map.number_of_stars())]
        index = 0
        for st in star_map.stars:
            lines_to_write.append("{0} {1} {2} {3}\n".format(index, st.x, st.y, st.owner))
            index += 1
        
        for stp in star_map.star_paths:
            lines_to_write.append("{0} {1} {2} {3}\n".format(stp.stars[0].index, stp.stars[1].index, stp.distance, stp.owner))

        f.writelines(lines_to_write)