from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
import render_functions as rend
from message_log import MessageLog

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld

## Engine responsible for drawing map and entities, as well as handling player input.
class Engine:
    gamemap: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_xy = (0, 0)
        self.player = player
    
    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass # Ignore impossible actions

    def update_fov(self) -> None:
        """Recompute visible area based around player POV."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8 # Space to use different algorithm, maybe FOV_DIAMOND or FOV_SHADOW?
        )
        # If a tile is visible, it should be added to "explored"
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        rend.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            max_value=self.player.fighter.max_hp,
            total_width=20
        )

        rend.render_dungeon_level(
            console=console,
            dungeon_level= self.game_world.current_floor,
            location=(0, 47)
        )

        rend.render_names_at_mouse_location(
            console=console, 
            x=21, 
            y=44, 
            engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine object as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as file:
            file.write(save_data)