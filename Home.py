"""
Home.py
--------
Entry point for the Startup Success Prediction System.

Run with:
    streamlit run Home.py

This is page 1 of 3:
    1) Home                       (this file)
    2) Startup Prediction         (pages/1_Startup_Prediction.py)
    3) Model Comparison Dashboard (pages/2_Model_Comparison.py)
"""

import sys
import os

sys.path.append(os.path.dirname(__file__))

import streamlit as st
from utils.styling import inject_global_css, render_footer, card

# --------------------------------------------------------------------------
# Page configuration (must be the first Streamlit call on this page)
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Startup Success Prediction System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
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

</style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
        /* Sidebar ke andar jo bhi icons hain, unka filter khatam karo */
        [data-testid="stSidebar"] span[data-testid="stIcon"], 
        [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] span {
            filter: none !important;
            -webkit-filter: none !important;
            opacity: 1 !important;
            transition: none !important;
        }
        
        /* Agar emoji hai, toh usay force karo ke wo apna original color dikhaye */
        [data-testid="stSidebar"] p {
            color: white !important;
        }
        /* Headings (Enter Startup Details etc.) */
h1, h2, h3 {
    color: white !important;
}
    </style>
""", unsafe_allow_html=True)
inject_global_css()

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    # 1. Top Heading
    st.markdown("""
<div style="text-align:center; padding:10px;">
    <h1>🚀 Startup Success</h1>
    <h3 style="color:gray;">📊 Prediction System</h3>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    
    # 2. Your specific navigation
    st.markdown("#### Navigation")
    st.page_link("Home.py", label="Home", icon="🏠")
    st.page_link("pages/1_Startup_Prediction.py", label="Startup Prediction", icon="🔮")
    st.page_link("pages/2_Model_Comparison.py", label="Model Comparison", icon="📊")
    
    st.markdown("---")
    
    # 3. Note: The items "Page: Startup Prediction" and "Final Model..." 
    # have been removed as requested.
    
    st.caption("Final Model: **Gradient Boosting**")
    st.caption("Dataset size: **~64,000 records**")

# --------------------------------------------------------------------------
# Hero section
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <span class="hero-eyebrow">Machine Learning &middot; Binary Classification</span>
        <h1>🚀 Startup Success Prediction System</h1>
        <p>
            A data-driven decision support tool that estimates the probability of a
            startup succeeding or failing, based on its funding profile, company age,
            and categorical attributes such as industry, country, and state.
            Built end-to-end with a trained Gradient Boosting Classifier.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Quick stat chips
# --------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="card"><h4>📦 Dataset Size</h4><p style="font-size:1.6rem;font-weight:800;color:#E7ECF7;">~64,000</p><p>Startup records used for training &amp; evaluation</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card"><h4>🧠 Models Trained</h4><p style="font-size:1.6rem;font-weight:800;color:#E7ECF7;">2</p><p>Random Forest &amp; Gradient Boosting</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="card"><h4>🏆 Final Model</h4><p style="font-size:1.6rem;font-weight:800;color:#6FE7C5;">Gradient Boosting</p><p>Selected for best overall performance</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="card"><h4>🎯 ROC-AUC</h4><p style="font-size:1.6rem;font-weight:800;color:#E7ECF7;">0.767</p><p>On the held-out test set</p></div>', unsafe_allow_html=True)

st.write("")

# --------------------------------------------------------------------------
# Project overview
# --------------------------------------------------------------------------
st.markdown('<div class="section-label">Project Overview</div>', unsafe_allow_html=True)
st.markdown("## What this project does")

left, right = st.columns([1.2, 1])
with left:
    st.markdown(
        """
        The **Startup Success Prediction System** uses historical startup data
        (funding history, company age, industry category, and geography) to
        predict whether a startup is likely to **succeed** or **fail**.

        Early-stage investors, accelerators, and founders rarely have a simple,
        consistent way to gauge venture risk from structured data alone. This
        project frames that gap as a **supervised binary classification problem**
        and solves it with a tuned Gradient Boosting Classifier, trained on
        nearly 64,000 historical startup records.
        """
    )
with right:
    st.markdown(
        card(
            "Business Problem",
            "Investors and founders need a fast, consistent, data-backed way to "
            "estimate a startup's likelihood of success before committing time "
            "or capital — reducing reliance on intuition alone.",
            "💼",
        ),
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------------------------------
# Objectives
# --------------------------------------------------------------------------
st.markdown('<div class="section-label">Project Objectives</div>', unsafe_allow_html=True)
st.markdown("## Objectives")

o1, o2, o3 = st.columns(3)
with o1:
    st.markdown(
        card(
            "Predictive Modeling",
            "Build and compare multiple classification models to predict "
            "startup outcome (success vs. failure) from funding and "
            "categorical features.",
            "🎯",
        ),
        unsafe_allow_html=True,
    )
with o2:
    st.markdown(
        card(
            "Model Selection",
            "Evaluate models on accuracy, precision, recall, F1-score, and "
            "ROC-AUC to select the most reliable model for deployment.",
            "⚖️",
        ),
        unsafe_allow_html=True,
    )
with o3:
    st.markdown(
        card(
            "Usable Tool",
            "Package the final model behind an interactive Streamlit app so "
            "non-technical users can get instant, explainable predictions.",
            "🛠️",
        ),
        unsafe_allow_html=True,
    )

st.write("")

# --------------------------------------------------------------------------
# Dataset & modeling summary
# --------------------------------------------------------------------------
st.markdown('<div class="section-label">Data &amp; Modeling Summary</div>', unsafe_allow_html=True)
st.markdown("## Dataset & Models")

d1, d2 = st.columns(2)
with d1:
    st.markdown(
        card(
            "Dataset",
            "Approximately <b>64,000</b> startup records with features including "
            "<code>funding_total_usd</code>, <code>funding_rounds</code>, "
            "<code>company_age</code>, <code>funding_duration</code>, plus "
            "categorical fields for industry category, country, and state. "
            "Target: <code>status</code> (1 = Success, 0 = Failure).",
            "📊",
        ),
        unsafe_allow_html=True,
    )
with d2:
    st.markdown(
        """
        <div class="card">
            <h4>🧪 Models Trained</h4>
            <p>Two ensemble tree-based classifiers were trained and compared:</p>
            <span class="chip">🌲 Random Forest</span>
            <span class="chip">⚡ Gradient Boosting</span>
            <p style="margin-top:0.6rem;">
                <b>Gradient Boosting</b> was selected as the final production model
                based on its superior accuracy, F1-score, and ROC-AUC.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.info(
    "👉 Use the **sidebar navigation** to try a live prediction on the "
    "**Startup Prediction** page, or explore detailed metrics on the "
    "**Model Comparison Dashboard** page.",
    icon="ℹ️",
)

render_footer()
