import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult
from trajectory.rendering.font_utils import get_font

class SignalReadingChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        # Use scenario from data if available, else fallback
        if self.scenario:
            self.prompt_text = self.scenario["prompt"]
            self.correct_text = self.scenario["correct"]
            self.options = self.scenario["options"]
        else:
            self.prompt_text = "Analyze the professional signal."
            self.correct_text = "Signal A"
            self.options = ["Signal A", "Signal B", "Signal C"]

        self.font = get_font(20)
        self.header_font = get_font(28, bold=True)
        self.timer_duration = 15000

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, opt in enumerate(self.options):
                    rect = pygame.Rect(440, 250 + i * 90, 400, 70)
                    if rect.collidepoint(x, y):
                        accuracy = 1.0 if opt == self.correct_text else 0.0
                        time_taken = self.get_elapsed_ms()
                        performance = accuracy * (1.0 - min(0.5, time_taken / self.timer_duration))
                        return ChallengeResult(performance, time_taken)

        if self.get_elapsed_ms() > self.timer_duration:
            return ChallengeResult(0.1, self.timer_duration)
        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((10, 20, 30, 240))
        surface.blit(overlay, (0, 0))

        # Professional Frame
        pygame.draw.rect(surface, self.theme["primary"], (340, 80, 600, 560), 2, border_radius=15)

        title = self.header_font.render("SITUATIONAL ANALYSIS", True, self.theme["accent"])
        surface.blit(title, (640 - title.get_width()//2, 110))

        # Scenario Text (Wrapped)
        from trajectory.rendering.renderer import draw_narrative_box
        # We reuse the wrap logic by just rendering here
        words = self.prompt_text.split(' ')
        lines = []
        current_line = ""
        for w in words:
            if self.font.size(current_line + w)[0] < 500:
                current_line += w + " "
            else:
                lines.append(current_line)
                current_line = w + " "
        lines.append(current_line)

        for i, line in enumerate(lines):
            txt = self.font.render(line, True, (255, 255, 255))
            surface.blit(txt, (640 - txt.get_width()//2, 170 + i * 25))

        # Options
        for i, opt in enumerate(self.options):
            rect = pygame.Rect(440, 300 + i * 90, 400, 70)
            pygame.draw.rect(surface, (20, 30, 50), rect, border_radius=10)
            pygame.draw.rect(surface, self.theme["primary"], rect, 2, border_radius=10)

            label = self.font.render(opt, True, self.theme["text"])
            surface.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

        # Timer
        time_left = max(0, self.timer_duration - self.get_elapsed_ms())
        pygame.draw.rect(surface, (40, 40, 60), (440, 600, 400, 10), border_radius=5)
        pygame.draw.rect(surface, (255, 100, 100), (440, 600, int(400 * (time_left / self.timer_duration)), 10), border_radius=5)
