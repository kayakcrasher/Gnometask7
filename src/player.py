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
