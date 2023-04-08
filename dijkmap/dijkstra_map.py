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
        self.height, self.width = closed_map.shape
        self.neighbours = set()
        # tile map corresponding to where stimulus can travel (smell, sound, etc.)
        self.tiles = np.full((self.height, self.width), fill_value= -1)
        self.tiles[np.where(closed_map == "#")] = 0 # Open

    def render(self) -> None:
        print(np.matrix(self.tiles))

    def add_node(self, node: tuple[int, tuple[int, int]]) -> None:
        self.neighbours.add(node[1])
        self.tiles[node[1]] = node[0]

    def process_nodes(self) -> None:
        while self.neighbours:
            new_neighbours = set()
            for tile in self.neighbours:
                x, y = tile
                intensity = self.tiles[tile]
                if intensity > 1:
                    for i in [x-1, x, x+1]:
                        for j in [y-1, y, y+1]:
                            #test for in-bounds here too
                            if (i, j) != (x, y) and intensity > self.tiles[(i, j)] > -1:
                                self.tiles[(i, j)] = intensity - 1
                                new_neighbours.add((i, j))
                self.neighbours = new_neighbours
    
    def can_feel(self, target: tuple[int, int], start: tuple[int, int], distance: int) -> bool:
        pass
        #stimulus_map = self.process_node()


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