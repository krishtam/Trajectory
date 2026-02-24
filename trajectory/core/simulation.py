from dataclasses import dataclass
from typing import List, Dict, Any
from trajectory.core.seed_engine import WorldConfig, WinConditionConfig
from trajectory.core.agents import AgentState

class WorldState:
    def __init__(self, config: WorldConfig):
        self.resource = config.player.starting_resource
        self.reputation = config.player.reputation
        self.pressure_level = 0.5
        self.cycle = 0
        self.metrics = {
            "output": 0.0,
            "system_health": 1.0,
            "network_size": float(config.player.network_size)
        }
        self.events_fired = []
        self.agents = [AgentState(a) for a in config.agents]

    def to_evidence_dict(self) -> Dict[str, int]:
        """Convert world state to evidence for Bayesian network."""
        economy_state = 1 # Default stable
        if self.pressure_level > 0.8: economy_state = 0 # Contraction
        elif self.pressure_level < 0.2: economy_state = 2 # Expansion

        # Player performance based on output vs cycle
        performance = 1 if self.metrics["output"] >= self.cycle * 15 else 0

        return {
            "EconomyState": economy_state,
            "PlayerPerformance": performance,
        }

    def apply_event(self, event_id: str, config: WorldConfig):
        self.events_fired.append(event_id)
        if event_id == "MarketShock":
            self.resource *= 0.8
            self.pressure_level = min(1.0, self.pressure_level + 0.2)
        elif event_id == "OpportunityWindow":
            self.reputation = min(1.0, self.reputation + 0.1)
        elif event_id == "FundingEvent":
            self.resource += 20000.0
        elif event_id == "CompetitorAdvance":
            self.reputation = max(0.0, self.reputation - 0.05)
            self.pressure_level = min(1.0, self.pressure_level + 0.1)

    def apply_challenge_outcome(self, performance: float, config: WorldConfig):
        # Update metrics based on challenge performance
        self.metrics["output"] += performance * 10.0
        self.resource += performance * 25000.0
        self.reputation = min(1.0, self.reputation + (performance - 0.5) * 0.1)
        self.pressure_level = max(0.0, self.pressure_level - (performance - 0.5) * 0.2)

    def check_win(self, win_config: WinConditionConfig) -> bool:
        if win_config.type == "threshold":
            return self.resource >= win_config.target_value
        return False

    def check_lose(self, win_config: WinConditionConfig) -> bool:
        if self.cycle >= win_config.time_limit_cycles:
            return not self.check_win(win_config)
        if self.resource <= 0:
            return True
        return False
