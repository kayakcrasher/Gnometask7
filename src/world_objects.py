"""World objects: trees, stumps, buildings.

These sit on top of the tile map. Each has a world position and can be
drawn, interacted with, and (for resources) harvested.
"""

import pygame
from src import settings as S


class WorldObject:
    """Base for anything placed in the world that isn't terrain."""

    def __init__(self, x: int, y: int):
        self.x = x            # world pixel coords (base / trunk)
        self.y = y
        self.solid = True     # blocks walking

    def draw(self, surface: pygame.Surface, cam_x: int, cam_y: int) -> None:
        raise NotImplementedError

    def distance_to(self, px: float, py: float) -> float:
        dx = self.x - px
        dy = self.y - py
        return (dx * dx + dy * dy) ** 0.5


class OakTree(WorldObject):
    """A choppable oak. Placeholder art: brown trunk + green canopy.

    Art pass later: layered canopy, outline, texture, falling leaves.
    """

    MAX_HP = 3   # chops to fell

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.hp = self.MAX_HP
        self.stump = False

    def chop(self) -> bool:
        """Return True if the tree was felled by this chop."""
        if self.stump:
            return False
        self.hp -= 1
        if self.hp <= 0:
            self.stump = True
            return True
        return False

    def draw(self, surface: pygame.Surface, cam_x: int, cam_y: int) -> None:
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)

        if self.stump:
            # stump: low brown circle with lighter top
            pygame.draw.ellipse(surface, S.WOOD_DARK, (sx - 12, sy - 8, 24, 16))
            pygame.draw.ellipse(surface, S.WOOD_LIGHT, (sx - 12, sy - 12, 24, 12))
            return

        # shadow
        shadow = pygame.Surface((52, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), shadow.get_rect())
        surface.blit(shadow, (sx - 26, sy - 4))

        # trunk
        pygame.draw.rect(surface, S.WOOD_DARK, (sx - 6, sy - 30, 12, 30))
        pygame.draw.rect(surface, S.WOOD_MID, (sx - 6, sy - 30, 5, 30))

        # canopy (three overlapping circles for depth)
        pygame.draw.circle(surface, S.GRASS_DARK, (sx, sy - 52), 26)
        pygame.draw.circle(surface, S.GRASS_MID, (sx - 4, sy - 56), 22)
        pygame.draw.circle(surface, S.GRASS_LIGHT, (sx + 3, sy - 60), 16)

    def label(self) -> str:
        return "Oak tree" if not self.stump else "Stump"


def scatter_oak_trees(tilemap, count: int = 40) -> list[OakTree]:
    """Place oak trees on grass tiles, avoiding the dirt path and water.

    Deterministic-ish for now (simple pseudo-random walk). Real scatter
    comes when we add worldgen.
    """
    import random
    rng = random.Random(42)   # fixed seed = same world every run
    ts = S.TILE_SIZE
    trees: list[OakTree] = []

    # tile type ids mirror tilemap.py
    GRASS, DIRT, WATER = 0, 1, 2

    attempts = 0
    while len(trees) < count and attempts < count * 20:
        attempts += 1
        tx = rng.randint(2, tilemap.width - 3)
        ty = rng.randint(2, tilemap.height - 3)
        if tilemap.tiles[ty][tx] != GRASS:
            continue

        # don't crowd: skip if another tree is close
        wx = tx * ts + ts // 2
        wy = ty * ts + ts // 2
        if any(abs(t.x - wx) < ts * 2 and abs(t.y - wy) < ts * 2 for t in trees):
            continue

        trees.append(OakTree(wx, wy))

    return trees
