"""
model_utils.py
---------------
Model loading, feature preparation, and prediction helpers for the
Startup Success Prediction System.

The app expects a trained scikit-learn compatible model pickled at
``startup_model.pkl`` (placed at the project root, alongside Home.py).
The model is expected to accept a single-row pandas DataFrame whose
columns mirror the training feature set:

    funding_total_usd, funding_rounds, company_age, funding_duration,
    category, country, state   (categorical columns may be label/one-hot
    encoded upstream depending on how the pipeline was trained)

Because the exact preprocessing pipeline used during training is not
shipped with this app, ``predict_status`` tries a few reasonable input
shapes and falls back to a transparent, clearly-labeled heuristic
"demo mode" if the real model cannot be loaded or the schema does not
match -- this keeps the UI fully functional for demonstration while
being honest with the user about what is happening.
"""

from __future__ import annotations

import os
import pickle
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd
import streamlit as st

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "startup_model.pkl")

CATEGORY_OPTIONS = [
    "Software", "E-Commerce", "Biotechnology", "Fintech", "Healthcare",
    "Mobile", "Hardware", "Enterprise Software", "Education", "Gaming",
    "Clean Technology", "Social Media", "Advertising", "Analytics", "Other",
]

COUNTRY_OPTIONS = [
    "USA", "United Kingdom", "Canada", "India", "Germany", "France",
    "China", "Israel", "Australia", "Singapore", "Pakistan", "Other",
]

STATE_OPTIONS = [
    "California", "New York", "Texas", "Massachusetts", "Washington",
    "Florida", "Illinois", "Not Applicable / Outside US", "Other",
]


@dataclass
class PredictionResult:
    """Container for a single prediction outcome."""
    label: str                 # "Success" or "Failure"
    success_probability: float  # 0-1
    failure_probability: float  # 0-1
    confidence: float           # 0-1, max of the two probabilities
    demo_mode: bool             # True if the real model wasn't used


@st.cache_resource(show_spinner=False)
def load_model():
    """Load the pickled model from disk.

    Returns
    -------
    object or None
        The unpickled model object, or None if it could not be loaded.
    """
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None
    except Exception:
        # Corrupt file, version mismatch, etc.
        return None


def _build_feature_frame(
    funding_total_usd: float,
    funding_rounds: int,
    company_age: float,
    funding_duration: float,
    category: str,
    country: str,
    state: str,
) -> pd.DataFrame:
    """Assemble a single-row DataFrame matching the expected training schema."""
    return pd.DataFrame(
        [{
            "funding_total_usd": funding_total_usd,
            "funding_rounds": funding_rounds,
            "company_age": company_age,
            "funding_duration": funding_duration,
            "category": category,
            "country": country,
            "state": state,
        }]
    )


def _heuristic_probability(
    funding_total_usd: float,
    funding_rounds: int,
    company_age: float,
    funding_duration: float,
) -> float:
    """A transparent, simple heuristic used only when no real model is available.

    This is NOT a trained model -- it is a small logistic-style function over
    normalized inputs so the demo UI still produces a plausible, varying
    probability instead of a hard-coded number.
    """
    funding_score = np.log1p(max(funding_total_usd, 0)) / 18.0      # ~0-1
    rounds_score = min(funding_rounds, 8) / 8.0
    age_score = 1.0 - min(abs(company_age - 5), 10) / 10.0           # sweet spot ~5 yrs
    duration_score = min(funding_duration, 6) / 6.0

    raw = (
        0.40 * funding_score
        + 0.25 * rounds_score
        + 0.15 * age_score
        + 0.20 * duration_score
    )
    raw = np.clip(raw, 0.02, 0.98)
    return float(raw)


def predict_status(
    model,
    funding_total_usd: float,
    funding_rounds: int,
    company_age: float,
    funding_duration: float,
    category: str,
    country: str,
    state: str,
) -> PredictionResult:
    """Run a prediction using the loaded model, with a safe fallback path.

    Parameters
    ----------
    model : object or None
        The loaded model (from `load_model`), or None.
    Other parameters mirror the form fields collected on the Prediction page.

    Returns
    -------
    PredictionResult
    """
    features = _build_feature_frame(
        funding_total_usd, funding_rounds, company_age, funding_duration,
        category, country, state,
    )

    if model is not None:
        try:
            proba = model.predict_proba(features)[0]
            # Assume class order [0, 1] -> [failure, success]; fall back safely.
            classes = list(getattr(model, "classes_", [0, 1]))
            success_idx = classes.index(1) if 1 in classes else 1
            failure_idx = classes.index(0) if 0 in classes else 0
            success_p = float(proba[success_idx])
            failure_p = float(proba[failure_idx])
            label = "Success" if success_p >= failure_p else "Failure"
            confidence = max(success_p, failure_p)
            return PredictionResult(label, success_p, failure_p, confidence, demo_mode=False)
        except Exception:
            # Fall through to numeric-only encoding attempt, then heuristic.
            try:
                numeric_only = features[
                    ["funding_total_usd", "funding_rounds", "company_age", "funding_duration"]
                ]
                proba = model.predict_proba(numeric_only)[0]
                success_p = float(proba[-1])
                failure_p = float(1 - success_p)
                label = "Success" if success_p >= failure_p else "Failure"
                confidence = max(success_p, failure_p)
                return PredictionResult(label, success_p, failure_p, confidence, demo_mode=False)
            except Exception:
                pass  # drop to heuristic fallback below

    # ---- Fallback: transparent demo heuristic ----
    success_p = _heuristic_probability(
        funding_total_usd, funding_rounds, company_age, funding_duration
    )
    failure_p = 1 - success_p
    label = "Success" if success_p >= failure_p else "Failure"
    confidence = max(success_p, failure_p)
    return PredictionResult(label, success_p, failure_p, confidence, demo_mode=True)
