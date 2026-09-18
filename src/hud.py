"""HUD: chores panel + pooled progress bar.

Placeholder look for now. Real parchment UI comes in the art pass.
"""

import pygame
from src import settings as S
from src.chores import ChoreLog, POOL_THRESHOLD

PANEL_W = 300
PANEL_MARGIN = 16
ROW_H = 44


def draw_chore_panel(surface: pygame.Surface, log: ChoreLog,
                     font_title: pygame.font.Font,
                     font_row: pygame.font.Font) -> None:
    sw = surface.get_width()
    panel_x = sw - PANEL_W - PANEL_MARGIN
    panel_y = PANEL_MARGIN
    panel_h = surface.get_height() - PANEL_MARGIN * 2

    # panel background
    panel = pygame.Rect(panel_x, panel_y, PANEL_W, panel_h)
    pygame.draw.rect(surface, S.PARCHMENT, panel, border_radius=10)
    pygame.draw.rect(surface, S.INK, panel, width=2, border_radius=10)

    # title
    title = font_title.render("Today's chores", True, S.INK)
    surface.blit(title, (panel_x + 16, panel_y + 14))

    # pool bar
    bar_x = panel_x + 16
    bar_y = panel_y + 52
    bar_w = PANEL_W - 32
    bar_h = 14
    pygame.draw.rect(surface, S.PARCHMENT_DARK,
                     (bar_x, bar_y, bar_w, bar_h), border_radius=7)
    filled = int(bar_w * min(log.pool, POOL_THRESHOLD) / POOL_THRESHOLD)
    pygame.draw.rect(surface, S.GOLD,
                     (bar_x, bar_y, filled, bar_h), border_radius=7)
    pygame.draw.rect(surface, S.INK,
                     (bar_x, bar_y, bar_w, bar_h), width=2, border_radius=7)

    # chore rows
    y = bar_y + bar_h + 20
    for category, chores in log.grouped().items():
        cat_label = font_row.render(category.upper(), True, S.WOOD_DARK)
        surface.blit(cat_label, (panel_x + 16, y))
        y += 22

        for c in chores:
            _draw_chore_row(surface, panel_x, y, c, font_row)
            y += ROW_H

        y += 8


def _draw_chore_row(surface: pygame.Surface, panel_x: int, y: int,
                    chore, font: pygame.font.Font) -> None:
    box = pygame.Rect(panel_x + 16, y, 22, 22)
    pygame.draw.rect(surface, S.WHITE, box, border_radius=4)
    pygame.draw.rect(surface, S.INK, box, width=2, border_radius=4)

    if chore.done:
        # checkmark
        pygame.draw.line(surface, S.GRASS_DARK,
                         (box.x + 5, box.y + 11),
                         (box.x + 9, box.y + 16), 3)
        pygame.draw.line(surface, S.GRASS_DARK,
                         (box.x + 9, box.y + 16),
                         (box.x + 17, box.y + 5), 3)

    label_color = S.STONE_DARK if chore.done else S.INK
    text = font.render(chore.label, True, label_color)
    surface.blit(text, (box.right + 10, box.y + 1))


def chore_row_rects(surface: pygame.Surface, log: ChoreLog) -> list[tuple]:
    """Return (chore_id, rect) for hit-testing clicks.

    Mirrors the layout in draw_chore_panel. Keep them in sync.
    """
    sw = surface.get_width()
    panel_x = sw - PANEL_W - PANEL_MARGIN
    panel_y = PANEL_MARGIN

    bar_y = panel_y + 52
    y = bar_y + 14 + 20

    out: list[tuple] = []
    for category, chores in log.grouped().items():
        y += 22
        for c in chores:
            rect = pygame.Rect(panel_x + 16, y, PANEL_W - 32, 30)
            out.append((c.id, rect))
            y += ROW_H
        y += 8
    return out
