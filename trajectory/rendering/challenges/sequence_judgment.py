import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult
from trajectory.rendering.font_utils import get_font

class SequenceJudgmentChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        if self.scenario:
            self.prompt_text = self.scenario["prompt"]
            self.steps = self.scenario["steps"]
        else:
            self.prompt_text = "Standardize the workflow sequence."
            self.steps = ["Step A", "Step B", "Step C", "Step D"]

        self.font = get_font(16)
        self.header_font = get_font(28, bold=True)
        self.correct_order = list(range(len(self.steps)))
        self.current_order = list(range(len(self.steps)))
        rng.rng.shuffle(self.current_order)
        self.selected_idx = None

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(len(self.steps)):
                    rect = pygame.Rect(440, 220 + i * 65, 400, 55)
                    if rect.collidepoint(x, y):
                        if self.selected_idx is None:
                            self.selected_idx = i
                        else:
                            self.current_order[self.selected_idx], self.current_order[i] = \
                                self.current_order[i], self.current_order[self.selected_idx]
                            self.selected_idx = None

                if pygame.Rect(590, 580, 100, 50).collidepoint(x, y):
                    correct_count = sum(1 for i, v in enumerate(self.current_order) if v == self.correct_order[i])
                    performance = correct_count / len(self.steps)
                    return ChallengeResult(performance, self.get_elapsed_ms())
        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((10, 20, 30, 240))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, self.theme["primary"], (340, 100, 600, 550), 2, border_radius=15)

        title = self.header_font.render("SOP OPTIMIZATION", True, self.theme["accent"])
        surface.blit(title, (640 - title.get_width()//2, 130))

        prompt = self.font.render(self.prompt_text, True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 175))

        hint = self.font.render("(CLICK TWO STEPS TO SWAP POSITION)", True, (150, 150, 150))
        surface.blit(hint, (640 - hint.get_width()//2, 200))

        for i, idx in enumerate(self.current_order):
            rect = pygame.Rect(440, 230 + i * 65, 400, 55)
            color = (40, 45, 60)
            border_color = self.theme["primary"]
            if self.selected_idx == i:
                color = self.theme["accent"]
                border_color = (255, 255, 255)

            pygame.draw.rect(surface, color, rect, border_radius=10)
            pygame.draw.rect(surface, border_color, rect, 2, border_radius=10)

            label = self.font.render(f"{i+1}. {self.steps[idx].upper()}", True, (255, 255, 255) if self.selected_idx != i else (0,0,0))
            surface.blit(label, (rect.left + 20, rect.centery - label.get_height()//2))

        pygame.draw.rect(surface, self.theme["primary"], (590, 580, 100, 50), border_radius=10)
        btn_txt = get_font(16, bold=True).render("VALIDATE", True, self.theme["background"])
        surface.blit(btn_txt, (640 - btn_txt.get_width()//2, 592))
