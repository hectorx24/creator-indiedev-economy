"""
Dataset Pre-computation Script for Project 3
Generates 52 weeks of creator and dev economy data and video retention curves.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.economy_tracker import CreatorDevEconomyEngine
from models.burnout_model import BurnoutPredictionPipeline

def main():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    print("[1/2] Generating longitudinal creator & dev telemetry (3-year cohort)...")
    engine = CreatorDevEconomyEngine(seed=42)
    df_long = engine.simulate_longitudinal_year(weeks=156)
    df_long.to_csv(os.path.join(data_dir, "creator_dev_longitudinal.csv"), index=False)
    print(f"-> Saved longitudinal dataset: {len(df_long)} weeks")
    
    print("[2/2] Generating YouTube video retention curve benchmark...")
    df_retention_strong = engine.simulate_video_retention_curve(duration_minutes=12.0, hook_strength=0.90, pacing_density=0.85)
    df_retention_strong["variant"] = "High-Retention Structured Pacing (Aeterna Standard)"
    
    df_retention_weak = engine.simulate_video_retention_curve(duration_minutes=12.0, hook_strength=0.55, pacing_density=0.45)
    df_retention_weak["variant"] = "Unstructured / Slow Hook Baseline"
    
    import pandas as pd
    df_curves = pd.concat([df_retention_strong, df_retention_weak], ignore_index=True)
    df_curves.to_csv(os.path.join(data_dir, "video_retention_curves.csv"), index=False)
    print(f"-> Saved video retention curves: {len(df_curves)} time points")
    
    pipeline = BurnoutPredictionPipeline(random_state=42)
    metrics = pipeline.fit_and_evaluate(df_long)
    print(f"-> Burnout Prediction Model Validated: ROC-AUC = {metrics['roc_auc']:.4f}")
    print(f"-> Weights: {metrics['feature_weights']}")
    print("Project 3 datasets generated successfully!")

if __name__ == "__main__":
    main()
