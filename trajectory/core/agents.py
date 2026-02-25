import numpy as np
from typing import List, Dict
from trajectory.core.world_rng import WorldRNG

STATES = ["dormant", "active", "stressed", "hostile", "cooperative"]
STATE_INDEX = {state: i for i, state in enumerate(STATES)}

# Base transition matrices for different archetypes
BASE_MATRICES = {
    "authority": np.array([
        [0.7, 0.2, 0.05, 0.0, 0.05],
        [0.1, 0.6, 0.2, 0.05, 0.05],
        [0.05, 0.1, 0.5, 0.3, 0.05],
        [0.0, 0.05, 0.2, 0.7, 0.05],
        [0.2, 0.1, 0.1, 0.0, 0.6]
    ]),
    "competitor": np.array([
        [0.6, 0.3,  0.05, 0.05, 0.0 ],
        [0.2, 0.4,  0.2,  0.1,  0.1 ],
        [0.1, 0.2,  0.3,  0.3,  0.1 ],
        [0.05,0.1,  0.2,  0.55, 0.1 ],
        [0.3, 0.3,  0.1,  0.0,  0.3 ]
    ]),
    "opportunity": np.array([
        [0.8, 0.1, 0.0, 0.0, 0.1],
        [0.2, 0.5, 0.1, 0.0, 0.2],
        [0.1, 0.2, 0.4, 0.1, 0.2],
        [0.0, 0.1, 0.2, 0.6, 0.1],
        [0.1, 0.2, 0.1, 0.0, 0.6]
    ])
}

def compute_transition_matrix(archetype: str, aggression: float,
                               loyalty: float, world_pressure: float) -> np.ndarray:
    base = BASE_MATRICES.get(archetype, BASE_MATRICES["competitor"]).copy()

    # Aggression shifts mass toward hostile/stressed states
    hostile_idx = STATE_INDEX["hostile"]
    stressed_idx = STATE_INDEX["stressed"]
    dormant_idx = STATE_INDEX["dormant"]

    base[:, hostile_idx] += aggression * 0.15
    base[:, stressed_idx] += world_pressure * 0.2
    base[:, dormant_idx] -= (aggression * 0.1 + world_pressure * 0.1)

    # Renormalize
    base = np.clip(base, 0, 1)
    base = base / base.sum(axis=1, keepdims=True)

    return base

class AgentState:
    def __init__(self, config):
        self.config = config
        self.current_state = "active"
        self.relationship = config.relationship # -1 to 1

    def update_state(self, world_pressure: float, rng: WorldRNG) -> str:
        matrix = compute_transition_matrix(
            self.config.archetype,
            self.config.aggression,
            self.config.loyalty,
            world_pressure
        )
        current_idx = STATE_INDEX[self.current_state]
        transition_probs = matrix[current_idx]

        new_state_idx = rng.choice(len(STATES), p=transition_probs)
        self.current_state = STATES[new_state_idx]
        return self.current_state

    def update_relationship(self, delta: float):
        alpha = 0.15
        decay = 0.05 * (1.0 - self.config.loyalty)
        self.relationship = float(np.clip(self.relationship + alpha * delta - decay * self.relationship, -1.0, 1.0))
