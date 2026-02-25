from dataclasses import dataclass
from typing import List, Dict, Any
from trajectory.core.seed_engine import WorldConfig, WinConditionConfig
from trajectory.core.agents import AgentState

class WorldState:
    def __init__(self, config: WorldConfig):
        self.config = config
        self.resource = config.player.starting_resource
        self.reputation = config.player.reputation
        self.pressure_level = 0.5
        self.cycle = 0
        self.max_cycles = 5 # 5-day story
        self.metrics = {
            "output": 0.0,
            "success_rate": 0.0,
            "complications": 0,
            "cases_completed": 0,
            "p_and_l": 0.0,
            "portfolio_value": config.player.starting_resource
        }
        self.events_fired = []
        self.agents = [AgentState(a) for a in config.agents]
        self.difficulty_adj = [0.0] * 5
        self.narrative_log = []

    def to_evidence_dict(self) -> Dict[str, int]:
        economy_state = 1
        if self.pressure_level > 0.8: economy_state = 0
        elif self.pressure_level < 0.2: economy_state = 2

        performance = 1 if self.metrics["output"] >= self.cycle * 15 else 0

        return {
            "EconomyState": economy_state,
            "PlayerPerformance": performance,
        }

    def apply_event(self, event_id: str, config: WorldConfig):
        self.events_fired.append(event_id)
        if event_id == "MarketShock":
            self.resource *= 0.85
            self.pressure_level = min(1.0, self.pressure_level + 0.25)
        elif event_id == "SurgicalComplication":
            self.reputation = max(0.0, self.reputation - 0.15)
            self.pressure_level = min(1.0, self.pressure_level + 0.3)
        elif event_id == "AdminPressure":
            self.pressure_level = min(1.0, self.pressure_level + 0.15)
        elif event_id == "MarketRally":
            self.resource *= 1.15
            self.pressure_level = max(0.0, self.pressure_level - 0.1)

    def apply_challenge_outcome(self, performance: float, config: WorldConfig):
        # Professional outcome logic
        if config.pillar == "Expert": # Surgeon
            self.metrics["cases_completed"] += 1
            if performance > 0.6:
                self.metrics["success_rate"] = (self.metrics["success_rate"] * (self.metrics["cases_completed"]-1) + 1.0) / self.metrics["cases_completed"]
                self.reputation = min(1.0, self.reputation + 0.05)
            else:
                self.metrics["complications"] += 1
                self.metrics["success_rate"] = (self.metrics["success_rate"] * (self.metrics["cases_completed"]-1) + 0.0) / self.metrics["cases_completed"]
                self.reputation = max(0.0, self.reputation - 0.1)

            self.resource = self.reputation * 100000.0 # Rep is the currency

        elif config.pillar == "Allocator": # Trader
            gain = (performance - 0.5) * 0.1 * self.resource
            self.resource += gain
            self.metrics["p_and_l"] += gain
            self.metrics["portfolio_value"] = self.resource
            self.reputation = min(1.0, self.reputation + gain / 50000.0)

        self.pressure_level = max(0.0, min(1.0, self.pressure_level + (0.5 - performance) * 0.4))

    def check_win(self) -> bool:
        if self.cycle >= self.max_cycles:
            if self.config.pillar == "Expert":
                return self.reputation > 0.7
            else:
                return self.resource > self.config.player.starting_resource * 1.1
        return False

    def check_lose(self) -> bool:
        if self.resource <= 0 or self.reputation <= 0.1:
            return True
        return False
