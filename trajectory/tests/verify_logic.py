import sys
import os

# Add root to path
sys.path.append(os.getcwd())

from trajectory.core.seed_engine import WorldConfig
from trajectory.core.simulation import WorldState
from trajectory.ml.headless_simulate import headless_simulate
from trajectory.ml.quality_model import load_quality_model, screen_seed

def test_simulation():
    print("Testing Simulation Logic...")
    pillar = "Expert"
    career = "Chemist"
    seed = 4821

    config = WorldConfig.from_seed(seed, pillar, career)
    print(f"WorldConfig generated for {career} ({pillar}) with seed {seed}")

    win_rate = headless_simulate(config, n=10)
    print(f"Win rate over 10 runs: {win_rate*100}%")

    state = WorldState(config)
    print("Initial resource:", state.resource)
    state.apply_challenge_outcome(1.0, config) # Perfect performance
    print("Resource after perfect challenge:", state.resource)

    print("Simulation test passed.")

def test_ml_model():
    print("\nTesting ML Quality Model...")
    model = load_quality_model()
    if model:
        quality, conf, config = screen_seed(4821, "Expert", "Chemist", model)
        print(f"Seed 4821 Quality Score: {quality:.2f}, Confidence: {conf:.2f}")
    else:
        print("Model not found.")

if __name__ == "__main__":
    try:
        test_simulation()
        test_ml_model()
        print("\nAll non-GUI tests passed.")
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
