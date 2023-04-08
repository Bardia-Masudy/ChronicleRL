import numpy as np
from numpy.typing import NDArray
from placeholder_map import generate_dungeon

test_dungeon = generate_dungeon(
    max_rooms=10,
    room_max_size=7,
    room_min_size=3,
    map_width=20,
    map_height=18
)

class SoundMap:
    def __init__(self, closed_map: NDArray):
        self.neighbours = set()
        
        # tile map tracking strength of stimulus
        self.tiles = np.full((closed_map.shape), fill_value= 0)

        # tile map corresponding to how easily stimulus can travelover tiles. (1-9 where 9 is total blocking)
        self.closed = np.full((closed_map.shape), fill_value= 9)
        self.closed[np.where(closed_map == "#")] = 1 # Base level of impedence

    def render(self) -> None:
        print(np.matrix(self.tiles))

    def add_node(self, node: tuple[int, tuple[int, int]]) -> None:
        self.neighbours.add(node[1])
        self.tiles[node[1]] = node[0]

    def process_nodes(self) -> None:
        while self.neighbours:
            tile = self.neighbours.pop()
            x, y = tile
            intensity = self.tiles[tile]
            if intensity > 1:
                for neighbour in [  (x-1, y-1), (x  , y-1), (x+1, y-1),
                                    (x-1, y  ),             (x+1, y  ),
                                    (x-1, y+1), (x  , y+1), (x+1, y+1)]:
                    new_intensity = max(0, intensity - self.closed[neighbour])
                    #test for in-bounds here too
                    if intensity > self.tiles[neighbour] > -1:
                        self.tiles[neighbour] = new_intensity
                        self.neighbours.add(neighbour)
    
    def can_feel(self, start: tuple[int, int]) -> bool:
        return self.tiles[start] > 0


testmap = SoundMap(test_dungeon.tiles)
print(test_dungeon.player_xy)
testmap.add_node((9, test_dungeon.player_xy))
testmap.add_node((9, (9, 9)))
testmap.process_nodes()
testmap.render()


print(np.matrix(test_dungeon.tiles))
#print(np.where(test_dungeon.tiles == "#"))


"""How the SoundMap works:
1. __init__
2. add sources (each is a tuple(int, int) for coordinate and an int for volume)
3. engine/wherever will begin processing, which will loop through a spread function
4. spread function takes closed_map, open_map, and list of neighbours. calculates new neightbours and adds old neighbours to closed map.
                - THIS WILL CAUSE BUGS, LOUD SOUNDS WILL BE ABLE TO BE DROWNED OUT BY CLOSER QUIET SOUNDS
                - MAKE INSTEAD CALCULATE EACH SOUND INDIVIDUALLY, AND OVERLAY MAPS (Take Greater?)
5. once spread function is done, return open map with sound volumes at each tile."""