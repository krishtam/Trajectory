import pygame
import os

class AssetLoader:
    def __init__(self, base_path: str = "trajectory/assets"):
        self.base_path = base_path
        self.cache = {}

    def get_asset(self, category: str, name: str) -> pygame.Surface:
        """
        Retrieves an asset from assets/{category}/{name}.png
        """
        path = os.path.join(self.base_path, category, f"{name}.png")
        if path in self.cache:
            return self.cache[path]

        if not os.path.exists(path):
            # Fallback to a placeholder surface
            surf = pygame.Surface((128, 128), pygame.SRCALPHA)
            pygame.draw.rect(surf, (150, 150, 150), (0, 0, 128, 128), 2)
            return surf

        surf = pygame.image.load(path).convert_alpha()
        self.cache[path] = surf
        return surf

    def load_object(self, pillar: str, obj_name: str, color: tuple = None) -> pygame.Surface:
        # Map pillar to directory
        dir_map = {
            "Expert": "expert",
            "Allocator": "allocator",
            "Builder": "builder"
        }
        category = os.path.join("objects", dir_map.get(pillar, "expert"))
        return self.get_asset(category, obj_name)
