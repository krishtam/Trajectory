import pygame
import math

class Particle:
    SHAPE_FUNCS = {
        "hexagon": "_draw_hexagon",
        "line":    "_draw_line",
        "circle":  "_draw_circle",
        "dot":     "_draw_dot",
        "square":  "_draw_square",
        "scatter": "_draw_dot",
    }

    def __init__(self, rng, theme: dict, width: int, height: int):
        self.x = float(rng.integers(0, width))
        self.y = float(rng.integers(0, height))
        self.vx = float(rng.uniform(-0.4, 0.4))
        self.vy = float(rng.uniform(-0.4, 0.4))
        self.size = float(rng.uniform(2.5, 7.0))
        self.rotation = float(rng.uniform(0, 360))
        self.rot_speed = float(rng.uniform(-0.4, 0.4))
        self.shape = theme["particle_shape"]
        self.color = theme["particle_color"]
        self.W = width
        self.H = height

    def update(self):
        self.x = (self.x + self.vx) % self.W
        self.y = (self.y + self.vy) % self.H
        self.rotation = (self.rotation + self.rot_speed) % 360

    def draw(self, surface: pygame.Surface):
        draw_fn = getattr(self, self.SHAPE_FUNCS.get(self.shape, "_draw_dot"))
        draw_fn(surface)

    def _draw_hexagon(self, surface):
        pts = []
        for i in range(6):
            angle_rad = math.radians(self.rotation + 60 * i)
            pts.append((
                self.x + self.size * math.cos(angle_rad),
                self.y + self.size * math.sin(angle_rad)
            ))
        pygame.draw.polygon(surface, self.color, pts, 1)

    def _draw_line(self, surface):
        angle_rad = math.radians(self.rotation)
        x2 = self.x + self.size * math.cos(angle_rad)
        y2 = self.y + self.size * math.sin(angle_rad)
        pygame.draw.line(surface, self.color, (self.x, self.y), (x2, y2), 1)

    def _draw_circle(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size), 1)

    def _draw_dot(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 1)

    def _draw_square(self, surface):
        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (self.x, self.y)
        pygame.draw.rect(surface, self.color, rect, 1)

class ParticleSystem:
    def __init__(self, rng, theme: dict, width: int, height: int):
        self.particles = [Particle(rng, theme, width, height) for _ in range(theme.get("particle_count", 50))]

    def update(self):
        for p in self.particles:
            p.update()

    def draw(self, surface: pygame.Surface):
        # Using a transparent surface for all particles if needed, but here we draw directly
        for p in self.particles:
            p.draw(surface)
