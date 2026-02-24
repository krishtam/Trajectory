import pygame
from trajectory.rendering.font_utils import get_font

def draw_hud(surface: pygame.Surface, state, theme: dict):
    # Top bar
    pygame.draw.rect(surface, theme["background"], (0, 0, 1280, 48))
    pygame.draw.line(surface, theme["grid"], (0, 48), (1280, 48))

    font = get_font(18, bold=True)
    title = font.render(f"{state.config.career.upper()} - {state.config.pillar}", True, theme["text"])
    surface.blit(title, (10, 12))

    # Timeline
    progress = state.cycle / state.config.win_condition.time_limit_cycles
    pygame.draw.rect(surface, theme["grid"], (400, 20, 400, 8))
    pygame.draw.rect(surface, theme["primary"], (400, 20, int(400 * progress), 8))

    # Bottom bar
    pygame.draw.rect(surface, theme["background"], (0, 720-64, 1280, 64))
    pygame.draw.line(surface, theme["grid"], (0, 720-64), (1280, 720-64))

    res_label = font.render(f"{state.config.win_condition.metric}: {int(state.resource)}", True, theme["text"])
    surface.blit(res_label, (20, 720-40))

    seed_label = font.render(f"SEED: {state.config.seed}", True, theme["text"])
    surface.blit(seed_label, (1100, 720-40))
