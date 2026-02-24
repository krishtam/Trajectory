import pygame
from trajectory.rendering.challenges.base import Challenge, ChallengeResult

class SequenceJudgmentChallenge(Challenge):
    def __init__(self, config, theme, rng):
        super().__init__(config, theme, rng)
        self.font = pygame.font.SysFont("Arial", 20)
        self.steps = self._get_steps(config.career)
        self.correct_order = list(range(len(self.steps)))
        self.current_order = list(range(len(self.steps)))
        rng.rng.shuffle(self.current_order)
        self.selected_idx = None

    def _get_steps(self, career):
        if career == "Chemist":
            return ["Prepare Reagents", "Initiate Synthesis", "Monitor Temperature", "Filter Precipitate", "Analyze Purity"]
        elif career == "Trader":
            return ["Identify Opportunity", "Calculate Risk", "Execute Entry", "Monitor Position", "Exit Strategy"]
        elif career == "Entrepreneur":
            return ["Define MVP", "Build Prototype", "User Testing", "Iterate Design", "Full Launch"]
        return ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"]

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(len(self.steps)):
                    rect = pygame.Rect(440, 150 + i * 60, 400, 50)
                    if rect.collidepoint(x, y):
                        if self.selected_idx is None:
                            self.selected_idx = i
                        else:
                            # Swap
                            self.current_order[self.selected_idx], self.current_order[i] = \
                                self.current_order[i], self.current_order[self.selected_idx]
                            self.selected_idx = None

                if pygame.Rect(590, 550, 100, 50).collidepoint(x, y):
                    # Submit
                    correct_count = sum(1 for i, v in enumerate(self.current_order) if v == self.correct_order[i])
                    performance = correct_count / len(self.steps)
                    return ChallengeResult(performance, self.get_elapsed_ms())
        return None

    def draw(self, surface):
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        prompt = self.font.render("Sort in correct sequence (Click two to swap)", True, (255, 255, 255))
        surface.blit(prompt, (640 - prompt.get_width()//2, 100))

        for i, idx in enumerate(self.current_order):
            rect = pygame.Rect(440, 150 + i * 60, 400, 50)
            color = self.theme["primary"]
            if self.selected_idx == i:
                color = self.theme["accent"]
            pygame.draw.rect(surface, color, rect, 2)
            label = self.font.render(self.steps[idx], True, self.theme["text"])
            surface.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

        pygame.draw.rect(surface, self.theme["primary"], (590, 550, 100, 50))
        sub_label = self.font.render("DONE", True, self.theme["background"])
        surface.blit(sub_label, (640 - sub_label.get_width()//2, 565))
