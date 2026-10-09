"""
Burnout Hazard & Cognitive Fatigue Predictor
Vectorized Logistic & Ridge Regression Ensemble

Author: Héctor López (Aeterna Labs)
Evaluates:
- Maslach Burnout Inventory dimensions (Exhaustion, Depersonalization, Inefficacy)
- Impact of Context-Switching Penalties on Long-Term Solo Dev Retention
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple

class BurnoutPredictionPipeline:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.weights = None
        self.bias = 0.0
        self.mean_ = None
        self.scale_ = None
        self.feature_names = [
            "videos_produced",
            "github_commits",
            "context_switches",
            "lost_focus_hours",
            "effective_coding_hours",
        ]

    def fit_and_evaluate(self, df: pd.DataFrame, test_ratio: float = 0.25) -> Dict:
        X = df[self.feature_names].to_numpy()
        y = (df["burnout_hazard_index"] >= 50.0).astype(int).to_numpy() # High burnout classification
        
        np.random.seed(self.random_state)
        indices = np.random.permutation(len(X))
        split = int(len(X) * (1.0 - test_ratio))
        
        X_train_raw, X_test_raw = X[indices[:split]], X[indices[split:]]
        y_train, y_test = y[indices[:split]], y[indices[split:]]
        
        self.mean_ = np.mean(X_train_raw, axis=0)
        self.scale_ = np.std(X_train_raw, axis=0) + 1e-8
        
        X_train = (X_train_raw - self.mean_) / self.scale_
        X_test = (X_test_raw - self.mean_) / self.scale_
        
        # Vectorized Gradient Descent
        n_features = X_train.shape[1]
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        m = len(X_train)
        
        for _ in range(800):
            z = np.dot(X_train, self.weights) + self.bias
            preds = 1.0 / (1.0 + np.exp(-np.clip(z, -25.0, 25.0)))
            error = preds - y_train
            self.weights -= 0.05 * ((1.0 / m) * np.dot(X_train.T, error) + 0.01 * self.weights)
            self.bias -= 0.05 * ((1.0 / m) * np.sum(error))
            
        test_z = np.dot(X_test, self.weights) + self.bias
        test_probs = 1.0 / (1.0 + np.exp(-np.clip(test_z, -25.0, 25.0)))
        
        # Calculate ROC-AUC via rank-sum
        r = np.argsort(np.argsort(test_probs))
        n_pos = np.sum(y_test == 1)
        n_neg = np.sum(y_test == 0)
        if n_pos == 0 or n_neg == 0:
            roc_auc = 0.5
        else:
            rank_sum_pos = np.sum(r[y_test == 1]) + n_pos
            u = rank_sum_pos - (n_pos * (n_pos + 1)) / 2.0
            roc_auc = float(u / (n_pos * n_neg))
            
        feat_imp = {feat: float(round(abs(w), 4)) for feat, w in zip(self.feature_names, self.weights)}
        sorted_fi = dict(sorted(feat_imp.items(), key=lambda item: item[1], reverse=True))
        
        return {
            "roc_auc": float(round(roc_auc, 4)),
            "feature_weights": sorted_fi,
            "sample_size": len(df),
        }
