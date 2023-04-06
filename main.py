#!/usr/bin/env python3
import tcod
import copy

#import objects and classes from outside main.py
from engine import Engine
import entity_factories
from procgen import generate_dungeon

def main()-> None:
    #to be included in a json file later
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 50

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    #loads charset from file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms = max_rooms,
        room_min_size = room_min_size,
        room_max_size = room_max_size,
        map_width = map_width,
        map_height = map_height,
        max_monsters_per_room = max_monsters_per_room,
        engine = engine
    )
    engine.update_fov()

    #creates context for console
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="ChronicleRL",
        vsync=True,
    ) as context:
        # create console, set screen width, reverse coordinates to (x,y)
        root_console = tcod.Console(screen_width, screen_height, order="F")
        
        ## MAIN GAME LOOP
        while True:
            # add entities to console
            engine.render(console=root_console, context=context)

            # handle all events
            engine.event_handler.handle_events()

if __name__ == "__main__":
    main()