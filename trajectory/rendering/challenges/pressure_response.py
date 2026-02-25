import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult
from trajectory.rendering.font_utils import get_font

class PressureResponseChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        if self.scenario:
            self.event_text = self.scenario["prompt"]
            self.options = self.scenario["options"]
        else:
            self.event_text = "Urgent crisis!"
            self.options = ["Option A", "Option B", "Option C"]

        self.font = get_font(20)
        self.header_font = get_font(28, bold=True)
        self.timer_duration = 10000

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(3):
                    rect = pygame.Rect(440, 300 + i * 90, 400, 70)
                    if rect.collidepoint(x, y):
                        # Simplified performance logic
                        performance = 0.9 if i == 1 else 0.5
                        return ChallengeResult(performance, self.get_elapsed_ms())

        if self.get_elapsed_ms() > self.timer_duration:
            return ChallengeResult(0.1, self.timer_duration)

        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 200)) # Red tint
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (255, 50, 50), (340, 150, 600, 450), 2)

        title = self.header_font.render("PRESSURE RESPONSE", True, (255, 100, 100))
        surface.blit(title, (640 - title.get_width()//2, 180))

        prompt = self.font.render(self.event_text, True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 230))

        for i, opt in enumerate(self.options):
            rect = pygame.Rect(440, 300 + i * 90, 400, 70)
            pygame.draw.rect(surface, (80, 20, 20), rect)
            pygame.draw.rect(surface, (255, 50, 50), rect, 2)
            label = self.font.render(opt, True, (255, 255, 255))
            surface.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

        # Circular timer
        time_left = max(0, self.timer_duration - self.get_elapsed_ms())
        import math
        pygame.draw.arc(surface, (255, 255, 255), (600, 580, 80, 80), 0, (time_left / self.timer_duration) * 2 * math.pi, 5)
