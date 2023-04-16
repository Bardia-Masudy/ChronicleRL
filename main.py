#!/usr/bin/env python3
import tcod
import copy
import traceback

#import objects and classes from outside main.py
import colour
from engine import Engine
import entity_factories
import exceptions
import input_handlers
from procgen import generate_dungeon, generate_sound_map

def main()-> None:
    #to be included in a json file later
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2
    max_items_per_room = 2

    #loads charset from file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.message_log.add_message(
        "Drawn by its mysteries, you enter Zerksoth's Tomb. The doors slam shut behind you.", colour.welcome_text
    )

    engine.game_map = generate_dungeon(
        max_rooms = max_rooms,
        room_min_size = room_min_size,
        room_max_size = room_max_size,
        map_width = map_width,
        map_height = map_height,
        max_monsters_per_room = max_monsters_per_room,
        max_items_per_room = max_items_per_room,
        engine = engine
    )

    engine.sound_map = generate_sound_map(
        array= engine.game_map.tiles, 
        engine= engine
    )

    engine.update_fov()

    handler: input_handlers.BaseEventHandler = input_handlers.MainGameEventHandler(engine)

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
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception: # Handle exceptions in game
                    traceback.print_exc() #print error to stderr
                    # Then print error to message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), colour.error
                        )
                    engine.message_log.add_message(
                        traceback.format_exc(), colour.error
                    )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit: # Save and exit.
            raise # TODO: save function here
        except BaseException: # Save on any other unexpected exception
            raise # TODO: save function here


if __name__ == "__main__":
    main()