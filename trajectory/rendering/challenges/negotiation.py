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
            self.prompt_text = "Establish professional terms."
            self.agent_role = "Partner"
            self.subject = "Agreement"

        self.font = get_font(18)
        self.header_font = get_font(28, bold=True)
        self.player_offer = 40
        self.agent_offer = 100
        self.round = 1
        self.max_rounds = 4
        self.agent_reserve = rng.integers(65, 90)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if pygame.Rect(440, 450, 400, 30).collidepoint(x, y):
                    self.player_offer = (x - 440) / 400 * 100
                if pygame.Rect(590, 520, 100, 50).collidepoint(x, y):
                    if self.player_offer >= self.agent_reserve:
                        # Success
                        return ChallengeResult(1.0 - (self.round-1)*0.15, self.get_elapsed_ms())
                    else:
                        # Agent concession
                        self.round += 1
                        self.agent_reserve -= rng_logic(self.rng)
                        if self.round > self.max_rounds:
                            return ChallengeResult(0.2, self.get_elapsed_ms())
        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((10, 20, 30, 245))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, self.theme["primary"], (340, 80, 600, 580), 2, border_radius=15)

        title = self.header_font.render(f"NEGOTIATION: {self.agent_role.upper()}", True, self.theme["accent"])
        surface.blit(title, (640 - title.get_width()//2, 110))

        prompt = self.font.render(self.prompt_text, True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 160))

        # Agreement Zone
        pygame.draw.rect(surface, (30, 35, 45), (440, 280, 400, 60), border_radius=10)
        zopa_x = 440 + int(self.agent_reserve * 4)
        pygame.draw.rect(surface, (50, 150, 80), (zopa_x, 280, 440 + 400 - zopa_x, 60), border_radius=10)

        z_label = self.font.render("ZOPA (AGREEMENT ZONE)", True, (200, 255, 200))
        surface.blit(z_label, (640 - z_label.get_width()//2, 350))

        # Slider UI
        pygame.draw.rect(surface, (60, 65, 80), (440, 460, 400, 15), border_radius=5)
        handle_x = 440 + int(self.player_offer * 4)
        pygame.draw.circle(surface, self.theme["accent"], (handle_x, 467), 15)
        pygame.draw.circle(surface, (255, 255, 255), (handle_x, 467), 17, 2)

        offer_val = int(self.player_offer)
        v_label = get_font(24, bold=True).render(f"YOUR OFFER: {offer_val} UNITS", True, (255, 255, 255))
        surface.blit(v_label, (640 - v_label.get_width()//2, 410))

        # Submit Button
        pygame.draw.rect(surface, self.theme["primary"], (590, 520, 100, 50), border_radius=10)
        btn_txt = get_font(16, bold=True).render("OFFER", True, self.theme["background"])
        surface.blit(btn_txt, (640 - btn_txt.get_width()//2, 532))

        r_label = self.font.render(f"ROUND {self.round} / {self.max_rounds}", True, (150, 150, 170))
        surface.blit(r_label, (640 - r_label.get_width()//2, 610))

def rng_logic(rng):
    return rng.integers(3, 8)
