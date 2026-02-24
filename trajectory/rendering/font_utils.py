import pygame
import os

def get_font(size, bold=False):
    """
    Helper to load bundled fonts with fallback to SysFont.
    """
    font_name = "Inter-Bold.ttf" if bold else "Inter-Regular.ttf"
    path = os.path.join("trajectory", "assets", "fonts", font_name)

    if os.path.exists(path):
        try:
            return pygame.font.Font(path, size)
        except:
            pass

    return pygame.font.SysFont("Arial", size, bold=bold)

def get_mono_font(size):
    path = os.path.join("trajectory", "assets", "fonts", "JetBrainsMono-Regular.ttf")
    if os.path.exists(path):
        try:
            return pygame.font.Font(path, size)
        except:
            pass
    return pygame.font.SysFont("Courier New", size)
