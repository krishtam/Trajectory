import pygame
from trajectory.rendering.font_utils import get_font

class EndScreen:
    def __init__(self, won, state):
        self.won = won
        self.state = state
        self.font = get_font(48, bold=True)
        self.small_font = get_font(20)

    def update(self, events):
        for event in events:
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                return True
        return False

    def draw(self, surface):
        surface.fill((5, 10, 15))

        # Glow Effect
        center = (640, 360)
        color = (20, 60, 40) if self.won else (60, 20, 20)
        pygame.draw.circle(surface, color, center, 200)

        result_text = "SIMULATION SUCCESSFUL" if self.won else "SIMULATION TERMINATED"
        res_color = (100, 255, 150) if self.won else (255, 100, 100)

        text = self.font.render(result_text, True, res_color)
        surface.blit(text, (640 - text.get_width()//2, 220))

        sub_text = "CAREER TARGETS REACHED" if self.won else "RESOURCE DEPLETION / CYCLE LIMIT"
        sub = self.small_font.render(sub_text, True, (200, 200, 200))
        surface.blit(sub, (640 - sub.get_width()//2, 285))

        # Final Stats
        stat_rect = pygame.Rect(440, 350, 400, 120)
        pygame.draw.rect(surface, (15, 25, 40), stat_rect, border_radius=10)
        pygame.draw.rect(surface, res_color, stat_rect, 2, border_radius=10)

        m_label = self.small_font.render(f"FINAL {self.state.config.win_condition.metric.upper()}:", True, (150, 150, 200))
        surface.blit(m_label, (460, 370))
        m_val = get_font(24, bold=True).render(f"{int(self.state.resource):,}", True, (255, 255, 255))
        surface.blit(m_val, (460, 395))

        s_label = self.small_font.render(f"WORLD SEED:", True, (150, 150, 200))
        surface.blit(s_label, (460, 430))
        s_val = self.small_font.render(str(self.state.config.seed), True, (200, 200, 200))
        surface.blit(s_val, (580, 430))

        hint = self.small_font.render("PRESS ANY KEY TO RE-INITIALIZE", True, (100, 100, 120))
        surface.blit(hint, (640 - hint.get_width()//2, 600))
