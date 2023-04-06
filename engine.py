from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap

## Engine responsible for drawing map and entities, as well as handling player input.
class Engine:
    gamemap: GameMap

    def __init__(self, player: Entity):
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player
    
    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()
            #print(f"The {entity.name} wonders when it'll get a turn.")

    def update_fov(self) -> None:
        """Recompute visible area based around player POV."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8 # Space to use different algorithm, maybe FOV_DIAMOND or FOV_SHADOW?
        )
        # If a tile is visible, it should be added to "explored"
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        context.present(console)

        console.clear()