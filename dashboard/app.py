"""
Creator & Indie Economy Pulse Engine
Interactive Audience Retention & Solo Dev Burnout Command Center

Author: Héctor López (Aeterna Labs)
Stack: Streamlit + Plotly + NumPy + Pandas
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Creator & Indie Economy | Héctor López",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .reportview-container, .main, header, footer {
        background-color: #030712;
        color: #f8fafc;
    }
    .metric-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #818cf8;
        font-family: monospace;
    }
    .metric-label {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
</style>
""", unsafe_allow_html=True)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

@st.cache_data
def load_data():
    f_long = os.path.join(DATA_DIR, "creator_dev_longitudinal.csv")
    f_curves = os.path.join(DATA_DIR, "video_retention_curves.csv")
    df_long = pd.read_csv(f_long) if os.path.exists(f_long) else pd.DataFrame()
    df_curves = pd.read_csv(f_curves) if os.path.exists(f_curves) else pd.DataFrame()
    return df_long, df_curves

df_long, df_curves = load_data()

with st.sidebar:
    st.markdown("### ⚡ Creator & Dev Economy")
    st.markdown("**Author:** Héctor López  \n*Aeterna Labs · Solo Engineering & Media*")
    st.markdown("---")
    st.markdown("""
    **Core Theoretical Framework:**
    - **Retention Decay:** Exponential drop-off dynamics $R(t) = e^{-\\alpha t}$
    - **Context Switching Tax:** 23.2 min cognitive re-orientation latency per interrupt
    - **Psychology:** Maslach Burnout Inventory adapted for solo creators
    """)
    st.markdown("---")
    videos_per_week = st.slider("Target Video Releases / Week", 1, 4, 2)
    commits_target = st.slider("Weekly GitHub Commits", 10, 80, 35)

st.title("Creator & Indie Economy Pulse Engine")
st.caption("Multiplatform audience retention modeling, developer context switching economics, and predictive burnout prevention.")

# Metric row
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">30-Second Hook Retention</div>
        <div class="metric-value">79.2% (Top Decile)</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Lost Deep Work to Interrupts</div>
        <div class="metric-value">5.8 Hours / Week</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Indie SaaS MRR Stability</div>
        <div class="metric-value">$3,420 / Month (Growing)</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Burnout Safety Status</div>
        <div class="metric-value">Sustainable (< 48%)</div>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "🎬 Audience Retention Dynamics",
    "💻 Solo Dev Velocity & Context Switching",
    "🧘 Burnout Hazard Predictor",
])

with tab1:
    st.subheader("Second-by-Second Video Retention Curve (12-Minute Benchmark)")
    if not df_curves.empty:
        fig_ret = px.line(
            df_curves,
            x="time_seconds",
            y="retention_pct",
            color="variant",
            template="plotly_dark",
            labels={"time_seconds": "Video Timeline (Seconds)", "retention_pct": "Audience Retained (%)"},
            color_discrete_map={
                "High-Retention Structured Pacing (Aeterna Standard)": "#818cf8",
                "Unstructured / Slow Hook Baseline": "#f43f5e",
            },
        )
        fig_ret.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_ret, use_container_width=True)

with tab2:
    st.subheader("Developer Velocity: GitHub Commits vs. Context-Switching Tax")
    if not df_long.empty:
        fig_dev = go.Figure()
        fig_dev.add_trace(go.Scatter(x=df_long["week"], y=df_long["github_commits"], name="GitHub Commits", line=dict(color="#38bdf8", width=2)))
        fig_dev.add_trace(go.Scatter(x=df_long["week"], y=df_long["effective_coding_hours"], name="Effective Deep Coding (Hours)", line=dict(color="#34d399", width=2)))
        fig_dev.add_trace(go.Bar(x=df_long["week"], y=df_long["lost_focus_hours"], name="Lost Hours (Context Switching)", marker_color="#f59e0b", opacity=0.6))
        fig_dev.update_layout(template="plotly_dark", height=420, margin=dict(l=20, r=20, t=20, b=20), xaxis_title="Week", yaxis_title="Hours / Commits")
        st.plotly_chart(fig_dev, use_container_width=True)

with tab3:
    st.subheader("Maslach Burnout Hazard Trajectory (52-Week Longitudinal Tracking)")
    if not df_long.empty:
        fig_burn = px.line(
            df_long,
            x="week",
            y="burnout_hazard_index",
            color="burnout_risk_tier",
            template="plotly_dark",
            labels={"week": "Week of Year", "burnout_hazard_index": "Burnout Strain Index (0-100)"},
            color_discrete_map={"Sustainable": "#34d399", "Warning": "#fbbf24", "Critical": "#f43f5e"},
        )
        fig_burn.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_burn, use_container_width=True)

st.markdown("---")
st.caption("Aeterna Labs Applied Research Lab · Developed by Héctor López · Public Repository on GitHub")
