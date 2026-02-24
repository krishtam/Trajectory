import pygame

def draw_org_chart(surface: pygame.Surface, rng_display,
                   world_data: dict, theme: dict, rect: pygame.Rect):
    """
    Draws a procedural org chart for Operator/Manager.
    """
    center_x = rect.centerx
    top_y = rect.top + 20

    # Root node
    pygame.draw.rect(surface, theme["primary"], (center_x - 40, top_y, 80, 30), 2)

    # Children
    for i in range(3):
        child_x = rect.left + (i + 1) * (rect.width // 4)
        child_y = top_y + 80
        pygame.draw.line(surface, theme["grid"], (center_x, top_y + 30), (child_x, child_y), 1)
        pygame.draw.rect(surface, theme["accent"], (child_x - 30, child_y, 60, 25), 2)
