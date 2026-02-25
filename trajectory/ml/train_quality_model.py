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
    n_samples = 200 # Increased for better metrics
    X, y = generate_training_data(n_samples=n_samples)

    print("Training XGBoost model...")
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        importance_type='weight'
    )

    model.fit(X, y)

    os.makedirs("trajectory/ml/models", exist_ok=True)
    joblib.dump(model, "trajectory/ml/models/seed_quality.pkl")
    print("Model trained and saved to trajectory/ml/models/seed_quality.pkl")

    # --- Generate Presentation Graphics ---
    print("Generating presentation graphics...")

    # 1. Quality Score Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(y, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Distribution of Generated World Quality Scores')
    plt.xlabel('Quality Score (0-1)')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('trajectory/ml/models/quality_distribution.png')
    plt.close()

    # 2. Feature Importance
    plt.figure(figsize=(12, 8))
    xgb.plot_importance(model, max_num_features=15, height=0.7, color='coral')
    plt.title('XGBoost Feature Importance for Seed Quality')
    plt.tight_layout()
    plt.savefig('trajectory/ml/models/feature_importance.png')
    plt.close()

    print("Presentation graphics saved to trajectory/ml/models/")

if __name__ == "__main__":
    train_quality_model()
