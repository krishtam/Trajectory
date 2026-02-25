import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult
from trajectory.rendering.font_utils import get_font

class SignalReadingChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        if self.scenario:
            self.prompt_text = self.scenario["prompt"]
            self.correct_text = self.scenario["correct"]
            self.options = self.scenario["options"]
        else:
            self.prompt_text = "Identify the outlier."
            self.correct_text = "Outlier 1"
            self.options = ["Outlier 1", "Normal 1", "Normal 2"]

        self.font = get_font(22)
        self.header_font = get_font(28, bold=True)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, opt in enumerate(self.options):
                    rect = pygame.Rect(440, 250 + i * 90, 400, 70)
                    if rect.collidepoint(x, y):
                        accuracy = 1.0 if opt == self.correct_text else 0.0
                        time_taken = self.get_elapsed_ms()
                        performance = accuracy * (1.0 - min(0.5, time_taken / 20000))
                        return ChallengeResult(performance, time_taken)

        if self.get_elapsed_ms() > 15000:
            return ChallengeResult(0.0, 15000)
        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((10, 20, 30, 230))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, self.theme["primary"], (340, 100, 600, 520), 2)

        title = self.header_font.render("SIGNAL ANALYSIS", True, self.theme["primary"])
        surface.blit(title, (640 - title.get_width()//2, 130))

        prompt = self.font.render(self.prompt_text, True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 180))

        for i, opt in enumerate(self.options):
            rect = pygame.Rect(440, 250 + i * 90, 400, 70)
            pygame.draw.rect(surface, self.theme["grid"], rect)
            pygame.draw.rect(surface, self.theme["accent"], rect, 2)

            label = self.font.render(opt, True, self.theme["text"])
            surface.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

        # Progress bar
        time_left = max(0, 15000 - self.get_elapsed_ms())
        pygame.draw.rect(surface, (100, 100, 100), (440, 550, 400, 10))
        pygame.draw.rect(surface, self.theme["primary"], (440, 550, int(400 * (time_left / 15000)), 10))
