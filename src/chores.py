"""Chores: the daily habit checklist.

Each chore is a real-life task (brush teeth, walk, etc). Completing
chores fills a pooled progress bar; when the bar fills, something
grows in the world (a tree, a bloom, etc).

For now: data + logic only, no UI.
"""

from dataclasses import dataclass, field


@dataclass
class Chore:
    id: str
    label: str
    category: str          # e.g. "cottage", "garden", "village"
    done: bool = False
    points: int = 1        # how much it contributes to the pool


# Default starter chores. Categories group them in the UI.
DEFAULT_CHORES: list[Chore] = [
    Chore("bed",      "Get out of bed",       "cottage"),
    Chore("teeth",    "Brush your teeth",     "cottage"),
    Chore("make_bed", "Make the bed",         "cottage"),
    Chore("breakfast","Have a little breakfast","cottage"),
    Chore("garden",   "Water the garden",     "garden"),
    Chore("walk",     "Walk the village path","village"),
]

# How many pooled points are needed to plant one thing.
POOL_THRESHOLD = 5


@dataclass
class ChoreLog:
    chores: list[Chore] = field(default_factory=lambda: list(DEFAULT_CHORES))
    pool: int = 0                  # current pooled points
    total_completed: int = 0       # lifetime count

    def complete(self, chore_id: str) -> bool:
        """Mark a chore done. Returns True if it actually changed."""
        for c in self.chores:
            if c.id == chore_id and not c.done:
                c.done = True
                self.pool += c.points
                self.total_completed += 1
                return True
        return False

    def undo(self, chore_id: str) -> bool:
        """Un-mark a chore (in case of misclick)."""
        for c in self.chores:
            if c.id == chore_id and c.done:
                c.done = False
                self.pool -= c.points
                self.total_completed -= 1
                return True
        return False

    def ready_to_plant(self) -> bool:
        return self.pool >= POOL_THRESHOLD

    def consume_pool(self) -> None:
        """Spend a full pool (call this when planting)."""
        if self.ready_to_plant():
            self.pool -= POOL_THRESHOLD

    def reset_daily(self) -> None:
        """Reset for a new day. Pool persists; chores uncheck."""
        for c in self.chores:
            c.done = False

    def grouped(self) -> dict[str, list[Chore]]:
        """Return chores grouped by category, for the UI."""
        out: dict[str, list[Chore]] = {}
        for c in self.chores:
            out.setdefault(c.category, []).append(c)
        return out
