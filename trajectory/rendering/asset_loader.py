import pygame
import numpy as np
import os
from PIL import Image

def colorize_asset(surface: pygame.Surface, target_color: tuple) -> pygame.Surface:
    """
    Recolors a grayscale RGBA surface to target_color while preserving alpha.
    """
    result = surface.copy().convert_alpha()
    r, g, b = target_color[:3]

    # Pixel-level colorize: multiply luminance by target color
    arr = pygame.surfarray.pixels3d(result)
    # luminance calculation
    luminance = arr.mean(axis=2, keepdims=True) / 255.0
    arr[:,:,0] = (luminance[:,:,0] * r).astype(np.uint8)
    arr[:,:,1] = (luminance[:,:,0] * g).astype(np.uint8)
    arr[:,:,2] = (luminance[:,:,0] * b).astype(np.uint8)

    return result

class AssetLoader:
    def __init__(self, base_path: str = "trajectory/assets"):
        self.base_path = base_path
        self.cache = {}

    def load_icon(self, career: str, color: tuple = None) -> pygame.Surface:
        path = os.path.join(self.base_path, "icons", f"{career.lower()}.png")
        return self._load_and_colorize(path, color)

    def load_object(self, pillar: str, obj_name: str, color: tuple = None) -> pygame.Surface:
        path = os.path.join(self.base_path, "objects", pillar.lower(), f"{obj_name}.png")
        return self._load_and_colorize(path, color)

    def _load_and_colorize(self, path: str, color: tuple) -> pygame.Surface:
        cache_key = (path, color)
        if cache_key in self.cache:
            return self.cache[cache_key]

        if not os.path.exists(path):
            # Return placeholder
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.rect(surf, (200, 200, 200), (0, 0, 64, 64), 2)
            return surf

        surf = pygame.image.load(path).convert_alpha()
        if color:
            surf = colorize_asset(surf, color)

        self.cache[cache_key] = surf
        return surf
