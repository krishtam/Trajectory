import pygame
from trajectory.rendering.procedural.chart_utils import generate_chart_surface

def draw_audience_curve(surface: pygame.Surface, rng_display,
                        world_data: dict, theme: dict, rect: pygame.Rect):
    """
    Draws a procedural audience growth curve for Creator/Designer.
    """
    data = [10, 15, 12, 20, 25, 22, 35, 50, 45, 60, 80, 75, 100, 130]
    # Add some noise
    data = [d + rng_display.uniform(-5, 5) for d in data]

    chart_surf = generate_chart_surface(data, theme, chart_type="line", size_px=rect.size)
    surface.blit(chart_surf, rect.topleft)
