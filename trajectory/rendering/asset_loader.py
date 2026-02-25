import pygame
import os
from trajectory.rendering.programmatic_assets import ProgrammaticAssets

class AssetLoader:
    def __init__(self, base_path: str = "trajectory/assets"):
        self.base_path = base_path
        self.cache = {}

    def get_asset(self, category: str, name: str) -> pygame.Surface:
        """
        Overhauled: Uses ProgrammaticAssets instead of loading PNGs.
        """
        # We ignore category for now and use the name to look up drawing functions.
        # This aligns with the "ditch PNG pipeline" requirement.

        cache_key = (name)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Determine size based on name hints or default
        size = (256, 256)
        if "icon" in name or "portrait" in name:
            size = (128, 128)

        surf = ProgrammaticAssets.get_surface(name, size=size)
        self.cache[cache_key] = surf
        return surf

    def load_object(self, pillar: str, obj_name: str, color: tuple = None) -> pygame.Surface:
        return self.get_asset("objects", obj_name)
