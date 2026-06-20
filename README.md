# 🚀 Startup Success Prediction System

A multi-page Streamlit application that predicts whether a startup will
**succeed** or **fail**, using a trained Gradient Boosting Classifier.

## Project Structure

```
startup-success-prediction/
├── Home.py                              # Page 1: Landing page
├── pages/
│   ├── 1_🔮_Startup_Prediction.py       # Page 2: Prediction form
│   └── 2_📊_Model_Comparison.py         # Page 3: Model comparison dashboard
├── utils/
│   ├── __init__.py
│   ├── styling.py                       # Shared CSS theme & UI helpers
│   └── model_utils.py                   # Model loading & prediction logic
├── startup_model.pkl                    # ⚠️ Add your trained model here (not included)
├── requirements.txt
└── README.md
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Place your trained model file at the project root:
   ```
   startup-success-prediction/startup_model.pkl
   ```
   The model should be a scikit-learn compatible classifier (e.g. a
   `GradientBoostingClassifier` or a `Pipeline` ending in one) that exposes
   `predict_proba()`, trained on these features:

   | Feature             | Type        |
   |---------------------|-------------|
   | funding_total_usd   | numeric     |
   | funding_rounds      | numeric     |
   | company_age         | numeric     |
   | funding_duration    | numeric     |
   | category            | categorical |
   | country             | categorical |
   | state               | categorical |

   and target `status` (1 = Success, 0 = Failure).

   > If `startup_model.pkl` is not found (or its schema doesn't match), the
   > Prediction page automatically falls back to a clearly-labeled **Demo Mode**
   > so the UI remains fully functional for demonstration purposes.

3. Run the app:
   ```bash
   streamlit run Home.py
   ```

## Pages

- **🏠 Home** — Project overview, business problem, objectives, dataset & model summary.
- **🔮 Startup Prediction** — Interactive form to predict success/failure with probabilities.
- **📊 Model Comparison Dashboard** — Side-by-side Random Forest vs Gradient Boosting metrics,
  interactive Plotly charts, and confusion matrix visualizations.

## Reported Model Performance

| Metric            | Random Forest | Gradient Boosting |
|--------------------|:-------------:|:------------------:|
| Accuracy           | 86.96%        | **90.37%**         |
| Precision          | **91.83%**    | 90.71%             |
| Recall             | 93.93%        | **99.54%**         |
| F1 Score           | 92.87%        | **94.92%**         |
| ROC-AUC            | 0.709         | **0.767**          |
| Training Time      | 24.33s        | **10.62s**         |

**Final model selected: Gradient Boosting Classifier.**
