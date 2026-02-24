import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult

class NegotiationChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        self.font = pygame.font.SysFont("Arial", 22)
        self.player_offer = 50
        self.agent_offer = 100
        self.round = 1
        self.max_rounds = 3
        self.agent_reserve = 70

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if pygame.Rect(440, 450, 400, 20).collidepoint(x, y):
                    self.player_offer = (x - 440) / 400 * 100
                if pygame.Rect(590, 520, 100, 50).collidepoint(x, y):
                    # Submit offer
                    if self.player_offer >= self.agent_reserve:
                        return ChallengeResult(1.0, self.get_elapsed_ms())
                    else:
                        self.round += 1
                        self.agent_reserve -= 5 # Agent concedes slightly
                        if self.round > self.max_rounds:
                            return ChallengeResult(0.3, self.get_elapsed_ms())
        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        prompt = self.font.render(f"Negotiation Round {self.round}/{self.max_rounds}", True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 150))

        # ZOPA Bar
        pygame.draw.rect(surface, (50, 50, 50), (440, 300, 400, 40))
        pygame.draw.rect(surface, self.theme["primary"], (440 + int(self.agent_reserve * 4), 300, 400 - int(self.agent_reserve * 4), 40))

        # Slider
        pygame.draw.rect(surface, (200, 200, 200), (440, 450, 400, 20))
        pygame.draw.circle(surface, self.theme["accent"], (440 + int(self.player_offer * 4), 460), 15)

        label = self.font.render(f"Your Offer: {int(self.player_offer)}", True, self.theme["text"])
        surface.blit(label, (640 - label.get_width()//2, 400))

        pygame.draw.rect(surface, self.theme["primary"], (590, 520, 100, 50))
        sub_label = self.font.render("OFFER", True, self.theme["background"])
        surface.blit(sub_label, (640 - sub_label.get_width()//2, 535))
