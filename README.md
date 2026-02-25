# TRAJECTORY

**Trajectory** is a probabilistic career simulation game designed for the FBLA Computer Game & Simulation Programming competition.

## Overview

In Trajectory, players select a professional career and navigate a series of professional challenges. The game uses a seeded PRNG system to ensure that every world is fully deterministic and reproducible. It features advanced simulation mechanics, including:

- **Bayesian Event Networks:** Modeling complex correlations between economic shifts and professional opportunities.
- **Agent Markov Chains:** Simulating dynamic relationships and behaviors of professional contacts (competitors, authorities, opportunities).
- **ML Seed Screening:** An XGBoost model ensures that randomly generated worlds meet high quality and balance standards.
- **Adaptive Difficulty:** An online Ridge Regression model adjusts challenge parameters based on real-time player performance.

## Installation

### Prerequisites

- Python 3.11 or higher
- All dependencies listed in `requirements.txt`

### Setup

1. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. Generate placeholder assets (if not already present):
   ```bash
   python -m trajectory.pipeline.generate_placeholders
   ```

3. Train the ML quality model (optional, pre-trained model included):
   ```bash
   python -m trajectory.ml.train_quality_model
   ```

## Running the Game

To launch the game, run:
```bash
python -m trajectory.main
```

## How to Play

1. **Career Selection:** Choose from three main career trajectories: Chemist (Expert), Trader (Allocator), or Entrepreneur (Builder).
2. **Navigate the World:** Observe your professional network, resource levels, and the procedural data visualizations (e.g., molecule diagrams, candlestick charts).
3. **Challenges:** Complete various professional challenges (Signal Reading, Resource Allocation, etc.) to grow your career.
4. **Win Condition:** Reach your professional goals within the allotted time cycles.

## Project Structure

- `trajectory/core/`: The simulation engine and deterministic RNG logic.
- `trajectory/ml/`: Machine learning models for quality screening and adaptive difficulty.
- `trajectory/rendering/`: The Pygame-based rendering pipeline and procedural generators.
- `trajectory/screens/`: Game state management and UI screens.
- `trajectory/assets/`: Graphical and font assets.
- `trajectory/data/`: Configuration templates for events and careers.
