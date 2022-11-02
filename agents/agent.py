from typing import Tuple
from stars import * 
import heapq

class Agent: 

    def __init__(self,star_map: starmap.StarMap, starting_star_index: int, agent_number: int):
        self.agent_number = agent_number

        self.star_map = star_map
        self.visited = [False for _ in range(0, star_map.number_of_stars())]
        self.next_star_index = starting_star_index
        self._arrived()


    def play(self, turns=1):
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
                return False if turns == 0 else self.play(turns - 1)
        elif self.star_map.stars[self.next_star_index].owner != self.agent_number and\
                self.star_map.stars[self.next_star_index].owner is not None:
            self._reset_current_edge()
            return False if turns == 0 else self.play(turns - 1)
        else:
            self.current_edge_progress += turns
            if self.current_edge.distance <= self.current_edge_progress:
                self._arrived()
                return True
        return False

    def _arrived(self):
        if self.star_map.stars[self.next_star_index].owner is None:
            self.star_map.stars[self.next_star_index].owner = self.agent_number
            self.visited[self.next_star_index] = True
        self._reset_current_edge()

    def _reset_current_edge(self):
        self.current_edge_progress = 0
        self.current_edge = None
        self.next_star_index = None

    def get_next_edge(self) -> starpath.StarPath:
        # implement an algorithm that decides which edge to take next
        pass
    
    def get_current_edge_progress(self):
        return self.current_edge.distance - self.current_edge_progress



# Default Agent
class StupidAgent(Agent):

    def __init__(self, star_map: starmap.StarMap, starting_star_index: int):
        self.visited_star_list = []
        super().__init__(star_map, starting_star_index) 

    def get_next_edge(self) -> starpath.StarPath:
        for i in self.visited_star_list:
            for j in self.star_map.star_path_dict[i].keys():
                if not self.visited[j]:
                    distance = self.star_map.is_connected(i, j)
                    if distance != 0 and self.star_map.star_path_dict[i][j].owner is None and self.star_map.stars[j].owner is None:
                        return self.star_map.star_path_dict[i][j]

    def _arrived(self):
        self.visited_star_list.append(self.next_star_index)
        super()._arrived()



# Our Agent using dijkstra's Algorithm
class GreedyAgent(Agent):

    def __init__(self, star_map: starmap.StarMap, starting_star: int):
        self._heap = []
        super().__init__(star_map, starting_star)


    def get_next_edge(self) -> starpath.StarPath:
        if len(self._heap) != 0:
            while len(self._heap) != 0:
                _, edge = self._pop()
                idx1, idx2 = edge.stars[0].index, edge.stars[1].index
                other_star = self.star_map.stars[idx1 if self.visited[idx2] else idx2]
                if edge.owner is None and other_star.owner is None:
                    return edge
        return None

    def _arrived(self):
        for connected_star_index in self.star_map.star_path_dict[self.next_star_index]:
            edge = self.star_map.star_path_dict[self.next_star_index][connected_star_index]
            if edge.owner is None and self.star_map.stars[connected_star_index].owner is None:
                self._push(edge)
        super()._arrived()


    def _push(self, edge: starpath.StarPath):
        heapq.heappush(self._heap, (edge.distance, edge))

    def _pop(self) -> Tuple[int, starpath.StarPath]:
        return heapq.heappop(self._heap)

    
        


