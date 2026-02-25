import pygame
import json
import os
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
        self.scenario = self._load_scenario()

    def _load_scenario(self):
        path = os.path.join("trajectory", "data", "challenges.json")
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            data = json.load(f)

        key = f"{self.config.pillar}/{self.config.career}"
        challenge_type = self.__class__.__name__.replace("Challenge", "")
        # convert CamelCase to Space Case
        import re
        challenge_type = re.sub(r'(?<!^)(?=[A-Z])', ' ', challenge_type)

        scenarios = data.get(key, {}).get(challenge_type, [])
        if scenarios:
            return self.rng.choice(scenarios)
        return None

    @abstractmethod
    def update(self, events: List[pygame.event.Event]) -> Optional[ChallengeResult]:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass

    def get_elapsed_ms(self) -> int:
        return pygame.time.get_ticks() - self.start_time
