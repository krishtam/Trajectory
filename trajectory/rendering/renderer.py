import pygame
from trajectory.rendering.hud import draw_hud
from trajectory.rendering.agent_panel import draw_agent_panel
from trajectory.rendering.font_utils import get_font
from trajectory.core.world_rng import WorldRNG

# Procedural visual imports
from trajectory.rendering.procedural.molecule import draw_molecule_diagram
from trajectory.rendering.procedural.candlestick import draw_candlestick_chart
from trajectory.rendering.procedural.growth_curve import draw_growth_curve

def render_frame(surface: pygame.Surface, game_state, theme: dict,
                 scene_objects, particle_system):

    # Layer 0: Background
    surface.fill(theme["background"])

    # Layer 1: Ambient Particles
    particle_system.update()
    particle_system.draw(surface)

    # Layer 2: Scene Objects (Semi-transparent backing)
    for obj in scene_objects:
        surface.blit(obj.surface, obj.rect)

    # --- DASHBOARD LAYOUT (1280x720) ---
    # Metrics Panel: Left 200px
    # Main Canvas: Center 880px
    # Team Panel: Right 200px

    # Main Dashboard Area (880px)
    dashboard_rect = pygame.Rect(200, 60, 880, 600)
    pygame.draw.rect(surface, (*theme["background"], 180), dashboard_rect)
    pygame.draw.rect(surface, theme["primary"], dashboard_rect, 1)

    # Narrative/Cycle Context
    if hasattr(game_state, 'narrative_text') and game_state.narrative_text:
        draw_narrative_box(surface, game_state.narrative_text, theme)

    # Layer 3: Procedural Main Visual (Immersive center-piece)
    inner_rect = dashboard_rect.inflate(-40, -100)
    rng_display = WorldRNG(game_state.config.seed + 123)

    visual_type = theme.get("procedural_main")
    if visual_type == "molecule_diagram":
        draw_molecule_diagram(surface, rng_display, {"pressure_level": game_state.pressure_level}, theme, inner_rect)
    elif visual_type == "candlestick_chart":
        draw_candlestick_chart(surface, rng_display, {}, theme, inner_rect)
    elif visual_type == "growth_curve":
        draw_growth_curve(surface, rng_display, {}, theme, inner_rect)

    # ECG/Vitals for Surgeon
    if game_state.config.pillar == "Expert":
        draw_vitals_overlay(surface, game_state, theme)
    elif game_state.config.pillar == "Allocator":
        draw_trader_overlays(surface, game_state, theme)

    # Layer 4: Panels
    draw_metrics_panel(surface, game_state, theme)
    draw_agent_panel(surface, game_state.agents, theme)

    # Layer 5: HUD (Top & Bottom)
    draw_hud(surface, game_state, theme)

    # Notifications
    if hasattr(game_state, 'notification') and game_state.notification:
        draw_notification(surface, game_state.notification, theme)

    # Layer 6: Challenge Overlay
    if game_state.active_challenge:
        game_state.active_challenge.draw(surface)

def draw_metrics_panel(surface, state, theme):
    panel_rect = pygame.Rect(0, 60, 200, 600)
    pygame.draw.rect(surface, (15, 20, 30), panel_rect)
    pygame.draw.line(surface, theme["grid"], (200, 60), (200, 660))

    font = get_font(14, bold=True)
    header = font.render("CAREER METRICS", True, theme["accent"])
    surface.blit(header, (100 - header.get_width()//2, 80))

    # Metric 1: Reputation/P&L
    # (Simplified representation for now)
    pygame.draw.rect(surface, (30, 40, 50), (20, 120, 160, 100), border_radius=5)
    m1_label = get_font(12).render("HOSPITAL REPUTATION" if state.config.pillar=="Expert" else "DAY P&L", True, (200,200,200))
    surface.blit(m1_label, (30, 130))

    val = f"{int(state.reputation*100)}%" if state.config.pillar=="Expert" else f"${int(state.metrics['p_and_l']):,}"
    val_surf = get_font(20, bold=True).render(val, True, (255,255,255))
    surface.blit(val_surf, (30, 155))

def draw_narrative_box(surface, text, theme):
    box_rect = pygame.Rect(240, 500, 800, 120)
    pygame.draw.rect(surface, (5, 10, 20, 230), box_rect, border_radius=10)
    pygame.draw.rect(surface, theme["primary"], box_rect, 2, border_radius=10)

    font = get_font(18)
    # Simple word wrap
    words = text.split(' ')
    lines = []
    current_line = ""
    for w in words:
        if font.size(current_line + w)[0] < 740:
            current_line += w + " "
        else:
            lines.append(current_line)
            current_line = w + " "
    lines.append(current_line)

    for i, line in enumerate(lines[:3]):
        txt_surf = font.render(line, True, (255, 255, 255))
        surface.blit(txt_surf, (270, 520 + i * 25))

def draw_vitals_overlay(surface, state, theme):
    font = get_font(16, bold=True)
    vitals = [
        ("HEART RATE", "142 bpm", (255, 100, 100)),
        ("BLOOD PRESSURE", "95/60", (255, 200, 50)),
        ("O2 SAT", "94%", (255, 200, 50))
    ]
    for i, (label, val, col) in enumerate(vitals):
        l_surf = get_font(10).render(label, True, (200, 200, 200))
        v_surf = font.render(val, True, col)
        surface.blit(l_surf, (900, 100 + i * 50))
        surface.blit(v_surf, (900, 115 + i * 50))

def draw_notification(surface, text, theme):
    font = get_font(18, bold=True)
    text_surf = font.render(text, True, (255, 255, 255))
    rect = text_surf.get_rect(center=(640, 40))
    bg_rect = rect.inflate(40, 15)
    pygame.draw.rect(surface, (200, 0, 0), bg_rect, border_radius=5)
    surface.blit(text_surf, rect)

def draw_trader_overlays(surface, state, theme):
    # 1. Ticker Tape
    ticker_rect = pygame.Rect(200, 610, 880, 50)
    pygame.draw.rect(surface, (5, 10, 15), ticker_rect)
    pygame.draw.line(surface, theme["primary"], (200, 610), (1080, 610))

    font = get_font(12, bold=True)
    offset = (pygame.time.get_ticks() // 20) % 1000
    ticker_text = "AAPL +1.2%   TSLA -0.8%   GOOGL +0.5%   BTC/USD +2.1%   SPY +0.3%   NVDA +4.5%   AMZN -0.2%   META +1.1%   "
    txt_surf = font.render(ticker_text + ticker_text, True, theme["accent"])
    surface.blit(txt_surf, (1080 - offset, 625))

    # 2. News Feed (Small panel)
    news_rect = pygame.Rect(800, 450, 260, 150)
    pygame.draw.rect(surface, (15, 20, 35, 200), news_rect, border_radius=10)
    pygame.draw.rect(surface, theme["primary"], news_rect, 1, border_radius=10)

    header = get_font(10, bold=True).render("REAL-TIME NEWS FEED", True, theme["accent"])
    surface.blit(header, (810, 460))

    # Just a sample headline
    headline = "FED HINTS AT HAWKISH STANCE" if state.pressure_level > 0.6 else "MARKETS STEADY AFTER OPEN"
    h_surf = get_font(12).render(headline, True, (255, 255, 255))
    surface.blit(h_surf, (810, 485))
