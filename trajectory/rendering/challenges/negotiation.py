import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult
from trajectory.rendering.font_utils import get_font

class NegotiationChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        if self.scenario:
            self.prompt_text = self.scenario["prompt"]
            self.agent_role = self.scenario["agent_role"]
            self.subject = self.scenario["subject"]
        else:
            self.prompt_text = "Negotiate terms."
            self.agent_role = "Partner"
            self.subject = "Contract"

        self.font = get_font(20)
        self.header_font = get_font(28, bold=True)
        self.player_offer = 30
        self.agent_offer = 100
        self.round = 1
        self.max_rounds = 4
        self.agent_reserve = rng.integers(60, 85)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if pygame.Rect(440, 450, 400, 30).collidepoint(x, y):
                    self.player_offer = (x - 440) / 400 * 100
                if pygame.Rect(590, 520, 100, 50).collidepoint(x, y):
                    if self.player_offer >= self.agent_reserve:
                        return ChallengeResult(1.0 - (self.round-1)*0.1, self.get_elapsed_ms())
                    else:
                        self.round += 1
                        self.agent_reserve -= 5
                        if self.round > self.max_rounds:
                            return ChallengeResult(0.2, self.get_elapsed_ms())
        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((10, 20, 30, 240))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, self.theme["primary"], (340, 80, 600, 560), 2)

        title = self.header_font.render(f"NEGOTIATION: {self.agent_role}", True, self.theme["primary"])
        surface.blit(title, (640 - title.get_width()//2, 110))

        prompt = self.font.render(self.prompt_text, True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 160))

        # ZOPA Bar
        pygame.draw.rect(surface, (40, 40, 40), (440, 300, 400, 50))
        # Agent reserve to 100 is the ZOPA
        zopa_x = 440 + int(self.agent_reserve * 4)
        pygame.draw.rect(surface, (0, 150, 0), (zopa_x, 300, 440 + 400 - zopa_x, 50))

        zopa_label = self.font.render("AGREEMENT ZONE", True, (200, 255, 200))
        surface.blit(zopa_label, (640 - zopa_label.get_width()//2, 360))

        # Slider
        pygame.draw.rect(surface, (100, 100, 100), (440, 450, 400, 30))
        handle_x = 440 + int(self.player_offer * 4)
        pygame.draw.rect(surface, self.theme["accent"], (handle_x - 5, 445, 10, 40))

        offer_text = self.font.render(f"YOUR OFFER: {int(self.player_offer)} units", True, self.theme["text"])
        surface.blit(offer_text, (640 - offer_text.get_width()//2, 410))

        pygame.draw.rect(surface, self.theme["primary"], (590, 520, 100, 50))
        btn_text = self.font.render("SUBMIT", True, self.theme["background"])
        surface.blit(btn_text, (640 - btn_text.get_width()//2, 535))

        round_text = self.font.render(f"Round {self.round} / {self.max_rounds}", True, (150, 150, 150))
        surface.blit(round_text, (640 - round_text.get_width()//2, 600))
