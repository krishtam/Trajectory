# Trajectory Technical Reference

This document details the mathematical and theoretical foundations of the Trajectory simulation engine.

## 1. Deterministic Seeded PRNG

Trajectory uses NumPy's **PCG64** (Permuted Congruential Generator) to ensure full reproducibility. Every world parameter, from market volatility to agent positions, is drawn from a single `WorldRNG` object initialized with the user's seed.

**Draw Order Guarantee:**
To maintain determinism across versions, all random draws follow a strict, documented sequence in `WorldConfig.from_seed`.

## 2. Bayesian Event Networks

Professional events are not independent. Trajectory uses a **Discrete Bayesian Network** (via `pgmpy`) to model conditional probabilities between world states and events.

- **Network Structure:** `EconomyState` → `MarketShock`, `PlayerPerformance` → `OpportunityWindow`, etc.
- **Inference:** The game uses Variable Elimination to compute $P(Event | Evidence)$ where evidence is the current world state.
- **Sampling:** A Bernoulli trial is performed against the computed probability using the seeded RNG.

## 3. Agent Markov Chains

Each professional agent operates as a discrete-time Markov chain with states: `dormant`, `active`, `stressed`, `hostile`, and `cooperative`.

- **Transition Matrix:** Dynamically computed based on agent attributes (aggression, loyalty) and world pressure.
- **State Updates:** Occur every simulation cycle, ensuring agents react realistically to the evolving environment.

## 4. ML Model 1: Seed Quality Scorer (XGBoost)

Random seeds can occasionally produce "boring" or "impossible" worlds. Trajectory employs an **XGBoost Regressor** to screen seeds during the boot process.

- **Features:** 23-dimensional vector representing the generated `WorldConfig`.
- **Labels:** Analytical quality scores derived from balance, drama, coherence, and agent diversity metrics.
- **Goal:** Filter out seeds with low predicted quality to ensure an engaging player experience.

## 5. ML Model 2: Difficulty Calibrator (Online Ridge Regression)

Trajectory implements adaptive difficulty through **Online Ridge Regression**.

- **Algorithm:** Uses the Sherman-Morrison formula for O(d²) recursive least squares updates.
- **Input:** Player performance features (accuracy, time taken, resource efficiency).
- **Output:** Delta adjustments to `ChallengeConfig` parameters (signal noise, window time).
- **Effect:** The game stays in the "flow state" by becoming harder as the player improves and easier if the player struggles.

## 6. Rendering & Procedural Visuals

The rendering engine uses a layered approach in Pygame:
- **Procedural Generators:** Create pillar-specific visuals. The Expert pillar features stylized medical anatomy and animated vitals, while the Allocator pillar features high-fidelity candlestick charts and live order book depth visualizations.
- **Asset Colorization:** Grayscale assets are dynamically tinted to the pillar's primary color at runtime to preserve memory and ensure thematic consistency.
