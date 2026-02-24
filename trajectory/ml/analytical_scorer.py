import numpy as np
from trajectory.core.seed_engine import WorldConfig
from trajectory.ml.headless_simulate import headless_simulate

def gaussian_score(x: float, mean: float, std: float) -> float:
    return float(np.exp(-0.5 * ((x - mean) / std) ** 2))

def analytical_quality_score(config: WorldConfig) -> float:
    scores = {}

    # 1. BALANCE
    difficulty = (
        config.challenges.signal_noise_level * 0.25 +
        config.challenges.allocation_tightness * 0.25 +
        config.challenges.sequence_scramble_rate * 0.2 +
        config.challenges.negotiation_hardness * 0.15 +
        config.player.risk_modifier * 0.15
    )
    scores["balance"] = gaussian_score(difficulty, mean=0.5, std=0.12)

    # 2. DRAMA
    has_threat = any(a.archetype in ["adversary", "competitor"] for a in config.agents)
    has_opp   = any(a.archetype == "opportunity" for a in config.agents)
    scores["drama"] = 1.0 if (has_threat and has_opp) else 0.15

    # 3. COHERENCE
    coherence = 1.0
    if config.economy.trend == "expansion" and config.economy.sector_health < 0.25:
        coherence *= 0.4
    if config.player.skill_level > 0.8 and config.challenges.signal_noise_level < 0.2:
        coherence *= 0.6
    scores["coherence"] = coherence

    # 4. AGENT DIVERSITY
    if len(config.agents) >= 2:
        vectors = np.array([a.behavior_vector for a in config.agents])
        from scipy.spatial.distance import pdist
        mean_dist = float(np.mean(pdist(vectors, metric="euclidean")))
        scores["diversity"] = min(1.0, mean_dist / 0.6)
    else:
        scores["diversity"] = 0.0

    # 5. COMPLETABILITY
    win_rate = headless_simulate(config, n=20)
    scores["completable"] = gaussian_score(win_rate, mean=0.38, std=0.15)

    # 6. AGENT COUNT
    scores["agent_count"] = gaussian_score(len(config.agents), mean=5.0, std=1.5)

    weights = {
        "balance":     0.22,
        "drama":       0.22,
        "coherence":   0.18,
        "diversity":   0.15,
        "completable": 0.15,
        "agent_count": 0.08,
    }

    return float(sum(scores[k] * weights[k] for k in weights))
