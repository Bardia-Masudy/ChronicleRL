import numpy as np

# Tile graphics structure type compatible with Console.tiles_rgb
graphic_dt = np.dtype(
    [
        ("ch", np.int32),   # Unicode codepoint
        ("fg", "3B"),       # 3 unsigned bytes for RGB colour
        ("bg", "3B")        # as fg
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", bool),      # True if tile can be walked over
        ("transparent", bool),   # True is this tile can be seen through
        ("dark", graphic_dt),    # Graphics for when out of sight/remembered
        ("light", graphic_dt)    # Graphics for when in FOV
    ]
)

def new_tile(
    *, #Enforce use of keywords
    walkable: int,
    transparent: int,
    dark: tuple[int, tuple[int, int, int], tuple[int, int, int]],
    light: tuple[int, tuple[int, int, int], tuple[int, int, int]]
) -> np.ndarray:
    """Helper function for defining individual tile types."""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

# Tile types
floor = new_tile(
    walkable=True, 
    transparent=True, 
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50))
)

wall = new_tile(
    walkable=False, 
    transparent=False, 
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50))
)