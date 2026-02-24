import pygame
from trajectory.rendering.procedural.chart_utils import generate_chart_surface

def draw_growth_curve(surface: pygame.Surface, rng_display,
                      world_data: dict, theme: dict, rect: pygame.Rect):
    """
    Draws a procedural growth curve for Builder/Entrepreneur.
    """
    # Generate exponential-ish growth data
    data = []
    val = 1.0
    for i in range(20):
        val *= rng_display.uniform(1.0, 1.3)
        data.append(val)

    chart_surf = generate_chart_surface(data, theme, chart_type="line", size_px=rect.size)
    surface.blit(chart_surf, rect.topleft)
