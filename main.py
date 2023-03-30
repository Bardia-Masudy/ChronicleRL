#!/usr/bin/env python3
import tcod

#import Action subobjects from actions and EventHandler from input_handler
from actions import EscapeAction, MovementAction
from input_handlers import EventHandler

def main()-> None:
    #to be included in a json file later
    screen_width = 80
    screen_height = 50

    #handles player location for root console
    player_x = int(screen_width/2)
    player_y = int(screen_height/2)

    #loads charset from file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    #create instance of EventHandler class to receive and process events
    event_handler = EventHandler()

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
            #add player to console
            root_console.print(x=player_x, y=player_y, string="@")

            #print to screen
            context.present(root_console)

            #refresh console
            root_console.clear()

            for event in tcod.event.wait():
                #send event to event_handler's dispatch method, store keydown as action
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                #movement handling 
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                #exit on Esc key down
                elif isinstance(action, EscapeAction):
                    raise SystemExit()

if __name__ == "__main__":
    main()