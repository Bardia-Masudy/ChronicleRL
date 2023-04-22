## An element of each gamemap, should contain a list of each light source 
## that exists in it, pushed by each actor with a light component.
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

from components.light import Light

import numpy as np
from numpy.typing import NDArray

class LightMap():
    parent: GameMap

    def __init__(self, width: int, height: int) -> None:
        self.lights: set[Light] = set()
        self.tiles = np.full((width, height), 0, order="F") # 0: impassible, +N: +N cost to traversing

    def update_map(self) -> None:
        self.tiles[np.where(self.parent.tiles["walkable"] == True)] = 1

    def add_node(self, location: tuple[int, int], radius: int):
        self.tiles[location] = radius
    
    def process_map(self):
        neighbours: set[tuple[int, int]] = set() # x, y tiles with lights, and eventually, neibouring cells lit up

        self.update_map()
        for light in self.lights:
            light.push_location()
            neighbours.add(light.location)

        while neighbours:
            tile = neighbours.pop()
            x, y = tile.location
            for neighbour in [[x-1, y-1],[x, y-1],[x+1, y-1],
                              [x-1, y  ],         [x+1, y  ],
                              [x-1, y+1],[x, y+1],[x+1, y+1]]:
                pass

        




"""
Each actor with a light is stored in a list in the lightmap.
the lightmap is stored in each gamemap.
the lightmap gets tiles from the gamemap, after procgen.generate_dungeon() runs
the lightmap needs a function that runs a djikstra map every frame, taking each node and value to find every lit up tile.
that needs to get fed into the engine, to show where the player and enemies can see (can enemies see in the dark or not) 
"""