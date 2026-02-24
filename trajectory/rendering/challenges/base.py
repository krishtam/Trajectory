import pygame
from abc import ABC, abstractmethod
from typing import List, Optional

class ChallengeResult:
    def __init__(self, performance: float, time_taken_ms: int):
        self.performance = performance
        self.time_taken_ms = time_taken_ms

class Challenge(ABC):
    def __init__(self, config, theme, rng):
        self.config = config
        self.theme = theme
        self.rng = rng
        self.start_time = pygame.time.get_ticks()
        self.result: Optional[ChallengeResult] = None

    @abstractmethod
    def update(self, events: List[pygame.event.Event]) -> Optional[ChallengeResult]:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass

    def get_elapsed_ms(self) -> int:
        return pygame.time.get_ticks() - self.start_time
