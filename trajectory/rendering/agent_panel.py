import pygame
from trajectory.rendering.font_utils import get_font

def draw_agent_panel(surface: pygame.Surface, agents, theme: dict):
    panel_rect = pygame.Rect(0, 60, 260, 596)
    pygame.draw.rect(surface, (10, 15, 25), panel_rect)
    pygame.draw.line(surface, theme["primary"], (260, 60), (260, 656), 2)

    font_header = get_font(16, bold=True)
    font_name = get_font(14, bold=True)
    font_state = get_font(12)

    header = font_header.render("PROFESSIONAL NETWORK", True, theme["accent"])
    surface.blit(header, (130 - header.get_width()//2, 75))

    for i, agent in enumerate(agents):
        y_base = 110 + i * 120
        agent_rect = pygame.Rect(10, y_base, 240, 110)
        pygame.draw.rect(surface, (20, 25, 40), agent_rect, border_radius=10)

        # Archetype Icon / Portrait
        color = theme["primary"]
        if agent.config.archetype in ["adversary", "competitor"]:
            color = (255, 80, 80)
        elif agent.config.archetype == "authority":
            color = (255, 200, 50)

        # Draw Portrait or Icon
        from trajectory.rendering.programmatic_assets import ProgrammaticAssets
        portrait_name = "generic_icon"
        if "Surgeon" in theme.get("terminology", {}).get("agent_authority", ""):
            if agent.config.archetype == "authority": portrait_name = "portrait_anesthesiologist_f"
            elif agent.config.archetype == "gatekeeper": portrait_name = "portrait_nurse_m"
            else: portrait_name = "portrait_resident_f"
        elif "Trader" in theme.get("terminology", {}).get("agent_authority", ""):
            if agent.config.archetype == "authority": portrait_name = "agent_fed_icon"
            elif agent.config.archetype == "competitor": portrait_name = "agent_whale_icon"
            elif agent.config.archetype == "opportunity": portrait_name = "agent_analyst_icon"
            else: portrait_name = "agent_algorithm_icon"

        p_surf = ProgrammaticAssets.get_surface(portrait_name, size=(80, 80), color=color)
        surface.blit(p_surf, (20, y_base + 15))

        # Info
        name_txt = font_name.render(agent.config.archetype.upper(), True, (255, 255, 255))
        surface.blit(name_txt, (75, y_base + 15))

        state_txt = font_state.render(f"STATUS: {agent.current_state.upper()}", True, color)
        surface.blit(state_txt, (75, y_base + 35))

        # Relationship Bar
        pygame.draw.rect(surface, (40, 40, 50), (75, y_base + 55, 140, 6))
        rel_fill = int((agent.relationship + 1) / 2 * 140)
        pygame.draw.rect(surface, theme["primary"], (75, y_base + 55, rel_fill, 6))
