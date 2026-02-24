import numpy as np

class WorldRNG:
    """Single seeded RNG object for entire world generation.
    All draws happen through this object in fixed documented order.
    NEVER use random.random() or np.random.* global functions."""

    def __init__(self, seed: int):
        self.rng = np.random.default_rng(seed)
        self.draw_count = 0  # auditable

    def uniform(self, low=0.0, high=1.0) -> float:
        self.draw_count += 1
        return float(self.rng.uniform(low, high))

    def integers(self, low: int, high: int) -> int:
        self.draw_count += 1
        return int(self.rng.integers(low, high))

    def choice(self, items: list, p: list = None):
        self.draw_count += 1
        return self.rng.choice(items, p=p)

    def normal(self, mean=0.0, std=1.0) -> float:
        self.draw_count += 1
        return float(self.rng.normal(mean, std))
