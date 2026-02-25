import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult
from trajectory.rendering.font_utils import get_font

class ResourceAllocationChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        if self.scenario:
            self.prompt_text = self.scenario["prompt"]
            self.targets = self.scenario["targets"]
        else:
            self.prompt_text = "Allocate professional bandwidth."
            self.targets = ["Focus A", "Focus B", "Focus C"]

        self.font = get_font(18)
        self.header_font = get_font(28, bold=True)
        self.allocation = [0] * len(self.targets)
        self.ideal = [40, 40, 20] # Hidden ideal

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if pygame.Rect(590, 520, 100, 50).collidepoint(x, y):
                    diff = sum(abs(a - b) for a, b in zip(self.allocation, self.ideal))
                    performance = max(0.1, 1.0 - (diff / 100))
                    return ChallengeResult(performance, self.get_elapsed_ms())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: self.allocation[0] = min(100, self.allocation[0] + 10)
                if event.key == pygame.K_2: self.allocation[1] = min(100, self.allocation[1] + 10)
                if event.key == pygame.K_3: self.allocation[2] = min(100, self.allocation[2] + 10)

        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((10, 20, 30, 240))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, self.theme["primary"], (340, 80, 600, 560), 2, border_radius=15)

        title = self.header_font.render("RESOURCE ALLOCATION", True, self.theme["accent"])
        surface.blit(title, (640 - title.get_width()//2, 110))

        prompt = self.font.render(self.prompt_text, True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 160))

        hint = self.font.render("(PRESS 1, 2, 3 TO INCREMENT PERCENTAGE)", True, self.theme["accent"])
        surface.blit(hint, (640 - hint.get_width()//2, 200))

        total = sum(self.allocation)
        total_label = self.font.render(f"TOTAL DEPLOYED: {total}%", True, (100, 255, 100) if total <= 100 else (255, 100, 100))
        surface.blit(total_label, (640 - total_label.get_width()//2, 240))

        for i, target in enumerate(self.targets):
            y = 300 + i * 80
            pygame.draw.rect(surface, (30, 35, 50), (440, y, 400, 45), border_radius=10)
            pygame.draw.rect(surface, self.theme["primary"], (440, y, int(4 * self.allocation[i]), 45), border_radius=10)

            label = self.font.render(f"{target.upper()}: {self.allocation[i]}%", True, (255, 255, 255))
            surface.blit(label, (460, y + 10))

        pygame.draw.rect(surface, self.theme["accent"], (590, 550, 100, 50), border_radius=10)
        sub_label = get_font(16, bold=True).render("DEPLOY", True, self.theme["background"])
        surface.blit(sub_label, (640 - sub_label.get_width()//2, 562))
