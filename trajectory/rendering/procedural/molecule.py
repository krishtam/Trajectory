import math
import pygame

def draw_molecule_diagram(surface: pygame.Surface, rng_display,
                           world_data: dict, theme: dict, rect: pygame.Rect):
    """
    Draws a procedural molecule diagram seeded by world data.
    """
    n_atoms = rng_display.integers(5, 12)
    center_x = rect.centerx
    center_y = rect.centery
    radius = min(rect.width, rect.height) * 0.35

    # Place atoms on concentric rings
    atoms = [(center_x, center_y)]  # center atom always exists
    ring_sizes = [3, 5, 8]

    for ring_idx, ring_size in enumerate(ring_sizes):
        if len(atoms) >= n_atoms:
            break
        ring_radius = radius * (0.3 + ring_idx * 0.35)
        for j in range(ring_size):
            if len(atoms) >= n_atoms:
                break
            angle = (2 * math.pi / ring_size) * j + rng_display.uniform(0, 0.3)
            ax = center_x + ring_radius * math.cos(angle)
            ay = center_y + ring_radius * math.sin(angle)
            atoms.append((ax, ay))

    # Draw bonds (connect atoms within distance threshold)
    bond_threshold = radius * 0.5
    for i in range(len(atoms)):
        for j in range(i+1, len(atoms)):
            dx = atoms[i][0] - atoms[j][0]
            dy = atoms[i][1] - atoms[j][1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < bond_threshold:
                alpha = int(180 * (1 - dist/bond_threshold))
                bond_color = (*theme["primary"][:3], alpha)
                # Create a temporary surface for transparent lines
                temp_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                pygame.draw.line(temp_surf, bond_color,
                                (int(atoms[i][0]), int(atoms[i][1])),
                                (int(atoms[j][0]), int(atoms[j][1])), 2)
                surface.blit(temp_surf, (0,0))

    # Draw atoms
    element_symbols = ["C", "H", "O", "N", "S", "P", "Fe", "Cl"]
    from trajectory.rendering.font_utils import get_font
    font = get_font(12)

    for i, (ax, ay) in enumerate(atoms):
        pressure = world_data.get("pressure_level", 0.5)
        pulse = math.sin(pygame.time.get_ticks() * 0.002 + i) * 2
        atom_r = int(10 + pulse + pressure * 3)

        pygame.draw.circle(surface, theme["primary"], (int(ax), int(ay)), atom_r)
        pygame.draw.circle(surface, theme["accent"], (int(ax), int(ay)), atom_r, 2)

        # Element label
        symbol = element_symbols[i % len(element_symbols)]
        label = font.render(symbol, True, theme["background"])
        surface.blit(label, (int(ax) - label.get_width()//2, int(ay) - label.get_height()//2))
