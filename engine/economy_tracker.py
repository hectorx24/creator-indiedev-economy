"""
Creator & Indie Economy Pulse Engine
Dual-Domain Telemetry Engine (Content Audiovisual Metrics + Solo Software Engineering)

Author: Héctor López (Aeterna Labs)
Implements:
- Multiplatform Audience Retention Decay: R(t) = exp(-alpha * t) * (1 - beta * hook_loss)
- Developer Context Switching Tax: Cognitive switching penalty = 23.2 minutes / task interrupt
- Revenue Variance Decomposition: Volatile ad CPM/sponsorships vs. Sticky SaaS MRR
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class CreatorDevEconomyEngine:
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        
    def simulate_video_retention_curve(
        self,
        duration_minutes: float = 12.0,
        hook_strength: float = 0.85, # 0 to 1 (first 3-30s punchiness)
        pacing_density: float = 0.75, # edit cuts per minute, narrative tension
    ) -> pd.DataFrame:
        """Models second-by-second viewer retention curve for YouTube long-form content."""
        seconds = np.arange(0, int(duration_minutes * 60) + 1, 5) # 5s intervals
        
        # Initial 30s drop (hook penalty)
        # Strong hooks retain 75-85% at 30s; weak hooks collapse to 50%
        retention = []
        for s in seconds:
            if s <= 30:
                drop = (1.0 - hook_strength) * (s / 30.0) * 0.35
                r = 1.0 - drop
            else:
                decay_rate = 0.00035 / max(0.2, pacing_density)
                baseline = (1.0 - (1.0 - hook_strength) * 0.35)
                r = baseline * np.exp(-decay_rate * (s - 30))
                # Add micro-bumps for narrative chapter spikes
                if s % 180 == 0:
                    r += 0.025
            retention.append(float(np.clip(r, 0.05, 1.0) * 100.0))
            
        return pd.DataFrame({"time_seconds": seconds, "retention_pct": retention})

    def simulate_weekly_cycle(
        self,
        week: int,
        videos_produced: int = 2,
        github_commits: int = 28,
        context_switches: int = 14,
        saas_active_subscribers: int = 120,
    ) -> Dict:
        """Simulates one weekly cohort cycle combining media production and software development."""
        # 1. Media metrics
        views_weekly = int(videos_produced * np.random.normal(18500, 3200))
        ad_rpm = float(np.random.normal(3.85, 0.45)) # USD per 1000 views
        sponsor_revenue = float(np.random.choice([0.0, 750.0, 1500.0], p=[0.6, 0.3, 0.1]))
        media_gross_revenue = float(round((views_weekly / 1000.0) * ad_rpm + sponsor_revenue, 2))
        
        # 2. Software development metrics
        # Context switching tax: each interrupt consumes ~23 mins of cognitive re-orientation
        lost_deep_work_hours = float(round((context_switches * 23.2) / 60.0, 1))
        effective_coding_hours = float(round(max(4.0, (github_commits * 0.85) - (lost_deep_work_hours * 0.4)), 1))
        
        saas_mrr = float(saas_active_subscribers * 19.0) # $19/mo tier
        total_weekly_income = float(round(media_gross_revenue + (saas_mrr / 4.0), 2))
        
        # 3. Psychological Burnout Index (Maslach adaptation: 0 - 100)
        # Driven by high context switches, unbuffered release deadlines, and volatile revenue anxiety
        fatigue_strain = (videos_produced * 16.0) + (effective_coding_hours * 1.2) + (lost_deep_work_hours * 2.2)
        income_uncertainty_strain = 18.0 if sponsor_revenue == 0.0 else 6.0
        burnout_score = float(np.clip(fatigue_strain * 0.45 + income_uncertainty_strain + np.random.normal(0, 4), 10.0, 95.0))
        
        return {
            "week": week,
            "videos_produced": videos_produced,
            "weekly_views": views_weekly,
            "media_revenue_usd": media_gross_revenue,
            "saas_mrr_usd": saas_mrr,
            "total_weekly_income_usd": total_weekly_income,
            "github_commits": github_commits,
            "context_switches": context_switches,
            "lost_focus_hours": lost_deep_work_hours,
            "effective_coding_hours": effective_coding_hours,
            "burnout_hazard_index": round(burnout_score, 1),
            "burnout_risk_tier": "Critical" if burnout_score > 70 else ("Warning" if burnout_score > 48 else "Sustainable"),
        }

    def simulate_longitudinal_year(self, weeks: int = 52) -> pd.DataFrame:
        records = []
        subs = 40
        for w in range(1, weeks + 1):
            subs += int(np.random.choice([2, 4, 6, -1]))
            # Creator crunch seasons (Q4 ad surges vs Summer code sprints)
            is_crunch = (w in [11, 12, 42, 43, 44])
            vids = 3 if is_crunch else int(np.random.choice([1, 2]))
            commits = 45 if not is_crunch else 15
            switches = 22 if is_crunch else int(np.random.uniform(8, 16))
            
            rec = self.simulate_weekly_cycle(
                week=w,
                videos_produced=vids,
                github_commits=commits,
                context_switches=switches,
                saas_active_subscribers=subs,
            )
            records.append(rec)
        return pd.DataFrame(records)

if __name__ == "__main__":
    engine = CreatorDevEconomyEngine()
    df = engine.simulate_longitudinal_year(52)
    print("Creator-Dev Economy 52-Week simulation completed:")
    print(df[["week", "total_weekly_income_usd", "effective_coding_hours", "burnout_hazard_index", "burnout_risk_tier"]].head(5))
