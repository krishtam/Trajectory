import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult

class SignalReadingChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        self.correct_idx = rng.integers(0, 3)
        self.signals = ["Signal A", "Signal B", "Signal C"]
        self.labels = self._get_labels(config.career)
        self.selected_idx = None
        self.font = pygame.font.SysFont("Arial", 24)

    def _get_labels(self, career):
        if career == "Chemist":
            return ["Compound Alpha Yield", "Compound Beta Yield", "Compound Gamma Yield"]
        elif career == "Trader":
            return ["Asset Momentum", "Volume Anomaly", "Alpha Score"]
        elif career == "Entrepreneur":
            return ["User Growth Rate", "Retention Index", "Burn Rate Stability"]
        return ["Metric 1", "Metric 2", "Metric 3"]

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(3):
                    rect = pygame.Rect(440, 200 + i * 100, 400, 80)
                    if rect.collidepoint(x, y):
                        self.selected_idx = i
                        accuracy = 1.0 if i == self.correct_idx else 0.0
                        time_taken = self.get_elapsed_ms()
                        performance = accuracy * (1.0 - min(1.0, time_taken / 15000))
                        return ChallengeResult(performance, time_taken)
        return None

    def draw(self, surface):
        # Dim background
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        prompt = self.font.render(f"Select the strongest {self.labels[self.correct_idx]}", True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 120))

        for i in range(3):
            rect = pygame.Rect(440, 200 + i * 100, 400, 80)
            pygame.draw.rect(surface, self.theme["primary"], rect, 2)
            label = self.font.render(self.labels[i], True, self.theme["text"])
            surface.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

        # Timer bar
        time_left = max(0, 15000 - self.get_elapsed_ms())
        pygame.draw.rect(surface, (200, 0, 0), (440, 550, int(400 * (time_left / 15000)), 10))
