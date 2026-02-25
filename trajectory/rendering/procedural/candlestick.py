import pygame
from trajectory.rendering.procedural.chart_utils import generate_chart_surface
from trajectory.rendering.font_utils import get_font

def draw_candlestick_chart(surface: pygame.Surface, rng_display,
                           world_data: dict, theme: dict, rect: pygame.Rect):
    """
    Renders a live market dashboard with candlestick charts and order book.
    """
    # 1. Main Candlestick Chart (Top half)
    chart_rect = pygame.Rect(rect.left, rect.top, rect.width, rect.height // 2)

    # Generate some fake candlestick data seeded
    data = []
    current_price = 100.0 + rng_display.uniform(-10, 10)
    for _ in range(30):
        o = current_price
        c = o + rng_display.uniform(-4, 4)
        h = max(o, c) + rng_display.uniform(0, 2)
        l = min(o, c) - rng_display.uniform(0, 2)
        data.append((o, h, l, c))
        current_price = c

    chart_surf = generate_chart_surface(data, theme, chart_type="candlestick", size_px=chart_rect.size)
    surface.blit(chart_surf, chart_rect.topleft)

    # 2. Market Depth / Order Book (Bottom half)
    depth_rect = pygame.Rect(rect.left, rect.top + rect.height // 2 + 20, rect.width, rect.height // 2 - 20)
    pygame.draw.rect(surface, (10, 15, 25), depth_rect)
    pygame.draw.rect(surface, theme["primary"], depth_rect, 1)

    font = get_font(12, bold=True)
    header = font.render("LIVE ORDER BOOK (BID / ASK)", True, theme["accent"])
    surface.blit(header, (depth_rect.centerx - header.get_width()//2, depth_rect.top + 10))

    # Draw simulated bids/asks
    for i in range(5):
        y = depth_rect.top + 40 + i * 25
        # Bid (Left)
        bid_w = rng_display.integers(50, 150)
        pygame.draw.rect(surface, (0, 100, 0), (depth_rect.centerx - 10 - bid_w, y, bid_w, 20))
        # Ask (Right)
        ask_w = rng_display.integers(50, 150)
        pygame.draw.rect(surface, (100, 0, 0), (depth_rect.centerx + 10, y, ask_w, 20))
