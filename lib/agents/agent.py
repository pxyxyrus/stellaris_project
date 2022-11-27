from typing import Tuple
from enum import Enum
import numpy as np
from lib.stars import * 
import heapq

class Agent: 

    def __init__(self,star_map: starmap.StarMap, starting_star_index: int, agent_number: int):
        self.agent_number = agent_number

        self.star_map = star_map
        self.visited = [False for _ in range(0, star_map.number_of_stars())]
        self.next_star_index = starting_star_index
        self._arrived()


    def play(self, turns=1) -> bool:
        # need to implement agent's "unit action"
        # "unit action" could be either of the four actions
        # 1. pick an edge if there is no edge traveling.
        # 2. travel an edge by 1.
        # 3. if the current edge that the agent is traveling leads to an node that is taken,
        #    reset the traveling edge.
        # 4. do nothing if nothing is available.
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

    # function that is called when the agent finishes traveling an edge and arrives to a node
    def _arrived(self):
        if self.star_map.stars[self.next_star_index].owner is None:
            self.star_map.stars[self.next_star_index].owner = self.agent_number
            self.visited[self.next_star_index] = True
        self._reset_current_edge()

    # reset the current traveling edge info
    def _reset_current_edge(self):
        self.current_edge_progress = 0
        self.current_edge = None
        self.next_star_index = None

    def get_next_edge(self) -> starpath.StarPath:
        # implement an algorithm that decides which edge to take next
        pass
    
    def get_current_edge_progress(self):
        return self.current_edge.distance - self.current_edge_progress

    # kind of a buggy code
    # we assume that the edge passed in has one star visited and the other one not
    def get_unvisited_star_from_edge(self, edge: starpath.StarPath) -> Star:
        idx1, idx2 = edge.stars[0].index, edge.stars[1].index
        return self.star_map.stars[idx1 if self.visited[idx2] else idx2]




# Default Agent
# Picks random edge that leads to an untaken node
class StupidAgent(Agent):

    def __init__(self, star_map: starmap.StarMap, starting_star_index: int, agent_number: int):
        # this is just adding star indices in the list
        self.visited_star_list = []
        super().__init__(star_map, starting_star_index, agent_number) 

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



# Agent using dijkstra's Algorithm of edge weights
class GreedyAgent(Agent):

    def __init__(self, star_map: starmap.StarMap, starting_star_index: int, agent_number: int):
        self._heap = []
        super().__init__(star_map, starting_star_index, agent_number)


    def get_next_edge(self) -> starpath.StarPath:
        while len(self._heap) != 0:
            edge = self._pop()
            other_star = self.get_unvisited_star_from_edge(edge)
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
        heapq.heappush(self._heap, edge)

    def _pop(self) -> starpath.StarPath:
        return heapq.heappop(self._heap)

    def _peek(self) -> starpath.StarPath:
        return self._heap[0]

    

    
        

# Same as dijikstra's agent
# But onemore condition
# 1. prioritizes which ever edge that increases distance in the axis-direction
# 2. then it prioritizes edge distance
class SlicingAgent(Agent):

    class SlicingDirection(Enum):
        HORIZONTAL=1
        VERTICAL=2

    def __init__(self, star_map: starmap.StarMap, starting_star_index: int, agent_number: int, invert: bool=False):
        self._heap1 = [] # positive direction
        self._heap2 = [] # negative direction
        self._heap3 = [] # edge weight
        self.starting_star = star_map.stars[starting_star_index]
        
        if np.abs(self.starting_star.x) > np.abs(self.starting_star.y):
            if invert:
                self.slicing_direction = self.SlicingDirection.VERTICAL
            else: 
                self.slicing_direction = self.SlicingDirection.HORIZONTAL
            self.max_star_coord = self.starting_star.x
            self.min_star_coord = self.starting_star.x
        else:
            if invert:
                self.slicing_direction = self.SlicingDirection.HORIZONTAL
            else: 
                self.slicing_direction = self.SlicingDirection.VERTICAL
            self.max_star_coord = self.starting_star.y
            self.min_star_coord = self.starting_star.y
        super().__init__(star_map, starting_star_index, agent_number)


    def get_next_edge(self) -> starpath.StarPath:
        heaplist = []
        if (self.slicing_direction == self.SlicingDirection.HORIZONTAL and self.starting_star.x > 0) or\
            (self.slicing_direction == self.SlicingDirection.VERTICAL and self.starting_star.y > 0):
            heaplist = [self._heap1, self._heap2, self._heap3]
        else:
            heaplist = [self._heap2, self._heap1, self._heap3]

        for heap in heaplist:
            while len(heap) != 0:
                _, edge = self._pop(heap)
                other_star = self.get_unvisited_star_from_edge(edge)
                if edge.owner is None and other_star.owner is None:
                    return edge
        return None


    def _arrived(self):
        if self.slicing_direction == self.SlicingDirection.HORIZONTAL:
            self.max_star_coord = max([\
                self.star_map.stars[self.next_star_index].x, self.max_star_coord\
            ])
            self.min_star_coord = max([\
                self.star_map.stars[self.next_star_index].x, self.min_star_coord\
            ])
        elif self.slicing_direction == self.SlicingDirection.VERTICAL:
            self.max_star_coord = max([\
                self.star_map.stars[self.next_star_index].y, self.max_star_coord\
            ])
            self.min_star_coord = max([\
                self.star_map.stars[self.next_star_index].y, self.min_star_coord\
            ])
        for connected_star_index in self.star_map.star_path_dict[self.next_star_index]:
            edge = self.star_map.star_path_dict[self.next_star_index][connected_star_index]
            if edge.owner is None and self.star_map.stars[connected_star_index].owner is None:
                st = self.star_map.stars[connected_star_index]
                if self.slicing_direction == self.SlicingDirection.HORIZONTAL:
                    if st.x > self.max_star_coord:
                        self._push(self._heap1, st.x * -1, edge)
                        # since the heap always returns min, multiply -1 to make it to max heap
                    elif st.x < self.min_star_coord:
                        self._push(self._heap2, st.x, edge)
                elif self.slicing_direction == self.SlicingDirection.VERTICAL:
                    if st.y > self.max_star_coord:
                        self._push(self._heap1, st.y * -1, edge)
                        # since the heap always returns min, multiply -1 to make it to max heap
                    elif st.y < self.min_star_coord:
                        self._push(self._heap2, st.y, edge)
                
                self._push(self._heap3, edge.distance, edge)

        super()._arrived()


    # based on the direction we pick (horizontal <-> X axis, vertical <-> Y-axis)
    def _push(self, heap, num: int, edge: starpath.StarPath):
        heapq.heappush(heap, (num, edge))

    def _pop(self, heap) -> Tuple[int, starpath.StarPath]:
        return heapq.heappop(heap)

    def _peek(self, heap) -> Tuple[int, starpath.StarPath]:
        return heap[0]
