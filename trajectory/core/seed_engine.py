from dataclasses import dataclass, field
from typing import List, Optional
from trajectory.core.world_rng import WorldRNG
from trajectory.core.career_taxonomy import CAREER_TAXONOMY, resolve_pillar

@dataclass
class EconomyConfig:
    volatility: float            # U(0.1, 0.9) — market/sector instability
    trend: str                   # choice(["expansion","stable","contraction"])
    cycle_position: float        # U(0, 1) — position in business cycle
    sector_health: float         # U(0.2, 1.0) — overall sector performance
    disruption_risk: float       # U(0, 0.8) — technological/competitive disruption
    regulatory_pressure: float   # U(0, 0.7) — regulatory environment intensity

@dataclass
class PlayerConfig:
    starting_resource: float     # pillar-specific primary resource (capital, runway, etc.)
    skill_level: float           # U(0.3, 0.9) — starting competency
    network_size: int            # randint(3, 20) — initial relationship count
    risk_modifier: float         # U(0.7, 1.3) — multiplier on challenge difficulty
    reputation: float            # U(0.2, 0.8) — starting industry reputation

@dataclass
class AgentConfig:
    archetype: str               # see Agent Archetypes below
    name_key: str                # key into names table → display name
    aggression: float            # U(0, 1) — how actively agent acts against player
    loyalty: float               # U(0, 1) — stability of relationship with player
    activity_rate: float         # U(0.1, 0.9) — frequency of agent actions
    relationship: float          # U(-1, 1) — current relationship value
    behavior_vector: List[float] # 8-dim feature vector for ML behavior model

@dataclass
class EventPoolConfig:
    event_ids: List[str]             # references to events.json template library
    base_probabilities: List[float]  # prior P(event fires) per cycle
    correlation_matrix: List[List[float]]  # for Bayesian network CPDs
    trigger_thresholds: List[float]  # world state value that amplifies probability

@dataclass
class ChallengeConfig:
    signal_noise_level: float       # U(0.2, 0.8) — fraction of data redacted
    allocation_tightness: float     # U(0.6, 1.2) — demand/supply ratio of resource units
    sequence_scramble_rate: float   # U(0.4, 0.9) — fraction of steps out of order
    pressure_window_ms: int         # randint(10000, 25000) — ms for pressure response
    negotiation_hardness: float     # U(0.3, 0.9) — agent concession rate

@dataclass
class WinConditionConfig:
    type: str                    # "threshold" | "survival" | "relationship" | "output"
    metric: str                  # pillar-specific metric e.g. "portfolio_value"
    target_value: float          # value to reach
    time_limit_cycles: int       # max cycles before forced resolution (4–6)

