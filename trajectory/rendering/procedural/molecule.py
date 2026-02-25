import math
import pygame

def draw_molecule_diagram(surface: pygame.Surface, rng_display,
                           world_data: dict, theme: dict, rect: pygame.Rect):
    """
    Overhauled: Renders a medical Bio-Analysis visualization (Human Heart Region)
    instead of simple chemistry molecules.
    """
    # Draw Human Silhouette Placeholder (Stylized)
    center_x = rect.centerx
    center_y = rect.centery

    # Head
    pygame.draw.circle(surface, theme["grid"], (center_x, rect.top + 50), 30)
    # Torso
    pygame.draw.rect(surface, theme["grid"], (center_x - 60, rect.top + 85, 120, 180), border_radius=15)

    # Heart Region Glow
    heart_pos = (center_x - 15, rect.top + 130)
    pressure = world_data.get("pressure_level", 0.5)
    pulse = math.sin(pygame.time.get_ticks() * 0.005) * 5
    glow_r = int(25 + pulse + pressure * 20)

    glow_col = (255, 100, 100, 100) if pressure > 0.7 else (100, 200, 255, 100)
    temp_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.circle(temp_surf, glow_col, heart_pos, glow_r)
    surface.blit(temp_surf, (0,0))

    # Stylized Anatomical Heart (Simple vector)
    pygame.draw.ellipse(surface, (200, 50, 50), (heart_pos[0]-15, heart_pos[1]-20, 30, 40))

    # Animated Vitals Lines (ECG-like)
    points = []
    for x in range(rect.left + 50, rect.right - 50, 5):
        offset = math.sin(x * 0.05 + pygame.time.get_ticks() * 0.01) * 20
        # Periodic 'spike'
        if (x + pygame.time.get_ticks()//10) % 200 < 20:
            offset -= 40
        points.append((x, rect.bottom - 100 + offset))

    if len(points) > 1:
        pygame.draw.lines(surface, (100, 255, 150), False, points, 2)

    # Status Labels
    from trajectory.rendering.font_utils import get_font
    font = get_font(12, bold=True)
    status = "CRITICAL" if pressure > 0.7 else "STABLE"
    lbl = font.render(f"SYSTEM STATUS: {status}", True, (255, 255, 255))
    surface.blit(lbl, (center_x - lbl.get_width()//2, rect.bottom - 40))
