import numpy as np

class DifficultyCalibrator:
    """Online Ridge Regression for adaptive difficulty.
    Watches player challenge performance and adjusts WorldConfig parameters."""

    def __init__(self, d: int = 6, lambda_reg: float = 1.0):
        self.d = d
        self.lambda_reg = lambda_reg
        self.A_inv = np.eye(d) / lambda_reg   # (X^T X + λI)^{-1}
        self.b = np.zeros(d)                   # X^T y
        self.w = np.zeros(d)                   # current weights
        self.n_updates = 0

    def update(self, x: np.ndarray, y: float):
        """x = challenge feature vector, y = performance score (0-1)."""
        Ax = self.A_inv @ x
        self.A_inv -= np.outer(Ax, Ax) / (1.0 + x @ Ax)
        self.b += x * y
        self.w = self.A_inv @ self.b
        self.n_updates += 1

    def predict_difficulty_adjustment(self, current_features: np.ndarray) -> np.ndarray:
        if self.n_updates < 3:
            return np.zeros(5)

        predicted_performance = float(current_features @ self.w)
        delta = predicted_performance - 0.55

        adjustment = delta * np.array([
            0.05,   # Δ signal_noise_level
            0.04,   # Δ allocation_tightness
            0.04,   # Δ sequence_scramble_rate
           -500.0,  # Δ pressure_window_ms
            0.03,   # Δ negotiation_hardness
        ])

        return adjustment