@dataclass
class WorldConfig:
    seed: int
    pillar: str
    career: str
    career_stage: str
    economy: EconomyConfig
    player: PlayerConfig
    agents: List[AgentConfig]
    events: EventPoolConfig
    challenges: ChallengeConfig
    win_condition: WinConditionConfig
    quality_score: float = 0.0
    quality_confidence: float = 0.0

    def to_vector(self) -> List[float]:
        """Flatten to feature vector for XGBoost input."""
        trend_enc = {"expansion": 1.0, "stable": 0.5, "contraction": 0.0}
        return [
            self.economy.volatility,
            trend_enc[self.economy.trend],
            self.economy.cycle_position,
            self.economy.sector_health,
            self.economy.disruption_risk,
            self.economy.regulatory_pressure,
            self.player.skill_level,
            self.player.risk_modifier,
            self.player.reputation,
            float(self.player.network_size) / 20.0,
            float(len(self.agents)),
            float(sum(a.aggression for a in self.agents)) / len(self.agents) if self.agents else 0,
            float(max(a.aggression for a in self.agents)) if self.agents else 0,
            float(sum(a.loyalty for a in self.agents)) / len(self.agents) if self.agents else 0,
            float(sum(1 for a in self.agents if a.archetype == "opportunity")),
            float(sum(1 for a in self.agents if a.archetype in ["adversary","competitor"])),
            self.challenges.signal_noise_level,
            self.challenges.allocation_tightness,
            self.challenges.sequence_scramble_rate,
            float(self.challenges.pressure_window_ms) / 25000.0,
            self.challenges.negotiation_hardness,
            self.win_condition.target_value / 1000000.0,
            float(self.win_condition.time_limit_cycles),
        ]  # 23 features total

    @staticmethod
    def from_seed(seed: int, pillar: str, career: str) -> 'WorldConfig':
        rng = WorldRNG(seed)

        # Draw 1-6: EconomyConfig
        economy = EconomyConfig(
            volatility=rng.uniform(0.1, 0.9),
            trend=rng.choice(["expansion", "stable", "contraction"]),
            cycle_position=rng.uniform(0, 1),
            sector_health=rng.uniform(0.2, 1.0),
            disruption_risk=rng.uniform(0, 0.8),
            regulatory_pressure=rng.uniform(0, 0.7)
        )

        # Draw 7-8: PlayerConfig (starting_resource, skill_level)
        starting_resource = 100000.0
        skill_level = rng.uniform(0.3, 0.9)

        # Draw 9-11: PlayerConfig (network_size, risk_modifier, reputation)
        network_size = rng.integers(3, 20)
        risk_modifier = rng.uniform(0.7, 1.3)
        reputation = rng.uniform(0.2, 0.8)

        player = PlayerConfig(
            starting_resource=starting_resource,
            skill_level=skill_level,
            network_size=network_size,
            risk_modifier=risk_modifier,
            reputation=reputation
        )

        # Draw 12: Agent count n (3-8)
        n_agents = rng.integers(3, 8)
        agents = []
        for i in range(n_agents):
            # Draw 13-18: Agent i attributes (6 draws)
            archetypes = ["authority", "competitor", "gatekeeper", "opportunity", "dependency", "adversary"]
            agents.append(AgentConfig(
                archetype=rng.choice(archetypes),
                name_key=f"agent_{i}",
                aggression=rng.uniform(0, 1),
                loyalty=rng.uniform(0, 1),
                activity_rate=rng.uniform(0.1, 0.9),
                relationship=rng.uniform(-0.2, 0.2),
                behavior_vector=[rng.uniform(0, 1) for _ in range(8)]
            ))

        # Events
        event_pool_size = rng.integers(5, 15)
        event_ids = [f"event_{j}" for j in range(event_pool_size)] # Placeholder
        base_probabilities = [rng.uniform(0.05, 0.2) for _ in range(event_pool_size)]

        events = EventPoolConfig(
            event_ids=event_ids,
            base_probabilities=base_probabilities,
            correlation_matrix=[],
            trigger_thresholds=[rng.uniform(0.3, 0.7) for _ in range(event_pool_size)]
        )

        # Challenges
        challenges = ChallengeConfig(
            signal_noise_level=rng.uniform(0.2, 0.8),
            allocation_tightness=rng.uniform(0.6, 1.2),
            sequence_scramble_rate=rng.uniform(0.4, 0.9),
            pressure_window_ms=rng.integers(10000, 25000),
            negotiation_hardness=rng.uniform(0.3, 0.9)
        )

        # Win condition
        win_condition = WinConditionConfig(
            type="threshold",
            metric=CAREER_TAXONOMY[pillar]["currency_label"],
            target_value=starting_resource * 2.2,
            time_limit_cycles=rng.integers(6, 9)
        )

        # Extra draws for Scene Objects as per Part 4
        scene_object_count = rng.integers(5, 12)
        for _ in range(scene_object_count):
            rng.uniform() # position x
            rng.uniform() # position y
            rng.uniform() # scale
            rng.uniform() # alpha

        return WorldConfig(
            seed=seed,
            pillar=pillar,
            career=career,
            career_stage="Junior",
            economy=economy,
            player=player,
            agents=agents,
            events=events,
            challenges=challenges,
            win_condition=win_condition
        )

CURATED_SEEDS = {
    ("Expert",    "Chemist"):     4821,
    ("Expert",    "Doctor"):      19203,
    ("Expert",    "Lawyer"):      7741,
    ("Allocator", "Trader"):      58821,
    ("Builder",   "Entrepreneur"):14492,
    ("Connector", "Sales"):       28841,
    ("Operator",  "Manager"):     73918,
    ("Creator",   "Designer"):    82013,
}
