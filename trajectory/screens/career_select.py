import pygame
from trajectory.core.career_taxonomy import CAREER_TAXONOMY

class CareerSelectScreen:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 18)
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
        surface.fill((10, 15, 25))
        title = self.font.render("SELECT YOUR CAREER TRAJECTORY", True, (255, 255, 255))
        surface.blit(title, (640 - title.get_width()//2, 100))

        for i, (pillar, career) in enumerate(self.careers):
            color = (100, 200, 255) if i == self.selected_idx else (150, 150, 150)
            text = self.font.render(f"{career} ({pillar})", True, color)
            rect = text.get_rect(center=(640, 250 + i * 80))
            if i == self.selected_idx:
                pygame.draw.rect(surface, color, rect.inflate(20, 10), 2)
            surface.blit(text, rect)

        hint = self.small_font.render("Use Arrow Keys to select, ENTER to start", True, (100, 100, 100))
        surface.blit(hint, (640 - hint.get_width()//2, 600))
