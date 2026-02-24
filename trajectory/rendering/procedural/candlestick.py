import pygame
from trajectory.rendering.procedural.chart_utils import generate_chart_surface

def draw_candlestick_chart(surface: pygame.Surface, rng_display,
                           world_data: dict, theme: dict, rect: pygame.Rect):
    """
    Draws a procedural candlestick chart for Allocator/Trader.
    """
    # Generate some fake candlestick data
    data = []
    current_price = 100.0
    for _ in range(20):
        o = current_price
        c = o + rng_display.uniform(-5, 5)
        h = max(o, c) + rng_display.uniform(0, 3)
        l = min(o, c) - rng_display.uniform(0, 3)
        data.append((o, h, l, c))
        current_price = c

    chart_surf = generate_chart_surface(data, theme, chart_type="candlestick", size_px=rect.size)
    surface.blit(chart_surf, rect.topleft)
