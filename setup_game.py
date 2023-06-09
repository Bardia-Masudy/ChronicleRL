"""Handle mage session loading and initialization."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

import colour
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers

# load the game menu background image and remove its alpha channel.
background_image = tcod.image.load("menu_background.png")[:, :, :3]

def new_game() -> Engine:
    """Return a brand new gamesession as an Engine instance."""
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms = max_rooms,
        room_min_size = room_min_size,
        room_max_size = room_max_size,
        map_width = map_width,
        map_height = map_height
    )

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        """You're finally here, the famed 'Endless Dungeon'!""", colour.welcome_text
    )
    
    return engine

def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as file:
        engine = pickle.loads(lzma.decompress(file.read()))
    assert isinstance(engine, Engine)
    return engine
class MainMenu(input_handlers.BaseEventHandler):
    """Handle main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "ChronicleRL",
            fg=colour.menu_title,
            alignment=tcod.CENTER,
        )

        console.print(
            console.width // 2,
            console.height - 2,
            "By Bardia Masudy",
            fg=colour.menu_title,
            alignment=tcod.CENTER
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N]ew Game", "[C]ontinue", "[Q]uit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=colour.menu_text,
                bg=colour.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64)
            )
        
    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc() #print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())
    
        return None