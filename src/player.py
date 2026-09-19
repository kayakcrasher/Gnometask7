"""Player: the gnome. Moves toward a clicked world position."""

import math
import pygame
from src import settings as S


class Player:
    def __init__(self, x: int, y: int):
        self.x = float(x)          # world pixel coords (center)
        self.y = float(y)
        self.speed = 180.0         # pixels per second
        self.target_x: float | None = None
        self.target_y: float | None = None
        self.radius = 10

    def move_to(self, wx: int, wy: int) -> None:
        """Set a destination in world pixel coords."""
        self.target_x = float(wx)
        self.target_y = float(wy)

    def update(self, dt: float) -> None:
        """Step toward the target. Stop when close enough."""
        if self.target_x is None or self.target_y is None:
            return

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)

        step = self.speed * dt

        # arrive if we're within one step of the target
        if dist <= step:
            self.x = self.target_x
            self.y = self.target_y
            self.target_x = None
            self.target_y = None
            return

        self.x += (dx / dist) * step
        self.y += (dy / dist) * step

    def draw(self, surface: pygame.Surface, cam_x: int, cam_y: int) -> None:
        """Placeholder gnome: shadow + body + red cap."""
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)

        # shadow
        shadow = pygame.Surface((28, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 70), shadow.get_rect())
        surface.blit(shadow, (sx - 14, sy + 6))

        # body (green tunic)
        pygame.draw.circle(surface, (74, 103, 65), (sx, sy), self.radius)

        # head
        pygame.draw.circle(surface, (240, 220, 190), (sx, sy - 8), 7)

        # red cap
        pygame.draw.polygon(
            surface,
            (170, 50, 45),
            [(sx - 8, sy - 10), (sx + 8, sy - 10), (sx, sy - 22)],
        )
