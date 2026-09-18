"""Global settings: screen, colors, tile size, FPS.

Every magic number lives here so we change it in one place.
"""

# --- display ---
SCREEN_W = 1280
SCREEN_H = 720
FPS = 60
CAPTION = "Gnome Tasks"

# --- world ---
TILE_SIZE = 32          # pixels per tile
MAP_W = 100             # tiles wide
MAP_H = 100             # tiles tall

# --- palette (from docs/ART.md) ---
# warm wood
WOOD_DARK = (107, 68, 35)
WOOD_MID = (139, 90, 43)
WOOD_LIGHT = (168, 118, 70)

# grass
GRASS_LIGHT = (124, 179, 66)
GRASS_MID = (85, 139, 47)
GRASS_DARK = (61, 107, 46)

# stone
STONE_LIGHT = (168, 162, 158)
STONE_DARK = (120, 113, 108)

# parchment / UI
PARCHMENT = (245, 230, 200)
PARCHMENT_DARK = (232, 213, 168)
INK = (58, 42, 26)
GOLD = (212, 160, 23)

# water
WATER_LIGHT = (107, 163, 184)
WATER_DARK = (74, 127, 150)
WATER_MID = (90, 145, 167)

# path
DIRT = (201, 168, 118)

# misc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
