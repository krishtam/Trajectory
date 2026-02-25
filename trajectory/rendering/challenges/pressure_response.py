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
            self.event_text = "Urgent situational crisis!"
            self.options = ["Standard Response", "Emergency Protocol", "Consult Authority"]

        self.font = get_font(20)
        self.header_font = get_font(28, bold=True)
        self.timer_duration = 10000

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(len(self.options)):
                    rect = pygame.Rect(440, 300 + i * 90, 400, 70)
                    if rect.collidepoint(x, y):
                        performance = 0.95 if i == 1 else 0.6
                        return ChallengeResult(performance, self.get_elapsed_ms())

        if self.get_elapsed_ms() > self.timer_duration:
            return ChallengeResult(0.2, self.timer_duration)

        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 200)) # High-tension red tint
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (255, 50, 50), (340, 150, 600, 480), 2, border_radius=15)

        title = self.header_font.render("PRESSURE RESPONSE", True, (255, 100, 100))
        surface.blit(title, (640 - title.get_width()//2, 180))

        # Wrapped prompt
        words = self.event_text.split(' ')
        lines = []
        current_line = ""
        for w in words:
            if self.font.size(current_line + w)[0] < 500:
                current_line += w + " "
            else:
                lines.append(current_line)
                current_line = w + " "
        lines.append(current_line)

        for i, line in enumerate(lines[:3]):
            txt = self.font.render(line, True, (255, 255, 255))
            surface.blit(txt, (640 - txt.get_width()//2, 230 + i * 25))

        for i, opt in enumerate(self.options):
            rect = pygame.Rect(440, 320 + i * 90, 400, 70)
            pygame.draw.rect(surface, (60, 15, 15), rect, border_radius=10)
            pygame.draw.rect(surface, (255, 80, 80), rect, 2, border_radius=10)
            label = self.font.render(opt.upper(), True, (255, 255, 255))
            surface.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

        # Animated circular timer
        time_left = max(0, self.timer_duration - self.get_elapsed_ms())
        import math
        pygame.draw.arc(surface, (255, 255, 255), (600, 600, 80, 80), 0, (time_left / self.timer_duration) * 2 * math.pi, 5)
