from __future__ import annotations

from typing import Optional, TYPE_CHECKING
import random


import numpy as np
import tcod

from actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction

if TYPE_CHECKING:
    from entity import Actor

class BaseAI(Action):
    
    def perform(self) -> None:
        raise NotImplementedError()
    
    def get_path_to(self, dest_x: int, dest_y: int) -> list[tuple[int, int]]:
        """Compute and get path to a target coordinate.
        If no valid path, return an empty list.
        """
        # Copy the walkable array
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an entity blocks movement and the cost isn't zero (blocking).
            # A lower number means more enemies will crowd behind eachother in
            # hallways. A higher number means enemies will take longer paths in
            # order to surround the player.
            cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y)) # Start position

        # Compute the path to the destination and remove the starting point.
        path: list[list[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]] for coordinate map of path.
        return [(index[0], index[1]) for index in path]

class ConfusedEnemy(BaseAI):
    """
    A confused enemy will stumble aroundaimlessly for a given umberof turns, then revert back to their previous AI.
    If an actor occupies a tile it is randmly moving into, it will attack.
    """

    def __init__(self, entity: Actor, previous_ai: Optional[BaseAI], duration: int) -> None:
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.duration = duration

    def perform(self) -> None:
        # Revert the AI back to the original state if the effect has run out of turns.
        if self.duration <= 0:
            self.engine.message_log.add_message(f"The {self.entity.name} is no longer confused.")
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )

            self.duration -= 1

            # The actor will either try to move or attack in the chosen random direction.
            # Its possible the actor will just bump into the wall, wasting a turn.
            return BumpAction(self.entity, direction_x, direction_y,).perform()
class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: list[tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy)) # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()
            
            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y
            ).perform()
        
        return WaitAction(self.entity).perform()
