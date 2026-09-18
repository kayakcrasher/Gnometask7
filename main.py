"""Gnome Tasks - entry point.

Opens a window, runs the game loop, exits cleanly.
Nothing else yet - this proves the toolchain works.
"""

import sys
import pygame

# --- constants (will move to settings.py next) ---
SCREEN_W, SCREEN_H = 1280, 720
FPS = 60
BG_COLOR = (74, 103, 65)  # muted rustic green
CAPTION = "Gnome Tasks"


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(BG_COLOR)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
