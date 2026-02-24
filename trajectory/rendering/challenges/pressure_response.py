import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult

class PressureResponseChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        self.font = pygame.font.SysFont("Arial", 22)
        self.event_text = self._get_event_text(config.career)
        self.options = ["Aggressive", "Balanced", "Cautious"]

    def _get_event_text(self, career):
        if career == "Chemist":
            return "A pressure valve is failing in the lab!"
        elif career == "Trader":
            return "A major bank just announced bankruptcy!"
        elif career == "Entrepreneur":
            return "Your server is under heavy load!"
        return "An urgent crisis requires your attention!"

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(3):
                    rect = pygame.Rect(440, 300 + i * 80, 400, 60)
                    if rect.collidepoint(x, y):
                        # Outcome sampling simplified
                        performance = 0.8 if i == 1 else 0.4
                        return ChallengeResult(performance, self.get_elapsed_ms())

        if self.get_elapsed_ms() > 10000:
            return ChallengeResult(0.2, 10000) # Timeout

        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((100, 0, 0, 150)) # Red tint for pressure
        surface.blit(overlay, (0, 0))

        prompt = self.font.render(self.event_text, True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 200))

        for i, opt in enumerate(self.options):
            rect = pygame.Rect(440, 300 + i * 80, 400, 60)
            pygame.draw.rect(surface, self.theme["primary"], rect, 2)
            label = self.font.render(opt, True, self.theme["text"])
            surface.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

        # Timer circle
        time_left = max(0, 10000 - self.get_elapsed_ms())
        pygame.draw.arc(surface, (255, 255, 255), (600, 550, 80, 80), 0, (time_left / 10000) * 6.28, 5)
