import pygame

def draw_agent_panel(surface: pygame.Surface, agents, theme: dict):
    panel_rect = pygame.Rect(0, 48, 240, 608)
    pygame.draw.rect(surface, theme["background"], panel_rect)
    pygame.draw.line(surface, theme["grid"], (240, 48), (240, 656))

    font = pygame.font.SysFont("Arial", 14)

    for i, agent in enumerate(agents):
        y = 80 + i * 80
        # Agent node
        color = theme["primary"]
        if agent.config.archetype in ["adversary", "competitor"]:
            color = (255, 100, 100)
        elif agent.config.archetype == "opportunity":
            color = theme["accent"]

        pygame.draw.circle(surface, color, (120, y), 20, 2)
        pygame.draw.circle(surface, color, (120, y), 15 if agent.current_state == "active" else 10)

        # Name and state
        name_label = font.render(f"{agent.config.archetype.capitalize()}", True, theme["text"])
        surface.blit(name_label, (120 - name_label.get_width()//2, y + 25))

        state_label = font.render(f"[{agent.current_state}]", True, color)
        surface.blit(state_label, (120 - state_label.get_width()//2, y + 40))

        # Relationship bar
        rel_width = 100
        pygame.draw.rect(surface, theme["grid"], (70, y - 35, rel_width, 4))
        fill_width = int((agent.relationship + 1) / 2 * rel_width)
        pygame.draw.rect(surface, theme["primary"], (70, y - 35, fill_width, 4))
