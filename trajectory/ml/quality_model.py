import numpy as np
import joblib
import os
from trajectory.core.seed_engine import WorldConfig, CURATED_SEEDS

def load_quality_model():
    model_path = os.path.join(os.path.dirname(__file__), "models", "seed_quality.pkl")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

def screen_seed(seed: int, pillar: str, career: str, model) -> tuple:
    config = WorldConfig.from_seed(seed, pillar, career)
    if model is None:
        return 0.5, 1.0, config

    vector = np.array(config.to_vector()).reshape(1, -1)
    quality = float(model.predict(vector)[0])
    confidence = 1.0 - abs(quality - 0.5) * 0.2
    return quality, confidence, config

def get_good_seed(pillar: str, career: str, model, min_quality: float = 0.5) -> tuple:
    screening_rng = np.random.default_rng()
    for attempt in range(50):
        candidate = int(screening_rng.integers(0, 2**32))
        quality, confidence, config = screen_seed(candidate, pillar, career, model)
        if quality >= min_quality and confidence >= 0.7:
            config.quality_score = quality
            config.quality_confidence = confidence
            return candidate, config

    # Fallback
    fallback_seed = CURATED_SEEDS.get((pillar, career), 4821)
    config = WorldConfig.from_seed(fallback_seed, pillar, career)
    quality, confidence, config = screen_seed(fallback_seed, pillar, career, model)
    config.quality_score = quality
    config.quality_confidence = confidence
    return fallback_seed, config
