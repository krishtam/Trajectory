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

def render_frame(surface: pygame.Surface, game_state, theme: dict,
                 scene_objects, particle_system):

    # Layer 0: Background
    surface.fill(theme["background"])

    # Layer 1: Particles
    particle_system.update()
    particle_system.draw(surface)

    # Layer 2: Scene Objects
    for obj in scene_objects:
        surface.blit(obj.surface, obj.rect)

    # Layer 3: Procedural Main Visual
    main_rect = pygame.Rect(340, 100, 800, 400)
    rng_display = WorldRNG(game_state.config.seed + 123)

    visual_type = theme.get("procedural_main")
    if visual_type == "molecule_diagram":
        draw_molecule_diagram(surface, rng_display, {}, theme, main_rect)
    elif visual_type == "candlestick_chart":
        draw_candlestick_chart(surface, rng_display, {}, theme, main_rect)
    elif visual_type == "growth_curve":
        draw_growth_curve(surface, rng_display, {}, theme, main_rect)
    elif visual_type == "org_chart":
        draw_org_chart(surface, rng_display, {}, theme, main_rect)
    elif visual_type == "network_graph":
        draw_network_graph(surface, rng_display, {}, theme, main_rect)
    elif visual_type == "audience_curve":
        draw_audience_curve(surface, rng_display, {}, theme, main_rect)

    # Layer 4: Agent Panel
    draw_agent_panel(surface, game_state.agents, theme)

    # Layer 5: HUD
    draw_hud(surface, game_state, theme)

    # Layer 6: Challenge Overlay
    if game_state.active_challenge:
        game_state.active_challenge.draw(surface)
