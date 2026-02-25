import pygame
import os
import sys

# Add root to path
sys.path.append(os.getcwd())

from trajectory.rendering.procedural.molecule import draw_molecule_diagram
from trajectory.rendering.procedural.candlestick import draw_candlestick_chart
from trajectory.core.world_rng import WorldRNG

def generate_samples():
    pygame.init()
    surface = pygame.Surface((800, 400))

    theme = {
        "background": (10, 18, 30),
        "primary": (41, 182, 246),
        "accent": (129, 212, 250),
        "grid": (25, 45, 65)
    }

    os.makedirs("docs/samples", exist_ok=True)

    # 1. Molecule Sample
    surface.fill(theme["background"])
    rng = WorldRNG(4821)
    rect = pygame.Rect(0, 0, 800, 400)
    draw_molecule_diagram(surface, rng, {}, theme, rect)
    pygame.image.save(surface, "docs/samples/molecule_sample.png")
    print("Saved molecule_sample.png")

    # 2. Candlestick Sample
    surface.fill(theme["background"])
    rng = WorldRNG(58821)
    draw_candlestick_chart(surface, rng, {}, theme, rect)
    pygame.image.save(surface, "docs/samples/candlestick_sample.png")
    print("Saved candlestick_sample.png")

    pygame.quit()

if __name__ == "__main__":
    generate_samples()
