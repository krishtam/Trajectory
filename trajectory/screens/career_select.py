import pygame
from trajectory.rendering.font_utils import get_font

class CareerSelectScreen:
    def __init__(self):
        self.font = get_font(36, bold=True)
        self.small_font = get_font(18)
        self.careers = [
            ("Expert", "Chemist"),
            ("Allocator", "Trader"),
            ("Builder", "Entrepreneur")
        ]
        self.selected_idx = 0

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_idx = (self.selected_idx + 1) % len(self.careers)
                elif event.key == pygame.K_UP:
                    self.selected_idx = (self.selected_idx - 1) % len(self.careers)
                elif event.key == pygame.K_RETURN:
                    return self.careers[self.selected_idx]
            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.careers[self.selected_idx]
        return None

    def draw(self, surface):
        surface.fill((5, 10, 20))

        # Draw background grid
        for i in range(0, 1280, 80):
            pygame.draw.line(surface, (15, 20, 35), (i, 0), (i, 720))
        for j in range(0, 720, 80):
            pygame.draw.line(surface, (15, 20, 35), (0, j), (1280, j))

        title = self.font.render("SELECT CAREER TRAJECTORY", True, (255, 255, 255))
        surface.blit(title, (640 - title.get_width()//2, 80))

        sub = self.small_font.render("SIMULATION PARAMETERS WILL BE OPTIMIZED PER CAREER ARCHETYPE", True, (100, 150, 200))
        surface.blit(sub, (640 - sub.get_width()//2, 130))

        for i, (pillar, career) in enumerate(self.careers):
            color = (100, 200, 255) if i == self.selected_idx else (100, 100, 120)
            bg_color = (20, 30, 50) if i == self.selected_idx else (10, 15, 25)

            rect = pygame.Rect(440, 250 + i * 110, 400, 90)
            pygame.draw.rect(surface, bg_color, rect, border_radius=15)
            pygame.draw.rect(surface, color, rect, 2, border_radius=15)

            text = self.font.render(career.upper(), True, color)
            surface.blit(text, (640 - text.get_width()//2, 260 + i * 110))

            p_text = self.small_font.render(f"Pillar: {pillar}", True, (150, 150, 170))
            surface.blit(p_text, (640 - p_text.get_width()//2, 305 + i * 110))

        hint = self.small_font.render("NAVIGATE WITH ARROWS | INITIALIZE WITH ENTER", True, (80, 80, 100))
        surface.blit(hint, (640 - hint.get_width()//2, 650))
