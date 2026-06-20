"""
pages/1_Startup_Prediction.py
------------------------------
Page 2: Interactive prediction form. Collects startup attributes from the
user, loads the trained model (startup_model.pkl), and displays the
predicted outcome with success/failure probabilities and confidence.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.graph_objects as go

from utils.styling import inject_global_css, render_footer
from utils.model_utils import (
    load_model,
    predict_status,
    CATEGORY_OPTIONS,
    COUNTRY_OPTIONS,
    STATE_OPTIONS,
)

st.set_page_config(
    page_title="Startup Prediction | Startup Success Prediction System",
    page_icon="🔮",
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

/* form submit button text fix */
.stForm button {
    color: black !important;
    font-weight: 600 !important;
}

/* extra safety for inner text */
.stForm button * {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* Headings (Enter Startup Details etc.) */
h1, h2, h3 {
    color: white !important;
}

/* Field labels (Funding, Category etc.) */
label, .stTextInput label, .stSelectbox label {
    color: white !important;
}

/* Streamlit widget labels (important fix) */
[data-testid="stWidgetLabel"] {
    color: white !important;
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
    
    # 3. Note: The items "Page: Startup Prediction" and "Final Model..." 
    # have been removed as requested.
    
    st.caption("Final Model: **Gradient Boosting**")
    st.caption("Dataset size: **~64,000 records**")


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <span class="hero-eyebrow">Live Inference</span>
        <h1>🔮 Startup Prediction</h1>
        <p>Enter a startup's funding and profile information below to estimate
        its probability of success using the trained Gradient Boosting model.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Load model (cached) and warn the user transparently if unavailable
# --------------------------------------------------------------------------
model = load_model()
if model is None:
    st.warning(
        "⚠️ Could not find or load **startup_model.pkl** in the project root. "
        "The app will run in **Demo Mode**, generating illustrative predictions "
        "using a transparent heuristic instead of the trained model. "
        "Place your trained model file at the project root to enable real predictions.",
        icon="⚠️",
    )

# --------------------------------------------------------------------------
# Input form
# --------------------------------------------------------------------------
st.markdown('<div class="section-label">Startup Information</div>', unsafe_allow_html=True)
st.markdown("## Enter Startup Details")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        funding_total_usd = st.number_input(
            "💰 Funding Total (USD)",
            min_value=0.0,
            max_value=1_000_000_000.0,
            value=1_000_000.0,
            step=50_000.0,
            help="Total cumulative funding raised by the startup, in US dollars.",
        )
        funding_rounds = st.number_input(
            "🔁 Funding Rounds",
            min_value=0,
            max_value=20,
            value=2,
            step=1,
            help="Total number of distinct funding rounds the startup has closed.",
        )
        company_age = st.number_input(
            "📅 Company Age (years)",
            min_value=0.0,
            max_value=60.0,
            value=5.0,
            step=0.5,
            help="Number of years since the company was founded.",
        )
        funding_duration = st.number_input(
            "⏳ Funding Duration (years)",
            min_value=0.0,
            max_value=30.0,
            value=2.0,
            step=0.5,
            help="Time span between the first and last funding rounds.",
        )

    with col2:
        category = st.selectbox(
            "🏷️ Category / Industry",
            options=CATEGORY_OPTIONS,
            index=0,
            help="Primary industry or business category of the startup.",
        )
        country = st.selectbox(
            "🌍 Country",
            options=COUNTRY_OPTIONS,
            index=0,
            help="Country where the startup is headquartered.",
        )
        state = st.selectbox(
            "📍 State / Region",
            options=STATE_OPTIONS,
            index=0,
            help="State or region of headquarters (where applicable).",
        )

    st.write("")
    submitted = st.form_submit_button("🔍 Predict Startup Outcome", use_container_width=True)

# --------------------------------------------------------------------------
# Prediction & results
# --------------------------------------------------------------------------
if submitted:
    try:
        result = predict_status(
            model=model,
            funding_total_usd=funding_total_usd,
            funding_rounds=int(funding_rounds),
            company_age=company_age,
            funding_duration=funding_duration,
            category=category,
            country=country,
            state=state,
        )

        st.markdown('<div class="section-label">Prediction Result</div>', unsafe_allow_html=True)
        st.markdown("## Result")

        if result.demo_mode:
            st.caption("🧪 Generated in Demo Mode (heuristic, not the trained model).")

        if result.label == "Success":
            st.markdown(
                f"""
                <div class="result-success">
                    ✅ Predicted Outcome: <u>SUCCESS</u> — this startup profile shows
                    strong indicators of long-term viability.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="result-failure">
                    ❌ Predicted Outcome: <u>FAILURE</u> — this startup profile shows
                    elevated risk indicators based on the model.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ---- Probability metrics ----
        m1, m2, m3 = st.columns(3)
        m1.metric("Success Probability", f"{result.success_probability * 100:.2f}%")
        m2.metric("Failure Probability", f"{result.failure_probability * 100:.2f}%")
        m3.metric("Model Confidence", f"{result.confidence * 100:.2f}%")

        # ---- Probability gauge chart ----
        gauge_color = "#1FBF8F" if result.label == "Success" else "#FF5C6C"
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=result.success_probability * 100,
                number={"suffix": "%", "font": {"color": "#E7ECF7"}},
                title={"text": "Success Probability", "font": {"color": "#9BA8C7", "size": 16}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#9BA8C7"},
                    "bar": {"color": gauge_color},
                    "bgcolor": "rgba(0,0,0,0)",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 40], "color": "rgba(255,92,108,0.25)"},
                        {"range": [40, 70], "color": "rgba(255,196,0,0.18)"},
                        {"range": [70, 100], "color": "rgba(31,191,143,0.25)"},
                    ],
                },
            )
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            margin=dict(l=30, r=30, t=60, b=10),
            font={"color": "#E7ECF7"},
        )
        st.plotly_chart(fig, use_container_width=True)

        # ---- Probability bar chart ----
        bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=["Success", "Failure"],
                    y=[result.success_probability * 100, result.failure_probability * 100],
                    marker_color=["#1FBF8F", "#FF5C6C"],
                    text=[f"{result.success_probability*100:.2f}%", f"{result.failure_probability*100:.2f}%"],
                    textposition="outside",
                )
            ]
        )
        bar_fig.update_layout(
            title="Success vs Failure Probability",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#E7ECF7"},
            yaxis=dict(title="Probability (%)", range=[0, 100], gridcolor="rgba(255,255,255,0.08)"),
            xaxis=dict(title=""),
            height=380,
            margin=dict(l=30, r=30, t=60, b=30),
            showlegend=False,
        )
        st.plotly_chart(bar_fig, use_container_width=True)

        with st.expander("📋 View Submitted Startup Profile"):
            st.json(
                {
                    "funding_total_usd": funding_total_usd,
                    "funding_rounds": int(funding_rounds),
                    "company_age": company_age,
                    "funding_duration": funding_duration,
                    "category": category,
                    "country": country,
                    "state": state,
                }
            )

    except Exception as e:
        st.error(
            f"❌ Something went wrong while generating the prediction. "
            f"Please check your inputs and try again.\n\nDetails: {e}",
            icon="🚨",
        )

render_footer()
