# TRAJECTORY

**Trajectory** is a deterministic, probabilistic career simulation game designed for the FBLA Computer Game & Simulation Programming competition. It features advanced simulation mechanics driven by Bayesian networks, Markov chains, and machine learning models.

## Overview

In Trajectory, players navigate a 5-day professional narrative arc. The world is generated deterministically from a single seed, ensuring full reproducibility. The simulation is focused on two primary careers:
- **Cardiac Surgeon** (Expert Pillar): Navigate critical surgical procedures and team dynamics.
- **Day Trader** (Allocator Pillar): Manage a high-stakes portfolio in a volatile market.

## Installation

### Prerequisites
- Python 3.11+
- Requirements: `pygame`, `numpy`, `scipy`, `xgboost`, `scikit-learn`, `pgmpy`, `matplotlib`, `Pillow`, `joblib`.

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Initialize assets (Drawn programmatically):
   ```bash
   python -m trajectory.pipeline.generate_placeholders
   ```

## ML Training Pipeline & Data Collection

Trajectory features a professional ML pipeline for seed quality screening and adaptive difficulty.

### 1. Seed Quality Scrutiny (XGBoost)
The game uses a pre-trained XGBoost model to screen world seeds. Seeds that produce "boring" or "unbalanced" worlds are automatically filtered.

**To run the training pipeline:**
```bash
python -m trajectory.ml.train_quality_model
```
**Pipeline Workflow:**
- **Data Collection:** The script generates 500+ world configurations across all pillars.
- **Analytical Labeling:** Each config is scored based on balance, drama, and completability.
- **Logging:** All samples are logged to `trajectory/ml/logs/[RUN_ID]/training_samples.csv`.
- **Model Training:** An XGBoost regressor is trained on the collected vectors.
- **Visuals:** The pipeline automatically generates `quality_distribution.png` and `determinant_importance.png` in the run directory.

### 2. Bayesian & Regression Logging
During active gameplay, Trajectory logs simulation data to facilitate further analysis and model refinement.

- **Bayesian Events:** Every inference made by the pgmpy-based network is logged to `bayesian_events.csv`, including evidence and sampled events.
- **Difficulty Regression:** Every update to the online Ridge Regression model (Difficulty Calibrator) is logged to `difficulty_regression.csv`, tracking features, performance scores, weights, and delta adjustments.

**Log Location:** `trajectory/ml/logs/`

## Running the Game

```bash
python -m trajectory.main
```

## Game Design

- **Narrative Arcs:** Challenges emerge from a structured 5-day story.
- **Programmatic Assets:** All visuals (icons, portraits, medical monitors) are drawn programmatically for a clean, professional aesthetic.
- **Deterministic Simulation:** Same seed = Identical experience.
