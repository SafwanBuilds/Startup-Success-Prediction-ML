"""
pages/2_Model_Comparison.py
-----------------------------
Page 3: Model Comparison Dashboard. Displays a side-by-side performance
comparison between the Random Forest and Gradient Boosting classifiers
that were trained for this project, including an interactive metrics
table, per-metric bar charts, training-time comparison, and confusion
matrix visualizations for both models.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.styling import inject_global_css, render_footer

st.set_page_config(
    page_title="Model Comparison | Startup Success Prediction System",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Hide default Streamlit header */
header[data-testid="stHeader"] {
    background: #020b24;   /* Apni website ka background color */
}

/* Main app background */
.stApp {
    background-color: #020b24;
}
/* Headings (Enter Startup Details etc.) */
h1, h2, h3 {
    color: white !important;
}


/* Main button styling */
.stButton > button {
    background-color: white !important;
    color: black !important;   /* 👈 THIS is main fix */
    font-weight: 600 !important;
    border-radius: 8px;
    border: none !important;
}

/* Extra safety for span/text inside button */
.stButton > button * {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

inject_global_css()

with st.sidebar:
    # 1. Top Heading
    st.markdown("## 🚀 Startup Success")
    st.markdown("### Prediction System")
    st.markdown("---")
    
    # 2. Your specific navigation
    st.markdown("#### Navigation")
    st.page_link("Home.py", label="Home", icon="🏠")
    st.page_link("pages/1_Startup_Prediction.py", label="Startup Prediction", icon="🔮")
    st.page_link("pages/2_Model_Comparison.py", label="Model Comparison", icon="📊")
    
    st.markdown("---")
    
# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <span class="hero-eyebrow">Model Evaluation</span>
        <h1>📊 Model Comparison Dashboard</h1>
        <p>A detailed performance comparison between the two models trained for
        this project — Random Forest and Gradient Boosting — across accuracy,
        precision, recall, F1-score, ROC-AUC, and training time.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Static evaluation results (from the model training/evaluation run)
# --------------------------------------------------------------------------
METRICS = pd.DataFrame(
    {
        "Model": ["Random Forest", "Gradient Boosting"],
        "Accuracy (%)": [86.96, 90.37],
        "Precision (%)": [91.83, 90.71],
        "Recall (%)": [93.93, 99.54],
        "F1 Score (%)": [92.87, 94.92],
        "ROC-AUC": [0.709, 0.767],
        "Training Time (s)": [24.33, 10.62],
    }
)

MODEL_COLORS = {"Random Forest": "#8B7CFF", "Gradient Boosting": "#1FBF8F"}

# --------------------------------------------------------------------------
# Top-line winner callouts
# --------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(
        '<div class="card"><h4>🏆 Best Accuracy</h4>'
        '<p style="font-size:1.5rem;font-weight:800;color:#6FE7C5;">Gradient Boosting</p>'
        '<p>90.37% vs 86.96%</p></div>',
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        '<div class="card"><h4>🎯 Best Recall</h4>'
        '<p style="font-size:1.5rem;font-weight:800;color:#6FE7C5;">Gradient Boosting</p>'
        '<p>99.54% vs 93.93%</p></div>',
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        '<div class="card"><h4>⚖️ Best F1 Score</h4>'
        '<p style="font-size:1.5rem;font-weight:800;color:#6FE7C5;">Gradient Boosting</p>'
        '<p>94.92% vs 92.87%</p></div>',
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(
        '<div class="card"><h4>⚡ Fastest Training</h4>'
        '<p style="font-size:1.5rem;font-weight:800;color:#6FE7C5;">Gradient Boosting</p>'
        '<p>10.62s vs 24.33s</p></div>',
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------------------------------
# Metrics comparison table
# --------------------------------------------------------------------------
st.markdown('<div class="section-label">Metrics Table</div>', unsafe_allow_html=True)
st.markdown("## Metrics Comparison Table")

styled = (
    METRICS.set_index("Model")
    .style.format(
        {
            "Accuracy (%)": "{:.2f}",
            "Precision (%)": "{:.2f}",
            "Recall (%)": "{:.2f}",
            "F1 Score (%)": "{:.2f}",
            "ROC-AUC": "{:.3f}",
            "Training Time (s)": "{:.2f}",
        }
    )
    .background_gradient(cmap="Greens", subset=["Accuracy (%)", "Precision (%)", "Recall (%)", "F1 Score (%)", "ROC-AUC"])
    .background_gradient(cmap="Greens_r", subset=["Training Time (s)"])
)
st.dataframe(styled, use_container_width=True)

st.write("")

# --------------------------------------------------------------------------
# Helper to build a clean bar chart for a single metric
# --------------------------------------------------------------------------
def metric_bar_chart(metric_col: str, title: str, suffix: str = "%") -> go.Figure:
    fig = px.bar(
        METRICS,
        x="Model",
        y=metric_col,
        color="Model",
        color_discrete_map=MODEL_COLORS,
        text=METRICS[metric_col].map(lambda v: f"{v:.2f}{suffix}" if suffix == "%" else f"{v:.3f}"),
    )
    fig.update_traces(textposition="outside", width=0.45)
    fig.update_layout(
        title=title,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E7ECF7"},
        xaxis=dict(title=""),
        yaxis=dict(title=metric_col, gridcolor="rgba(255,255,255,0.08)"),
        height=380,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig


# --------------------------------------------------------------------------
# Per-metric comparison charts (2 per row)
# --------------------------------------------------------------------------
st.markdown('<div class="section-label">Performance Charts</div>', unsafe_allow_html=True)
st.markdown("## Metric-by-Metric Comparison")

row1c1, row1c2 = st.columns(2)
with row1c1:
    st.plotly_chart(metric_bar_chart("Accuracy (%)", "Accuracy Comparison"), use_container_width=True)
with row1c2:
    st.plotly_chart(metric_bar_chart("Precision (%)", "Precision Comparison"), use_container_width=True)

row2c1, row2c2 = st.columns(2)
with row2c1:
    st.plotly_chart(metric_bar_chart("Recall (%)", "Recall Comparison"), use_container_width=True)
with row2c2:
    st.plotly_chart(metric_bar_chart("F1 Score (%)", "F1 Score Comparison"), use_container_width=True)

row3c1, row3c2 = st.columns(2)
with row3c1:
    st.plotly_chart(metric_bar_chart("ROC-AUC", "ROC-AUC Comparison", suffix=""), use_container_width=True)
with row3c2:
    st.plotly_chart(
        metric_bar_chart("Training Time (s)", "Training Time Comparison (lower is better)", suffix=""),
        use_container_width=True,
    )

st.write("")

# --------------------------------------------------------------------------
# Radar / overview chart
# --------------------------------------------------------------------------
st.markdown('<div class="section-label">Overall View</div>', unsafe_allow_html=True)
st.markdown("## Multi-Metric Radar Overview")

radar_metrics = ["Accuracy (%)", "Precision (%)", "Recall (%)", "F1 Score (%)"]
radar_fig = go.Figure()
for _, row in METRICS.iterrows():
    radar_fig.add_trace(
        go.Scatterpolar(
            r=[row[m] for m in radar_metrics] + [row[radar_metrics[0]]],
            theta=radar_metrics + [radar_metrics[0]],
            fill="toself",
            name=row["Model"],
            line_color=MODEL_COLORS[row["Model"]],
        )
    )
radar_fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[80, 100], gridcolor="rgba(255,255,255,0.1)"),
        bgcolor="rgba(0,0,0,0)",
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    font={"color": "#E7ECF7"},
    height=440,
    legend=dict(orientation="h", yanchor="bottom", y=-0.15),
    margin=dict(l=40, r=40, t=30, b=30),
)
st.plotly_chart(radar_fig, use_container_width=True)

st.write("")

# --------------------------------------------------------------------------
# Confusion matrices
# --------------------------------------------------------------------------
st.markdown('<div class="section-label">Error Analysis</div>', unsafe_allow_html=True)
st.markdown("## Confusion Matrices")
st.caption(
    "Illustrative confusion matrices derived from each model's reported "
    "precision and recall on the test set, assuming a representative class "
    "split. Replace with your exact test-set counts for full precision."
)

# Derive an illustrative confusion matrix from precision/recall assuming
# a representative test set size and class balance, purely for visualization.
TEST_SIZE = 12800        # ~20% holdout of ~64,000 records
POS_RATE = 0.65          # assumed share of successful startups in test set


def build_confusion_matrix(precision: float, recall: float, test_size: int, pos_rate: float):
    """Construct an illustrative confusion matrix consistent with given precision/recall."""
    positives = int(test_size * pos_rate)
    negatives = test_size - positives

    tp = int(round(recall * positives))
    fn = positives - tp
    # precision = tp / (tp + fp)  =>  fp = tp / precision - tp
    fp = int(round(tp / precision - tp)) if precision > 0 else 0
    fp = min(fp, negatives)
    tn = negatives - fp

    return np.array([[tn, fp], [fn, tp]])


def plot_confusion_matrix(cm: np.ndarray, title: str, colorscale: str) -> go.Figure:
    labels = ["Failure (0)", "Success (1)"]
    fig = px.imshow(
        cm,
        text_auto=True,
        x=labels,
        y=labels,
        color_continuous_scale=colorscale,
        labels=dict(x="Predicted", y="Actual", color="Count"),
    )
    fig.update_layout(
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E7ECF7"},
        height=380,
        margin=dict(l=30, r=30, t=60, b=30),
        coloraxis_showscale=False,
    )
    return fig


cm_rf = build_confusion_matrix(0.9183, 0.9393, TEST_SIZE, POS_RATE)
cm_gb = build_confusion_matrix(0.9071, 0.9954, TEST_SIZE, POS_RATE)

cm1, cm2 = st.columns(2)
with cm1:
    st.plotly_chart(plot_confusion_matrix(cm_rf, "Random Forest — Confusion Matrix", "Purples"), use_container_width=True)
with cm2:
    st.plotly_chart(plot_confusion_matrix(cm_gb, "Gradient Boosting — Confusion Matrix", "Greens"), use_container_width=True)

st.write("")

# --------------------------------------------------------------------------
# Final verdict
# --------------------------------------------------------------------------
st.markdown('<div class="section-label">Conclusion</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="card">
        <h4>🏆 Final Model Selected: Gradient Boosting</h4>
        <p>
            Gradient Boosting was selected as the production model. It outperforms
            Random Forest on accuracy (90.37% vs 86.96%), F1-score (94.92% vs 92.87%),
            and ROC-AUC (0.767 vs 0.709), while training over <b>2x faster</b>
            (10.62s vs 24.33s). Its substantially higher recall (99.54%) makes it
            especially effective at correctly identifying startups likely to succeed,
            which is the priority outcome for this use case.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_footer()
