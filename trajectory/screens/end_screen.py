import pygame

class EndScreen:
    def __init__(self, won, state):
        self.won = won
        self.state = state
        self.font = pygame.font.SysFont("Arial", 48)
        self.small_font = pygame.font.SysFont("Arial", 24)

    def update(self, events):
        for event in events:
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                return True
        return False

    def draw(self, surface):
        surface.fill((10, 15, 20))

        result_text = "CAREER SUCCESS!" if self.won else "CAREER STALLED"
        color = (100, 255, 100) if self.won else (255, 100, 100)

        text = self.font.render(result_text, True, color)
        surface.blit(text, (640 - text.get_width()//2, 200))

        score_text = self.small_font.render(f"Final {self.state.config.win_condition.metric}: {int(self.state.resource)}", True, (255, 255, 255))
        surface.blit(score_text, (640 - score_text.get_width()//2, 300))

        seed_text = self.small_font.render(f"World Seed: {self.state.config.seed}", True, (150, 150, 150))
        surface.blit(seed_text, (640 - seed_text.get_width()//2, 350))

        hint = self.small_font.render("Press any key to restart", True, (100, 100, 100))
        surface.blit(hint, (640 - hint.get_width()//2, 500))
