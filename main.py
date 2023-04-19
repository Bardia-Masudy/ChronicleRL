#!/usr/bin/env python3
import tcod
import traceback

#import objects and classes from outside main.py
import colour
import exceptions
import input_handlers
import setup_game

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine, then save its Engine."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def main()-> None:
    #to be included in a json file later
    screen_width = 80
    screen_height = 50

    #loads charset from file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

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
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit: # Save and exit.
            save_game(handler, "savegame.sav")
        except BaseException: # Save on any other unexpected exception
            save_game(handler, "savegame.sav")


if __name__ == "__main__":
    main()