import numpy as np
import xgboost as xgb
import joblib
import os
import sys
import matplotlib.pyplot as plt

# Add the root directory to sys.path to import trajectory
sys.path.append(os.getcwd())

from trajectory.core.seed_engine import WorldConfig
from trajectory.core.career_taxonomy import CAREER_TAXONOMY
from trajectory.ml.analytical_scorer import analytical_quality_score
from trajectory.ml.logger import SimulationLogger

def generate_training_data(n_samples: int = 500, logger=None):
    global_rng = np.random.default_rng(42)
    X = []
    y = []

    pillars = list(CAREER_TAXONOMY.keys())

    for i in range(n_samples):
        if i % 50 == 0: print(f"Generating sample {i}...")
        seed = int(global_rng.integers(0, 2**32))
        pillar = global_rng.choice(pillars)
        career = global_rng.choice(CAREER_TAXONOMY[pillar]["careers"])

        config = WorldConfig.from_seed(seed, pillar, career)
        quality = analytical_quality_score(config)

        vector = config.to_vector()
        X.append(vector)
        y.append(quality)

        if logger:
            logger.log_world_config(vector, quality)

    return np.array(X), np.array(y)

def train_quality_model():
    logger = SimulationLogger()
    print(f"Starting training data collection. Run ID: {logger.run_id}")

    n_samples = 500
    X, y = generate_training_data(n_samples=n_samples, logger=logger)

    print("Training XGBoost model...")
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        importance_type='weight'
    )

    model.fit(X, y)

    model_dir = "trajectory/ml/models"
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, "seed_quality.pkl"))
    print(f"Model trained and saved to {model_dir}/seed_quality.pkl")

    # --- Generate Metrics & Visuals ---
    print("Generating training pipeline visuals...")

    # 1. Quality Score Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(y, bins=30, color='#2E5090', edgecolor='white', alpha=0.8)
    plt.title('World Generation Quality Scrutiny (Analytical Labels)')
    plt.xlabel('Analytical Score')
    plt.ylabel('Seed Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(logger.session_dir, 'quality_distribution.png'))
    plt.close()

    # 2. Feature Importance
    plt.figure(figsize=(12, 8))
    xgb.plot_importance(model, max_num_features=15, height=0.7, color='#2E5090')
    plt.title('XGBoost Determinant Weighting (Feature Importance)')
    plt.tight_layout()
    plt.savefig(os.path.join(logger.session_dir, 'determinant_importance.png'))
    plt.close()

    print(f"Pipeline data and visuals organized in {logger.session_dir}")

if __name__ == "__main__":
    train_quality_model()
