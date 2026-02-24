from trajectory.core.world_rng import WorldRNG
from trajectory.core.seed_engine import WorldConfig
from trajectory.core.simulation import WorldState
from trajectory.core.bayesian_network import build_event_network, sample_next_event

def headless_simulate(config: WorldConfig, n: int = 100) -> float:
    """
    Runs n simulated playthroughs of the world config.
    Returns win rate (fraction that reach win condition).
    """
    wins = 0

    for run_idx in range(n):
        # Deterministic sub-seed
        run_rng = WorldRNG(config.seed ^ (run_idx * 2654435761))

        state = WorldState(config)
        event_network = build_event_network(config.events)

        won = False
        for cycle in range(config.win_condition.time_limit_cycles):
            state.cycle = cycle
            # Update agents
            for agent in state.agents:
                agent.update_state(state.pressure_level, run_rng)

            # Sample event
            evidence = state.to_evidence_dict()
            event = sample_next_event(event_network, evidence, run_rng)
            if event:
                state.apply_event(event, config)

            # Simulate player performance
            performance = run_rng.normal(mean=config.player.skill_level, std=0.15)
            performance = float(max(0, min(1, performance)))

            state.apply_challenge_outcome(performance, config)

            if state.check_win(config.win_condition):
                won = True
                break

        if won:
            wins += 1

    return wins / n
