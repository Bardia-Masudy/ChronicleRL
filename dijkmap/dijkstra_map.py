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
        # set of neightbours for spread() function
        self.neighbours = set()
        # tile map corresponding to stimulus levels (smell, sound, etc.)
        self.tiles = np.full((self.height, self.width), fill_value= -1)
        self.tiles[np.where(closed_map == "#")] = 0
        # tile map corresponding to spaces where stimulus can spread
        # potential in the future for 0-9 ranking of impedment?
        #self.closed = np.full((self.height, self.width), fill_value=True)


    def add_node(self, source: tuple[int, tuple[int, int]]) -> None:
        """Add volume node of a specific intensity to the tile map."""
        self.tiles[source[1]] = source[0]
        self.neighbours.add(source[1])

    def render(self) -> None:
        print(np.matrix(self.tiles))

    def process(self) -> None:
        while self.neighbours:
            tile = self.neighbours.pop()
            volume = self.tiles[tile]
            x, y = tile
            #self.closed[(x, y)] = True
            for i in [x-1, x, x+1]:
                for j in [y-1, y, y+1]:
                    #test for in-bounds here too
                    if -1 < self.tiles[(i, j)] < volume:
                        self.tiles[(i, j)] = volume - 1
                        self.neighbours.add((i, j))

testmap = SoundMap(test_dungeon.tiles)
testmap.add_node((9, test_dungeon.player_xy))
testmap.add_node((9, (10,10)))
testmap.process()
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