import numpy as np
import xgboost as xgb
import joblib
import os
import sys

# Add the root directory to sys.path to import trajectory
sys.path.append(os.getcwd())

from trajectory.core.seed_engine import WorldConfig
from trajectory.core.career_taxonomy import CAREER_TAXONOMY
from trajectory.ml.analytical_scorer import analytical_quality_score

def generate_training_data(n_samples: int = 100):
    global_rng = np.random.default_rng(42)
    X = []
    y = []

    pillars = list(CAREER_TAXONOMY.keys())

    for i in range(n_samples):
        if i % 10 == 0: print(f"Generating sample {i}...")
        seed = int(global_rng.integers(0, 2**32))
        pillar = global_rng.choice(pillars)
        career = global_rng.choice(CAREER_TAXONOMY[pillar]["careers"])

        config = WorldConfig.from_seed(seed, pillar, career)
        quality = analytical_quality_score(config)

        X.append(config.to_vector())
        y.append(quality)

    return np.array(X), np.array(y)

def train_quality_model():
    print("Starting training data generation...")
    X, y = generate_training_data(n_samples=100)

    print("Training XGBoost model...")
    model = xgb.XGBRegressor(
        n_estimators=50,
        max_depth=4,
        learning_rate=0.1,
        random_state=42
    )

    model.fit(X, y)

    os.makedirs("trajectory/ml/models", exist_ok=True)
    joblib.dump(model, "trajectory/ml/models/seed_quality.pkl")
    print("Model trained and saved to trajectory/ml/models/seed_quality.pkl")

if __name__ == "__main__":
    train_quality_model()
