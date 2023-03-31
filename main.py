#!/usr/bin/env python3
import tcod

#import objects and classes from outside main.py
from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

def main()-> None:
    #to be included in a json file later
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 50

    #loads charset from file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    #create instance of EventHandler class to receive and process events
    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "g", (255, 255, 0))
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map = game_map, player=player)

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
            #add entities to console
            engine.render(console=root_console, context=context)

            #get all events
            events = tcod.event.wait()

            #handle events
            engine.handle_events(events)

if __name__ == "__main__":
    main()