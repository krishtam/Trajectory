# Training the Quality Model

Trajectory includes a pre-trained XGBoost model for seed quality screening. However, the model can be retrained or fine-tuned using the provided pipeline.

## Training Pipeline

The training process involves three stages:
1. **Data Generation:** Thousands of random world configurations are generated from different seeds.
2. **Analytical Scoring:** Each configuration is passed through a rule-based scorer that evaluates balance, drama, and coherence.
3. **Model Fitting:** An XGBoost regressor is trained to map the configuration features to the analytical score.

## Running the Training

To retrain the model:
```bash
python -m trajectory.ml.train_quality_model
```

The script will:
- Generate training samples.
- Train the model using `xgboost`.
- Save the model to `trajectory/ml/models/seed_quality.pkl`.
- Generate presentation graphics (feature importance and score distribution) in the same directory.

## Visualizing Results

After training, you can find the following plots in `trajectory/ml/models/`:
- `quality_distribution.png`: Shows the range of quality scores in the training set.
- `feature_importance.png`: Shows which world parameters most significantly impact the predicted quality.
