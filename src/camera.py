"""Camera: tracks a target and converts world <-> screen coords."""

from src import settings as S


class Camera:
    def __init__(self, map_w_px: int, map_h_px: int):
        self.x = 0
        self.y = 0
        self.map_w_px = map_w_px
        self.map_h_px = map_h_px

    def follow(self, target_x: int, target_y: int,
               screen_w: int, screen_h: int) -> None:
        """Center the camera on the target, clamped to map bounds."""
        self.x = target_x - screen_w // 2
        self.y = target_y - screen_h // 2

        self.x = max(0, min(self.x, self.map_w_px - screen_w))
        self.y = max(0, min(self.y, self.map_h_px - screen_h))

    def world_to_screen(self, wx: int, wy: int) -> tuple[int, int]:
        return wx - self.x, wy - self.y
