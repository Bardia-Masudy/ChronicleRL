from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import TYPE_CHECKING

import colour
import tile_types # TODO: move this to procgen generation script?

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor

class SoundMap:
    def __init__(self, array: NDArray, engine: Engine):
        self.engine = engine
        self.array = array
        self.neighbours = set()

        # tile map tracking strength of stimulus
        self.tiles = np.full((self.array.shape), fill_value= 0)

        self.update_costs()

    def update_costs(self) -> None:
        # tile map corresponding to how easily stimulus can travel over tiles. (1-9 where 9 is total blocking)
        self.costs = np.full((self.array.shape), fill_value= 9)
        self.costs[np.where(self.array["walkable"] == True)] = 1 # Base level of impedence

    def handle_player(self): # TODO: This whole thing is temporary, entities should all emit and register sound, then behave accordingly.
        #self.add_node((9,(self.engine.player.x, self.engine.player.y)))
        self.process_nodes()
        for actor in self.engine.game_map.actors: 
            if actor.name != "Player" and self.can_feel((actor.x, actor.y)):
                self.engine.message_log.add_message(
                    f"{actor.name} can hear you.", colour.enemy_atk
                )

    def render(self):
        return np.where(self.tiles>0)

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
                    new_intensity = max(0, intensity - self.costs[neighbour])
                    #test for in-bounds here too
                    if intensity > self.tiles[neighbour] > -1:
                        self.tiles[neighbour] = new_intensity
                        self.neighbours.add(neighbour)
    
    def can_feel(self, start: tuple[int, int]) -> bool:
        return self.tiles[start] > 0
