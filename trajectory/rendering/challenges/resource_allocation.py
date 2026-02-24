import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult

class ResourceAllocationChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        self.font = pygame.font.SysFont("Arial", 24)
        self.targets = ["Target Alpha", "Target Beta", "Target Gamma"]
        self.allocation = [0, 0, 0]
        self.total_resource = 100
        self.ideal = [50, 30, 20] # Hidden ideal

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if pygame.Rect(590, 500, 100, 50).collidepoint(x, y):
                    # Submit
                    diff = sum(abs(a - b) for a, b in zip(self.allocation, self.ideal))
                    performance = max(0, 1.0 - (diff / 100))
                    return ChallengeResult(performance, self.get_elapsed_ms())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: self.allocation[0] = min(100, self.allocation[0] + 10)
                if event.key == pygame.K_2: self.allocation[1] = min(100, self.allocation[1] + 10)
                if event.key == pygame.K_3: self.allocation[2] = min(100, self.allocation[2] + 10)

        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        prompt = self.font.render("Allocate resources (Press 1, 2, 3 to increase)", True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 150))

        for i in range(3):
            pygame.draw.rect(surface, self.theme["primary"], (440, 250 + i * 80, 400, 40), 2)
            pygame.draw.rect(surface, self.theme["accent"], (440, 250 + i * 80, int(4 * self.allocation[i]), 40))
            label = self.font.render(f"{self.targets[i]}: {self.allocation[i]}%", True, self.theme["text"])
            surface.blit(label, (860, 255 + i * 80))

        # Submit button
        pygame.draw.rect(surface, self.theme["primary"], (590, 500, 100, 50))
        sub_label = self.font.render("SUBMIT", True, self.theme["background"])
        surface.blit(sub_label, (640 - sub_label.get_width()//2, 510))
