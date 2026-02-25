import pygame
from trajectory.rendering.hud import draw_hud
from trajectory.rendering.agent_panel import draw_agent_panel
from trajectory.rendering.procedural.molecule import draw_molecule_diagram
from trajectory.rendering.procedural.candlestick import draw_candlestick_chart
from trajectory.rendering.procedural.growth_curve import draw_growth_curve
from trajectory.rendering.procedural.org_chart import draw_org_chart
from trajectory.rendering.procedural.network_graph import draw_network_graph
from trajectory.rendering.procedural.audience_curve import draw_audience_curve
from trajectory.core.world_rng import WorldRNG
from trajectory.rendering.font_utils import get_font

def render_frame(surface: pygame.Surface, game_state, theme: dict,
                 scene_objects, particle_system):

    # Layer 0: Background
    surface.fill(theme["background"])

    # Draw a subtle grid
    grid_color = theme["grid"]
    for x in range(0, 1280, 40):
        pygame.draw.line(surface, grid_color, (x, 0), (x, 720), 1)
    for y in range(0, 720, 40):
        pygame.draw.line(surface, grid_color, (0, y), (1280, y), 1)

    # Layer 1: Particles
    particle_system.update()
    particle_system.draw(surface)

    # Layer 2: Scene Objects (Backing visuals)
    for obj in scene_objects:
        surface.blit(obj.surface, obj.rect)

    # Main Dashboard Area
    dashboard_rect = pygame.Rect(260, 60, 1000, 580)
    pygame.draw.rect(surface, (*theme["background"], 200), dashboard_rect)
    pygame.draw.rect(surface, theme["primary"], dashboard_rect, 2)

    # Layer 3: Procedural Main Visual (Immersive center-piece)
    inner_rect = dashboard_rect.inflate(-40, -40)
    rng_display = WorldRNG(game_state.config.seed + 123)

    visual_type = theme.get("procedural_main")
    if visual_type == "molecule_diagram":
        draw_molecule_diagram(surface, rng_display, {"pressure_level": game_state.pressure_level}, theme, inner_rect)
    elif visual_type == "candlestick_chart":
        draw_candlestick_chart(surface, rng_display, {}, theme, inner_rect)
    elif visual_type == "growth_curve":
        draw_growth_curve(surface, rng_display, {}, theme, inner_rect)

    # ML Stats Overlay (Subtle)
    font_small = get_font(12)
    ml_label = font_small.render(f"DIF_ADJ: {game_state.difficulty_adj[0]:.3f} | BAYES_PRESSURE: {game_state.pressure_level:.2f}", True, theme["accent"])
    surface.blit(ml_label, (270, 615))

    # Layer 4: Agent Panel
    draw_agent_panel(surface, game_state.agents, theme)

    # Layer 5: HUD
    draw_hud(surface, game_state, theme)

    # Event Notification (if any)
    if hasattr(game_state, 'notification') and game_state.notification:
        draw_notification(surface, game_state.notification, theme)

    # Layer 6: Challenge Overlay
    if game_state.active_challenge:
        game_state.active_challenge.draw(surface)

def draw_notification(surface, text, theme):
    font = get_font(20, bold=True)
    text_surf = font.render(text, True, (255, 255, 255))
    rect = text_surf.get_rect(center=(640, 100))
    bg_rect = rect.inflate(40, 20)
    pygame.draw.rect(surface, (200, 0, 0), bg_rect)
    pygame.draw.rect(surface, (255, 255, 255), bg_rect, 2)
    surface.blit(text_surf, rect)
