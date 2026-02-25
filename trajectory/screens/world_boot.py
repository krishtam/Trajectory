import pygame
import time
from trajectory.rendering.font_utils import get_font

class WorldBootScreen:
    def __init__(self, config):
        self.config = config
        self.font = get_font(28, bold=True)
        self.small_font = get_font(16)
        self.start_time = time.time()
        self.duration = 3.0

    def update(self, events):
        if time.time() - self.start_time > self.duration:
            return True
        return False

    def draw(self, surface):
        surface.fill((5, 10, 15))

        # Background Grid
        for i in range(0, 1280, 40):
            pygame.draw.line(surface, (10, 15, 25), (i, 0), (i, 720))

        # Central Hexagon Glow
        center = (640, 360)
        pygame.draw.circle(surface, (20, 40, 60), center, 150)

        # ML Info Panel
        panel_rect = pygame.Rect(440, 280, 400, 160)
        pygame.draw.rect(surface, (15, 25, 40), panel_rect, border_radius=10)
        pygame.draw.rect(surface, (100, 200, 255), panel_rect, 2, border_radius=10)

        # Metrics
        q_label = self.small_font.render("XGBOOST_SEED_QUALITY", True, (150, 150, 200))
        surface.blit(q_label, (460, 300))
        q_val = self.font.render(f"{self.config.quality_score:.4f}", True, (255, 255, 255))
        surface.blit(q_val, (460, 320))

        c_label = self.small_font.render("MODEL_CONFIDENCE", True, (150, 150, 200))
        surface.blit(c_label, (460, 370))
        c_val = self.font.render(f"{self.config.quality_confidence * 100:.1f}%", True, (100, 255, 150))
        surface.blit(c_val, (460, 390))

        # Boot status
        status = "SYNCHRONIZING PRNG..."
        if time.time() - self.start_time > 1.0: status = "MAPPING BAYESIAN NETWORK..."
        if time.time() - self.start_time > 2.0: status = "STABILIZING WORLD STATE..."

        status_txt = self.small_font.render(status, True, (100, 200, 255))
        surface.blit(status_txt, (640 - status_txt.get_width()//2, 500))

        # Progress bar
        progress = (time.time() - self.start_time) / self.duration
        pygame.draw.rect(surface, (30, 40, 60), (440, 530, 400, 10), border_radius=5)
        pygame.draw.rect(surface, (100, 200, 255), (440, 530, int(400 * progress), 10), border_radius=5)
