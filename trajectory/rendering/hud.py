import pygame
from trajectory.rendering.font_utils import get_font

def draw_hud(surface: pygame.Surface, state, theme: dict):
    # Top bar (Darker, translucent)
    top_rect = pygame.Rect(0, 0, 1280, 60)
    pygame.draw.rect(surface, (5, 10, 20), top_rect)
    pygame.draw.line(surface, theme["primary"], (0, 60), (1280, 60), 2)

    font_main = get_font(24, bold=True)
    font_sub = get_font(14)

    # Career Identity
    title = font_main.render(state.config.career.upper(), True, theme["primary"])
    surface.blit(title, (20, 10))
    pillar_text = font_sub.render(f"ARCHETYPE: {state.config.pillar.upper()}", True, theme["accent"])
    surface.blit(pillar_text, (20, 38))

    # Cycle Timeline
    total_cycles = state.config.win_condition.time_limit_cycles
    progress = state.cycle / total_cycles
    bar_width = 400
    bar_x = 440
    pygame.draw.rect(surface, (30, 30, 40), (bar_x, 25, bar_width, 10), border_radius=5)
    pygame.draw.rect(surface, theme["primary"], (bar_x, 25, int(bar_width * progress), 10), border_radius=5)

    time_label = font_sub.render(f"CAREER PROGRESS: {int(progress*100)}%", True, (200, 200, 200))
    surface.blit(time_label, (bar_x + bar_width//2 - time_label.get_width()//2, 40))

    # Bottom HUD
    bot_rect = pygame.Rect(0, 656, 1280, 64)
    pygame.draw.rect(surface, (5, 10, 20), bot_rect)
    pygame.draw.line(surface, theme["primary"], (0, 656), (1280, 656), 2)

    # Resource Metrics
    metric_font = get_font(20, bold=True)
    res_val = int(state.resource)
    res_label = metric_font.render(f"{state.config.win_condition.metric.upper()}: {res_val:,}", True, (255, 255, 255))
    surface.blit(res_label, (20, 675))

    target_val = int(state.config.win_condition.target_value)
    target_label = font_sub.render(f"GOAL: {target_val:,}", True, theme["accent"])
    surface.blit(target_label, (20, 700))

    # Right Side Info
    seed_label = font_sub.render(f"SEED_PROTOCOL: {state.config.seed}", True, (100, 100, 120))
    surface.blit(seed_label, (1100, 685))
