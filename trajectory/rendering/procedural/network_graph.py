import pygame
import math

def draw_network_graph(surface: pygame.Surface, rng_display,
                       world_data: dict, theme: dict, rect: pygame.Rect):
    """
    Draws a procedural network graph for Connector/Sales.
    """
    nodes = []
    for _ in range(8):
        nodes.append((
            rng_display.integers(rect.left + 20, rect.right - 20),
            rng_display.integers(rect.top + 20, rect.bottom - 20)
        ))

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if rng_display.uniform() < 0.3:
                pygame.draw.line(surface, theme["grid"], nodes[i], nodes[j], 1)

    for node in nodes:
        pygame.draw.circle(surface, theme["primary"], node, 6)
        pygame.draw.circle(surface, theme["accent"], node, 6, 1)
