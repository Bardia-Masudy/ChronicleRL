from entity import Entity

# entity = Entity(char="CHAR", colour=(R, G, B), name="STRING", blocks_movement=bool)

player = Entity(char="@", colour=(255, 255, 255), name="Player", blocks_movement=True)

orc = Entity(char="O", colour=(63, 127, 63), name="Orc", blocks_movement=True)
goblin = Entity(char="g", colour=(0, 127, 0), name="Goblin", blocks_movement=True)