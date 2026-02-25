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
            self.prompt_text = "Allocate resources."
            self.targets = ["Alpha", "Beta", "Gamma"]

        self.font = get_font(20)
        self.header_font = get_font(28, bold=True)
        self.allocation = [0] * len(self.targets)
        self.ideal = [50, 30, 20] # Hidden ideal

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
        overlay.fill((10, 20, 30, 230))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, self.theme["primary"], (340, 120, 600, 480), 2)

        title = self.header_font.render("RESOURCE ALLOCATION", True, self.theme["primary"])
        surface.blit(title, (640 - title.get_width()//2, 150))

        prompt = self.font.render(self.prompt_text, True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 200))

        instruction = self.font.render("(Press 1, 2, 3 to increment)", True, self.theme["accent"])
        surface.blit(instruction, (640 - instruction.get_width()//2, 230))

        for i, target in enumerate(self.targets):
            y = 280 + i * 80
            pygame.draw.rect(surface, (40, 40, 50), (440, y, 400, 40))
            pygame.draw.rect(surface, self.theme["primary"], (440, y, int(4 * self.allocation[i]), 40))
            label = self.font.render(f"{target}: {self.allocation[i]}%", True, (255, 255, 255))
            surface.blit(label, (860, y + 5))

        pygame.draw.rect(surface, self.theme["primary"], (590, 520, 100, 50))
        sub_label = self.font.render("DEPLOY", True, self.theme["background"])
        surface.blit(sub_label, (640 - sub_label.get_width()//2, 532))
