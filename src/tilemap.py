"""Tile map: a grid of terrain types, drawn to the screen.

For now: flat grass with a dirt path and a water border.
Later: real island generation, trees, buildings.
"""

import pygame
from src import settings as S

# tile type ids
GRASS = 0
DIRT = 1
WATER = 2


class TileMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = [[GRASS for _ in range(width)] for _ in range(height)]
        self._generate()

    def _generate(self) -> None:
        """Placeholder world: water border, dirt path across the middle."""
        # water border
        for x in range(self.width):
            self.tiles[0][x] = WATER
            self.tiles[self.height - 1][x] = WATER
        for y in range(self.height):
            self.tiles[y][0] = WATER
            self.tiles[y][self.width - 1] = WATER

        # a dirt path down the middle
        mid = self.width // 2
        for y in range(1, self.height - 1):
            self.tiles[y][mid] = DIRT
            self.tiles[y][mid + 1] = DIRT

    def draw(self, surface: pygame.Surface, cam_x: int, cam_y: int) -> None:
        """Draw only the tiles visible on screen."""
        ts = S.TILE_SIZE
        start_x = max(0, cam_x // ts)
        start_y = max(0, cam_y // ts)
        end_x = min(self.width, (cam_x + surface.get_width()) // ts + 1)
        end_y = min(self.height, (cam_y + surface.get_height()) // ts + 1)

        for ty in range(start_y, end_y):
            for tx in range(start_x, end_x):
                color = self._color_for(self.tiles[ty][tx])
                rect = pygame.Rect(
                    tx * ts - cam_x,
                    ty * ts - cam_y,
                    ts,
                    ts,
                )
                pygame.draw.rect(surface, color, rect)

    @staticmethod
    def _color_for(tile: int) -> tuple[int, int, int]:
        if tile == GRASS:
            return S.GRASS_MID
        if tile == DIRT:
            return S.DIRT
        if tile == WATER:
            return S.WATER_MID if hasattr(S, "WATER_MID") else S.WATER_DARK
        return S.GRASS_MID
