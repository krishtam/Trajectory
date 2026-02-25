import pygame
from trajectory.core.world_rng import WorldRNG

class SceneObject:
    def __init__(self, surface, rect, alpha):
        self.surface = surface
        self.rect = rect
        self.alpha = alpha

def place_scene_objects(config, theme, asset_loader):
    rng = WorldRNG(config.seed + 999) # Different seed for placement
    objects = []

    available_objects = theme.get("scene_objects", [])
    if not available_objects:
        return []

    n = len(available_objects)
    for obj_name in available_objects:
        surf = asset_loader.load_object(config.pillar, obj_name, color=theme["primary"])

        # Random position in main canvas (240, 48) to (1280, 656)
        x = rng.integers(300, 1100)
        y = rng.integers(100, 550)
        scale = rng.uniform(0.5, 1.2)
        alpha = rng.integers(50, 150)

        scaled_surf = pygame.transform.rotozoom(surf, 0, scale)
        scaled_surf.set_alpha(alpha)
        rect = scaled_surf.get_rect(center=(x, y))

        objects.append(SceneObject(scaled_surf, rect, alpha))

    return objects
