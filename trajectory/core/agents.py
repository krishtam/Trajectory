import numpy as np
from typing import List, Dict
from trajectory.core.world_rng import WorldRNG

STATES = ["dormant", "active", "stressed", "hostile", "cooperative"]
STATE_INDEX = {state: i for i, state in enumerate(STATES)}

BASE_MATRICES = {
    "competitor": np.array([
        [0.6, 0.3,  0.05, 0.05, 0.0 ],
        [0.2, 0.4,  0.2,  0.1,  0.1 ],
        [0.1, 0.2,  0.3,  0.3,  0.1 ],
        [0.05,0.1,  0.2,  0.55, 0.1 ],
        [0.3, 0.3,  0.1,  0.0,  0.3 ]
    ]),
}

# Fill other archetypes with the same base for now, can be tuned later
for arch in ["authority", "gatekeeper", "opportunity", "dependency", "adversary"]:
    if arch not in BASE_MATRICES:
        BASE_MATRICES[arch] = BASE_MATRICES["competitor"].copy()

def compute_transition_matrix(archetype: str, aggression: float,
                               loyalty: float, world_pressure: float) -> np.ndarray:
    base = BASE_MATRICES.get(archetype, BASE_MATRICES["competitor"]).copy()

    # Aggression shifts probability mass toward hostile states
    hostile_idx = STATE_INDEX["hostile"]
    dormant_idx = STATE_INDEX["dormant"]
    shift = aggression * 0.15
    base[:, hostile_idx] += shift
    base[:, dormant_idx] -= shift

    # World pressure amplifies stress transitions
    stress_idx = STATE_INDEX["stressed"]
    base[:, stress_idx] += world_pressure * 0.1

    # Renormalize rows to sum to 1
    base = np.clip(base, 0, 1)
    base = base / base.sum(axis=1, keepdims=True)

    return base

class AgentState:
    def __init__(self, config):
        self.config = config
        self.current_state = "active"
        self.relationship = config.relationship

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
        """
        R_{t+1} = R_t + α × Δ_decision - β × R_t × decay_rate
        """
        alpha = 0.1
        beta = 0.05 # placeholder for base decay
        decay_rate = 1.0 - self.config.loyalty

        self.relationship = self.relationship + alpha * delta - beta * self.relationship * decay_rate
        self.relationship = float(np.clip(self.relationship, -1.0, 1.0))
