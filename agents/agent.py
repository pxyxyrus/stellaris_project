from stars import * 


class Agent:

    NUM_OF_AGENTS = 0    

    def __init__(self,star_map: starmap.StarMap, starting_star_index: int):
        self.agent_number = Agent.NUM_OF_AGENTS
        Agent.NUM_OF_AGENTS += 1

        self.current_edge = None
        self.star_map = star_map
        self.visited = [False for _ in range(0, star_map.number_of_stars())]
        self.star_map.stars[starting_star_index].owner = self.agent_number
        self.visited[starting_star_index] = True
        self.current_edge_progress = 0
        self.next_star_index = None


    def play(self):
        # need to implement agent's "unit action"
        # "unit action" could be either of the three actions
        # 1. pick an edge if there is no edge traveling.
        # 2. travel an edge by 1
        # 3. do nothing if nothing is available
        # if an star was taken after calling this function return true
        if self.current_edge is None:
            self.current_edge = self.get_next_edge()
            if self.current_edge is not None:
                idx1, idx2 = self.current_edge.stars[0].index, self.current_edge.stars[1].index
                self.next_star_index = idx1 if self.visited[idx2] else idx2
                self.current_edge.owner = self.agent_number
        else:
            self.current_edge_progress += 1
            if self.current_edge.distance <= self.current_edge_progress:
                self.visited[self.next_star_index] = True
                self.star_map.stars[self.next_star_index].owner = self.agent_number
                self.current_edge_progress = 0
                self.current_edge = None
                self.next_star_index = None
                return True
        return False

    def get_next_edge(self) -> starpath.StarPath:
        # implement an algorithm that decides which edge to take next
        pass


# Default Agent
class StupidAgent(Agent):

    def __init__(self, star_map: starmap.StarMap, starting_star_index: int):
        super().__init__(star_map, starting_star_index) 

    def get_next_edge(self) -> starpath.StarPath:
        for i in range(0, len(self.visited)):
            if self.visited[i]:
                for j in range(0, self.star_map.adjacency_matrix.shape[0]):
                    if not self.visited[j]:
                        distance = self.star_map.is_connected(i, j)
                        if distance != 0 and not self.star_map.star_path_dict[i][j].owner:
                            return self.star_map.star_path_dict[i][j]



# Our Agent using dijkstra's Algorithm
class GreedyAgent(Agent):

    def __init__(self, star_map: starmap.StarMap, starting_star: int):
        super().__init__(star_map, starting_star)

    def get_next_edge(self) -> starpath.StarPath:
        pass
    
        


