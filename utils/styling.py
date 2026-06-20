"""
styling.py
-----------
Centralized styling and shared utility helpers for the Startup Success
Prediction System. Keeping CSS and small reusable functions here means
every page renders with a consistent, professional look.

Design tokens
-------------
Background   : #0B1220 (deep navy)   - panels: #121A2B / #161F33
Accent (core): #5B8CFF (electric indigo)
Success      : #1FBF8F (emerald)
Failure      : #FF5C6C (coral red)
Neutral text : #E7ECF7 / #9BA8C7 (muted)
Display font : "Sora" (headings)      Body font: "Inter"
"""

import streamlit as st


def inject_global_css() -> None:
    """Inject the global CSS theme used across all pages.

    Call this once near the top of every page (after `st.set_page_config`).
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        :root{
            --bg:#0B1220;
            --panel:#121A2B;
            --panel-2:#161F33;
            --border:rgba(255,255,255,0.07);
            --accent:#5B8CFF;
            --accent-2:#8B7CFF;
            --success:#1FBF8F;
            --failure:#FF5C6C;
            --text:#E7ECF7;
            --muted:#9BA8C7;
        }

        html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

        .stApp {
            background: radial-gradient(1200px 600px at 10% -10%, #16213d 0%, #0B1220 55%) fixed;
            color: var(--text);
        }

        h1, h2, h3, h4 {
            font-family: 'Sora', sans-serif !important;
            letter-spacing: -0.01em;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0E1626 0%, #0A0F1C 100%);
            border-right: 1px solid var(--border);
        }
        section[data-testid="stSidebar"] * { color: var(--text) !important; }

        /* Hero banner */
        .hero {
            padding: 2.6rem 2.4rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(91,140,255,0.16), rgba(139,124,255,0.06));
            border: 1px solid var(--border);
            margin-bottom: 1.6rem;
        }
        .hero-eyebrow {
            display:inline-block;
            font-size:0.75rem;
            font-weight:700;
            letter-spacing:0.12em;
            text-transform:uppercase;
            color: var(--accent);
            background: rgba(91,140,255,0.12);
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            margin-bottom: 0.9rem;
        }
        .hero h1 {
            font-size: 2.6rem;
            margin: 0 0 0.6rem 0;
            background: linear-gradient(90deg, #FFFFFF, #AFC2FF);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .hero p { color: var(--muted); font-size: 1.05rem; max-width: 760px; }

        /* Generic card */
        .card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.4rem 1.5rem;
            height: 100%;
        }
        .card h4 { margin-top:0; color: var(--text); }
        .card p { color: var(--muted); font-size: 0.93rem; line-height:1.5; }

        /* Metric chips */
        .chip {
            display:inline-flex;
            align-items:center;
            gap:0.4rem;
            background: var(--panel-2);
            border: 1px solid var(--border);
            padding: 0.45rem 0.9rem;
            border-radius: 999px;
            font-size: 0.85rem;
            color: var(--text);
            margin: 0.2rem 0.4rem 0.2rem 0;
        }

        /* Result banners */
        .result-success, .result-failure {
            padding: 1.4rem 1.6rem;
            border-radius: 14px;
            font-size: 1.15rem;
            font-weight: 700;
            margin: 1rem 0;
            border: 1px solid var(--border);
        }
        .result-success {
            background: linear-gradient(135deg, rgba(31,191,143,0.18), rgba(31,191,143,0.04));
            color: #6FE7C5;
        }
        .result-failure {
            background: linear-gradient(135deg, rgba(255,92,108,0.18), rgba(255,92,108,0.04));
            color: #FF9CA6;
        }

        /* Section divider label */
        .section-label {
            color: var(--accent);
            font-weight: 700;
            font-size: 0.78rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.3rem;
        }

        /* Footer */
        .footer-note {
            color: var(--muted);
            font-size: 0.8rem;
            text-align: center;
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }

        /* Tighten default Streamlit paddings a touch */
        .block-container { padding-top: 2rem; padding-bottom: 3rem; }

        /* Dataframe / table polish */
        .stDataFrame { border-radius: 12px; overflow: hidden; }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.4rem;
            font-weight: 700;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(91,140,255,0.35);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render a consistent footer at the bottom of a page."""
    st.markdown(
        """
        <div class="footer-note">
            Startup Success Prediction System &middot; Built with Streamlit &amp; Gradient Boosting &middot;
            For educational / portfolio purposes
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str, icon: str = "") -> str:
    """Return HTML markup for a simple styled card.

    Parameters
    ----------
    title : str
        Card heading text.
    body : str
        Card body / description text.
    icon : str, optional
        An emoji or short icon glyph shown next to the title.
    """
    return f"""
    <div class="card">
        <h4>{icon}&nbsp; {title}</h4>
        <p>{body}</p>
    </div>
    """
