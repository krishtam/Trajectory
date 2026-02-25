import os
import json
import csv
from datetime import datetime

class SimulationLogger:
    def __init__(self, log_dir="trajectory/ml/logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = os.path.join(self.log_dir, self.run_id)
        os.makedirs(self.session_dir, exist_ok=True)

    def log_bayesian_inference(self, cycle, evidence, event, probabilities):
        file_path = os.path.join(self.session_dir, "bayesian_events.csv")
        file_exists = os.path.isfile(file_path)
        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["cycle", "evidence", "sampled_event", "prob_fires"])
            writer.writerow([cycle, json.dumps(evidence), event, probabilities])

    def log_regression_update(self, update_num, features, performance, weights, adjustment):
        file_path = os.path.join(self.session_dir, "difficulty_regression.csv")
        file_exists = os.path.isfile(file_path)
        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["update_num", "features", "performance", "weights", "adjustment"])
            writer.writerow([update_num, list(features), performance, list(weights), list(adjustment)])

    def log_world_config(self, config_vector, quality_score):
        file_path = os.path.join(self.session_dir, "training_samples.csv")
        file_exists = os.path.isfile(file_path)
        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["config_vector", "quality_score"])
            writer.writerow([config_vector, quality_score])
