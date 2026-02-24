import pygame
import time

class WorldBootScreen:
    def __init__(self, config):
        self.config = config
        self.font = pygame.font.SysFont("Arial", 28)
        self.start_time = time.time()
        self.duration = 2.0

    def update(self, events):
        if time.time() - self.start_time > self.duration:
            return True
        return False

    def draw(self, surface):
        surface.fill((10, 18, 30))

        # Display ML quality score
        quality_text = self.font.render(f"SEED QUALITY: {self.config.quality_score:.2f}", True, (41, 182, 246))
        surface.blit(quality_text, (640 - quality_text.get_width()//2, 300))

        conf_text = self.font.render(f"ML CONFIDENCE: {self.config.quality_confidence * 100:.1f}%", True, (129, 212, 250))
        surface.blit(conf_text, (640 - conf_text.get_width()//2, 350))

        loading_text = self.font.render("INITIALIZING WORLD ENGINE...", True, (255, 255, 255))
        surface.blit(loading_text, (640 - loading_text.get_width()//2, 500))

        # Simple progress bar
        progress = (time.time() - self.start_time) / self.duration
        pygame.draw.rect(surface, (41, 182, 246), (440, 550, int(400 * progress), 10))
