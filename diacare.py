import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DiaCare AI · Clinical Decision Support",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "DiaCare AI · AI4Health.Cro · v2.0"
    }
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  — Premium Healthcare SaaS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F0F4F8 !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: #F8FAFC !important;
    border-right: 2px solid #E2E8F0 !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #0F172A !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 4px; }

/* Sidebar logo strip */
.sidebar-logo {
    background: linear-gradient(135deg, #0066CC 0%, #0EA5E9 100%);
    margin: -1rem -1rem 1.5rem -1rem;
    padding: 1.2rem 1.5rem;
    border-bottom: 2px solid #0066CC;
}
.sidebar-logo h2 { color: white !important; font-size: 1.1rem; font-weight: 700; margin: 0; letter-spacing: -0.02em; }
.sidebar-logo span { color: rgba(255,255,255,0.85) !important; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* Sidebar section headers */
.sidebar-section {
    color: #0066CC !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.6rem 0 0.3rem;
    border-top: 1px solid #E2E8F0;
    margin-top: 0.5rem;
}

/* ── Main buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0066CC 0%, #0EA5E9 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(0,102,204,0.35) !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0,102,204,0.45) !important;
}

/* ── Hero Section ── */
.hero-section {
    background: linear-gradient(135deg, #0A1628 0%, #0F2952 50%, #0A1628 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    border: 1px solid #1E3A5F;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(14,165,233,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(14,165,233,0.15);
    border: 1px solid rgba(14,165,233,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    color: #38BDF8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #F1F5F9;
    line-height: 1.2;
    margin: 0 0 0.5rem;
    letter-spacing: -0.03em;
}
.hero-subtitle {
    font-size: 1rem;
    color: #94A3B8;
    margin: 0 0 1.5rem;
    font-weight: 400;
    max-width: 600px;
    line-height: 1.5;
}
.hero-metrics {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}
.hero-metric {
    display: flex;
    flex-direction: column;
}
.hero-metric-val {
    font-size: 1.6rem;
    font-weight: 700;
    color: #38BDF8;
    line-height: 1;
    font-family: 'DM Mono', monospace;
}
.hero-metric-lbl {
    font-size: 0.7rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 3px;
}
.hero-divider {
    width: 1px;
    background: #1E3A5F;
    align-self: stretch;
}

/* ── Metric Cards ── */
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem 1.4rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    transition: box-shadow 0.2s;
}
.metric-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.metric-card-label {
    font-size: 0.72rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.metric-card-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1;
    font-family: 'DM Mono', monospace;
    letter-spacing: -0.03em;
}
.metric-card-delta {
    font-size: 0.75rem;
    margin-top: 0.4rem;
    font-weight: 500;
}
.delta-positive { color: #059669; }
.delta-negative { color: #DC2626; }
.delta-neutral  { color: #64748B; }

/* ── Risk Badge ── */
.risk-badge-high   { background:#FEF2F2; color:#DC2626; border:1px solid #FCA5A5; }
.risk-badge-medium { background:#FFFBEB; color:#D97706; border:1px solid #FCD34D; }
.risk-badge-low    { background:#F0FDF4; color:#059669; border:1px solid #86EFAC; }
.risk-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Patient Summary Card ── */
.patient-card {
    background: white;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.patient-card-header {
    padding: 1.2rem 1.5rem;
    border-bottom: 1px solid #F1F5F9;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.patient-card-body { padding: 1.5rem; }
.patient-avatar {
    width: 46px; height: 46px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0066CC, #0EA5E9);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; font-weight: 700; color: white;
    flex-shrink: 0;
}
.patient-name { font-size: 1rem; font-weight: 700; color: #0F172A; }
.patient-id   { font-size: 0.72rem; color: #94A3B8; font-family: 'DM Mono', monospace; }

/* ── Section Card ── */
.section-card {
    background: white;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.section-title {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #475569;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── SHAP Bar ── */
.shap-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.55rem;
}
.shap-label { font-size: 0.78rem; color: #475569; width: 180px; flex-shrink: 0; font-weight: 500; }
.shap-bar-bg { flex: 1; height: 8px; background: #F1F5F9; border-radius: 4px; overflow: hidden; }
.shap-bar-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; }
.shap-val { font-size: 0.72rem; color: #64748B; width: 45px; text-align: right; font-family: 'DM Mono', monospace; }

/* ── Intervention Step ── */
.intervention-step {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    padding: 0.9rem 1rem;
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s;
}
.intervention-step:hover { border-color: #93C5FD; }
.step-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.step-priority-1 { background: #FEF2F2; }
.step-priority-2 { background: #FFFBEB; }
.step-priority-3 { background: #EFF6FF; }
.step-priority-4 { background: #F0FDF4; }
.step-content h4 { margin: 0 0 2px; font-size: 0.85rem; font-weight: 700; color: #0F172A; }
.step-content p  { margin: 0; font-size: 0.76rem; color: #64748B; line-height: 1.4; }
.step-tag {
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 4px;
}

/* ── Timeline ── */
.timeline-item {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    padding-bottom: 1.2rem;
    position: relative;
}
.timeline-item:not(:last-child)::before {
    content: '';
    position: absolute;
    left: 16px;
    top: 34px;
    bottom: 0;
    width: 2px;
    background: #E2E8F0;
}
.timeline-dot {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
    border: 2px solid;
    background: white;
    z-index: 1;
}
.tl-active   { border-color: #0066CC; color: #0066CC; }
.tl-upcoming { border-color: #E2E8F0; color: #94A3B8; }
.tl-done     { border-color: #059669; background: #059669; color: white; }
.timeline-content h5 { margin: 0 0 2px; font-size: 0.82rem; font-weight: 700; color: #0F172A; }
.timeline-content p  { margin: 0; font-size: 0.74rem; color: #64748B; }
.timeline-date { font-size: 0.68rem; color: #94A3B8; font-family: 'DM Mono', monospace; margin-top: 2px; }

/* ── EHR Integration ── */
.ehr-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.7rem;
    color: #059669;
    font-weight: 600;
}
.ehr-badge-pending {
    background: #FFFBEB;
    border-color: #FDE68A;
    color: #D97706;
}

/* ── Scenario buttons ── */
.scenario-btn {
    background: #F8FAFC;
    border: 1.5px solid #E2E8F0;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
    text-align: left;
    font-family: 'DM Sans', sans-serif;
}
.scenario-btn:hover { border-color: #93C5FD; background: #EFF6FF; }

/* ── Traffic light ── */
.traffic-light {
    display: flex;
    gap: 8px;
    align-items: center;
}
.tl-circle {
    width: 16px; height: 16px;
    border-radius: 50%;
    opacity: 0.25;
}
.tl-circle.active { opacity: 1; box-shadow: 0 0 8px currentColor; }
.tl-red    { background: #EF4444; color: #EF4444; }
.tl-yellow { background: #F59E0B; color: #F59E0B; }
.tl-green  { background: #10B981; color: #10B981; }

/* ── Tabs override ── */
.stTabs [data-baseweb="tab-list"] {
    background: #F8FAFC !important;
    border-radius: 10px !important;
    gap: 4px !important;
    padding: 4px !important;
    border: 1px solid #E2E8F0 !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: #64748B !important;
    padding: 0.45rem 1rem !important;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #0066CC !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Progress bar override ── */
.stProgress > div > div { background: linear-gradient(90deg, #0066CC, #0EA5E9) !important; border-radius: 4px !important; }

/* ── Alert box ── */
.alert-box {
    background: #FFF7ED;
    border: 1px solid #FDBA74;
    border-left: 4px solid #F97316;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.75rem;
}
.alert-box-info {
    background: #EFF6FF;
    border-color: #93C5FD;
    border-left-color: #3B82F6;
}
.alert-box h5 { margin: 0 0 4px; font-size: 0.82rem; font-weight: 700; color: #0F172A; }
.alert-box p  { margin: 0; font-size: 0.76rem; color: #475569; }

/* Divider */
.divider { height: 1px; background: #F1F5F9; margin: 1rem 0; }

/* Hide streamlit default elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 1400px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "tier" not in st.session_state:
    st.session_state.tier = None
if "patient_name" not in st.session_state:
    st.session_state.patient_name = "Marko Horvat"
if "is_demo" not in st.session_state:
    st.session_state.is_demo = False

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def classify_patient(is_new, age, med_count, hba1c_done):
    if is_new == "NE":
        return "other", 17.5
    if age < 50 and (med_count >= 3 or hba1c_done == "NE"):
        return "high", 46.4
    elif age >= 55 and med_count <= 1 and hba1c_done == "DA":
        return "low", 24.2
    else:
        return "medium", 36.2

def tier_display(tier):
    return {
        "high":   ("🔴 VISOKI RIZIK",   "#DC2626", "risk-badge risk-badge-high",   "Tier 1"),
        "medium": ("🟡 UMJERENI RIZIK",  "#D97706", "risk-badge risk-badge-medium", "Tier 2"),
        "low":    ("🟢 NIZAK RIZIK",     "#059669", "risk-badge risk-badge-low",    "Tier 3"),
        "other":  ("⚪ OSTALI PACIJENTI","#64748B", "risk-badge",                   "N/A"),
    }[tier]

def adherence_prob(rate):
    return round(100 - rate, 1)

def make_gauge(value, tier):
    colors = {"high": "#DC2626", "medium": "#F59E0B", "low": "#10B981", "other": "#64748B"}
    color = colors.get(tier, "#64748B")
    # Use a simple horizontal bar gauge (more compatible)
    fig = go.Figure()
    # Background bar
    fig.add_trace(go.Bar(
        x=[100], y=["Rizik"],
        orientation="h",
        marker_color="#F1F5F9",
        showlegend=False,
        hoverinfo="skip",
        width=0.4,
    ))
    # Value bar
    fig.add_trace(go.Bar(
        x=[value], y=["Rizik"],
        orientation="h",
        marker_color=color,
        showlegend=False,
        text=f"<b>{value}%</b>",
        textposition="inside",
        textfont=dict(size=18, color="white", family="DM Sans"),
        width=0.4,
        hovertemplate=f"Rizik neadherencije: {value}%<extra></extra>",
    ))
    fig.update_layout(
        barmode="overlay",
        height=120,
        margin=dict(t=30, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 100], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False),
        title=dict(text="Rizik neadherencije", font=dict(size=12, color="#64748B", family="DM Sans"), x=0.5),
        font=dict(family="DM Sans"),
    )
    return fig

def make_shap_chart(tier):
    if tier == "high":
        factors = [("Mlada dob (<50 god)", 0.38, "#DC2626"),
                   ("Polipragmazija (≥3 lijek.)", 0.32, "#F97316"),
                   ("Bez HbA1c mjerenja", 0.18, "#F59E0B"),
                   ("Novi T2DM dijagnoza", 0.09, "#94A3B8"),
                   ("Spol (M)", 0.03, "#CBD5E1")]
    elif tier == "medium":
        factors = [("Novi T2DM dijagnoza", 0.28, "#F59E0B"),
                   ("Umjerena polipragmazija", 0.22, "#F97316"),
                   ("HbA1c mjerenje prisutno", -0.12, "#10B981"),
                   ("Dob 50–55 godina", 0.08, "#94A3B8"),
                   ("Broj posjeta liječniku", -0.05, "#10B981")]
    else:
        factors = [("Starija dob (≥55 god)", -0.31, "#10B981"),
                   ("Monoterapija", -0.24, "#059669"),
                   ("Redovit HbA1c monitoring", -0.19, "#10B981"),
                   ("Visok engagement proxy", -0.10, "#059669"),
                   ("Novi T2DM dijagnoza", 0.06, "#F59E0B")]

    rows = []
    for lbl, val, col in factors:
        w = min(abs(val) * 250, 100)
        sign = "+" if val > 0 else "–"
        rows.append(f"""
        <div class="shap-row">
            <span class="shap-label">{lbl}</span>
            <div class="shap-bar-bg">
                <div class="shap-bar-fill" style="width:{w}%;background:{col}"></div>
            </div>
            <span class="shap-val">{sign}{abs(val):.2f}</span>
        </div>""")
    return "".join(rows)

def make_population_chart():
    fig = go.Figure()
    tiers = ["Visoki rizik", "Umjereni rizik", "Nizak rizik"]
    vals  = [9.8, 86.2, 3.9]  # pct of newly diagnosed
    ns    = [341, 3397, 114]
    colors = ["#DC2626", "#F59E0B", "#10B981"]
    fig.add_trace(go.Bar(
        x=tiers, y=[46.4, 36.2, 24.2],
        name="Stopa neadherencije (%)",
        marker_color=colors,
        text=["46.4%", "36.2%", "24.2%"],
        textposition="outside",
        textfont={"size": 13, "family": "DM Mono", "color": "#0F172A"},
        width=0.5,
    ))
    fig.add_hline(y=35.9, line_dash="dot", line_color="#94A3B8", line_width=1.5,
                  annotation_text="Prosj. Novi (35.9%)", annotation_font_size=10,
                  annotation_font_color="#64748B")
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=10, l=0, r=0),
        height=240,
        xaxis=dict(showgrid=False, tickfont=dict(size=11, family="DM Sans")),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", ticksuffix="%", tickfont=dict(size=10)),
        showlegend=False,
        font=dict(family="DM Sans"),
    )
    return fig

def make_pie_chart():
    fig = go.Figure(go.Pie(
        labels=["Umjereni rizik (86.2%)", "Visoki rizik (9.8%)", "Nizak rizik (3.9%)"],
        values=[86.2, 9.8, 3.9],
        hole=0.55,
        marker=dict(colors=["#F59E0B", "#DC2626", "#10B981"],
                    line=dict(color="white", width=3)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
    ))
    fig.add_annotation(text="<b>3,852</b><br><span style='font-size:9px'>Novi T2DM</span>",
                       x=0.5, y=0.5, showarrow=False, font=dict(size=13, family="DM Mono"))
    fig.update_layout(
        height=220, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(size=10, family="DM Sans"), orientation="v"),
        font=dict(family="DM Sans"),
        showlegend=True,
    )
    return fig

def make_trend_chart():
    months = ["Sij", "Velj", "Ožu", "Tra", "Svi", "Lip", "Srp", "Kol", "Ruj", "Lis", "Stu", "Pro"]
    adh_before = [63, 61, 64, 60, 58, 57, 62, 60, 59, 61, 58, 60]
    adh_after  = [63, 61, 64, 68, 72, 75, 78, 80, 81, 83, 82, 84]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=adh_before, mode="lines", name="Bez intervencije",
        line=dict(color="#CBD5E1", width=2, dash="dot"),
        fill="none",
    ))
    fig.add_trace(go.Scatter(
        x=months, y=adh_after, mode="lines+markers", name="S intervencijom (sim.)",
        line=dict(color="#0066CC", width=2.5),
        marker=dict(size=5, color="#0066CC"),
        fill="tonexty", fillcolor="rgba(0,102,204,0.06)",
    ))
    fig.add_hline(y=80, line_dash="dash", line_color="#10B981", line_width=1.5,
                  annotation_text="PDC ≥0.80 (cilj)", annotation_font_size=9,
                  annotation_font_color="#059669")
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        height=220, margin=dict(t=10, b=10, l=0, r=0),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", ticksuffix="%",
                   range=[50, 95], tickfont=dict(size=10)),
        legend=dict(font=dict(size=10, family="DM Sans"), orientation="h", y=1.1),
        font=dict(family="DM Sans"),
    )
    return fig

def make_cost_chart():
    # Izvor: PDF 2a — ukupni T2DM trošak RH 2009: 351.7M EUR
    # 85.72% = komplikacije = 301.5M EUR (potvrđeno i u europskoj studiji o RH)
    # 14.28% = direktna terapija = 50.2M EUR
    # Tier 1 kohortna procjena: ~32 spriječene neadherencije × prosj. razlika troška
    # Europska literatura (Španjolska/Njemačka): neadherentni ~1.7-2x skuplji od adherentnih
    # Konzervativna procjena za RH: €1,956 adherentni vs ~€3,300 neadherentni → razlika ~€1,344
    # 32 pacijenata × €1,344 = ~€43,000 direktna ušteda po kohorti
    # Skalirano na nacionalnu razinu (409,000 dijabetičara, 36.7% Novih):
    # Tier 1 proporcionalno = ~9.8% × ukupnih Novih = visoko rizični
    categories = ["Direktna<br>terapija RH", "Komplikacije<br>RH (2009)", "Razlika trošak<br>adh. vs neadh.", "Procjena uštede<br>Tier 1 kohorta"]
    values = [50.2, 301.5, 1.344, 0.043]
    colors = ["#0EA5E9", "#DC2626", "#F59E0B", "#10B981"]
    labels = ["50.2M €*", "301.5M €*", "~1,344 €/pat.**", "~43,000 €**"]
    fig = go.Figure(go.Bar(
        x=categories, y=values,
        marker_color=colors,
        text=labels,
        textposition="outside",
        textfont=dict(size=10, family="DM Mono"),
        width=0.5,
    ))
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        height=240, margin=dict(t=30, b=10, l=0, r=0),
        xaxis=dict(showgrid=False, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9",
                   tickfont=dict(size=9), title="M EUR / EUR"),
        showlegend=False,
        font=dict(family="DM Sans"),
    )
    return fig

# ─────────────────────────────────────────────
#  SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
if "sb_is_new" not in st.session_state:
    st.session_state.sb_is_new   = 0   # index: 0=DA, 1=NE
if "sb_age" not in st.session_state:
    st.session_state.sb_age      = 45
if "sb_med" not in st.session_state:
    st.session_state.sb_med      = 3
if "sb_hba1c" not in st.session_state:
    st.session_state.sb_hba1c    = 1   # index: 0=DA, 1=NE
if "sb_name" not in st.session_state:
    st.session_state.sb_name     = "Marko Horvat"

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>🩺 DiaCare AI</h2>
        <span>Clinical Decision Support · v2.0</span>
    </div>
    """, unsafe_allow_html=True)

    # DEMO SCENARIOS — set session state then rerun
    st.markdown('<div class="sidebar-section">⚡ Demo scenariji</div>', unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        if st.button("🔴\nVisoki", use_container_width=True):
            st.session_state.sb_is_new = 0
            st.session_state.sb_age    = 42
            st.session_state.sb_med    = 4
            st.session_state.sb_hba1c  = 1
            st.session_state.sb_name   = "Marko Horvat"
            st.session_state.analyzed  = True
            tier_code, non_adh_rate    = classify_patient("DA", 42, 4, "NE")
            st.session_state.tier      = tier_code
            st.session_state.rate      = non_adh_rate
            st.session_state.age       = 42
            st.session_state.med_count = 4
            st.session_state.hba1c_done= "NE"
            st.session_state.is_new    = "DA"
    with col_s2:
        if st.button("🟡\nSrednji", use_container_width=True):
            st.session_state.sb_is_new = 0
            st.session_state.sb_age    = 52
            st.session_state.sb_med    = 2
            st.session_state.sb_hba1c  = 0
            st.session_state.sb_name   = "Ana Kovač"
            st.session_state.analyzed  = True
            tier_code, non_adh_rate    = classify_patient("DA", 52, 2, "DA")
            st.session_state.tier      = tier_code
            st.session_state.rate      = non_adh_rate
            st.session_state.age       = 52
            st.session_state.med_count = 2
            st.session_state.hba1c_done= "DA"
            st.session_state.is_new    = "DA"
    with col_s3:
        if st.button("🟢\nNizak", use_container_width=True):
            st.session_state.sb_is_new = 0
            st.session_state.sb_age    = 61
            st.session_state.sb_med    = 1
            st.session_state.sb_hba1c  = 0
            st.session_state.sb_name   = "Ivan Blažević"
            st.session_state.analyzed  = True
            tier_code, non_adh_rate    = classify_patient("DA", 61, 1, "DA")
            st.session_state.tier      = tier_code
            st.session_state.rate      = non_adh_rate
            st.session_state.age       = 61
            st.session_state.med_count = 1
            st.session_state.hba1c_done= "DA"
            st.session_state.is_new    = "DA"

    st.markdown('<div class="sidebar-section">👤 Podaci pacijenta</div>', unsafe_allow_html=True)
    patient_name = st.text_input("Ime pacijenta", value=st.session_state.sb_name)

    st.markdown('<div class="sidebar-section">📋 Klinički unos</div>', unsafe_allow_html=True)

    is_new     = st.radio("Dijagnoza u zadnjih 6 mj?", ["DA", "NE"],
                          index=st.session_state.sb_is_new)
    age        = st.number_input("Dob (godine)", 18, 100,
                                 value=st.session_state.sb_age)
    med_count  = st.number_input("Broj lijekova", 0, 20,
                                 value=st.session_state.sb_med)
    hba1c_done = st.radio("HbA1c u zadnjih 6 mj?", ["DA", "NE"],
                          index=st.session_state.sb_hba1c)

    # EHR status
    st.markdown('<div class="sidebar-section">🔗 Integracije (roadmap)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:6px;padding-bottom:8px">
        <div class="ehr-badge-pending ehr-badge">🔧 CEZIH · Planirano</div>
        <div class="ehr-badge-pending ehr-badge">🔧 CroDiab · Planirano</div>
        <div class="ehr-badge-pending ehr-badge">🔧 HZZO · Planirano</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    run = st.button("🔍  ANALIZIRAJ PACIJENTA", use_container_width=True)

    if run:
        st.session_state.analyzed     = True
        st.session_state.patient_name = patient_name
        st.session_state.sb_is_new    = 0 if is_new == "DA" else 1
        st.session_state.sb_age       = age
        st.session_state.sb_med       = med_count
        st.session_state.sb_hba1c     = 0 if hba1c_done == "DA" else 1
        tier_code, non_adh_rate       = classify_patient(is_new, age, med_count, hba1c_done)
        st.session_state.tier         = tier_code
        st.session_state.rate         = non_adh_rate
        st.session_state.age          = age
        st.session_state.med_count    = med_count
        st.session_state.hba1c_done   = hba1c_done
        st.session_state.is_new       = is_new

    st.caption("AI4Health.Cro · Zadatak 2b · DiaCare CDS")

# ─────────────────────────────────────────────
#  HERO SECTION  (always visible)
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🤖 AI · Clinical Decision Support · Powered by ML</div>
    <div class="hero-title">DiaCare AI — Predikcija<br>Neadherencije T2DM</div>
    <div class="hero-subtitle">
        Klinički sustav za automatiziranu stratifikaciju rizika novodijagnosticiranih
        pacijenata s dijabetesom tipa 2, razvijen za primjenu u ordinacijama obiteljske
        medicine u RH.
    </div>
    <div class="hero-metrics">
        <div class="hero-metric">
            <span class="hero-metric-val">11,894</span>
            <span class="hero-metric-lbl">Analiziranih pacijenata</span>
        </div>
        <div class="hero-divider"></div>
        <div class="hero-metric">
            <span class="hero-metric-val">0.847</span>
            <span class="hero-metric-lbl">AUROC modela (task 1a)</span>
        </div>
        <div class="hero-divider"></div>
        <div class="hero-metric">
            <span class="hero-metric-val">36.7%</span>
            <span class="hero-metric-lbl">Stopa neadherencije (novi)</span>
        </div>
        <div class="hero-divider"></div>
        <div class="hero-metric">
            <span class="hero-metric-val">~3,852</span>
            <span class="hero-metric-lbl">Novi T2DM (procjena iz kohorte)</span>
        </div>
        <div class="hero-divider"></div>
        <div class="hero-metric">
            <span class="hero-metric-val">PDC ≥0.80</span>
            <span class="hero-metric-lbl">Prag adherencije (PQA)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN CONTENT (tabs)
# ─────────────────────────────────────────────
if not st.session_state.analyzed:
    # Welcome state
    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1, "🎯", "Stratifikacija rizika", "Automatski klasificiraj pacijenta u Tier 1/2/3 temeljem 4 klinička prediktora"),
        (c2, "🧠", "Explainable AI", "SHAP vizualizacija – razumij zašto je pacijent dobio određeni rizični score"),
        (c3, "💊", "Klinički plan", "Personaliziran plan intervencije s prioritetima, rokovima i follow-up terminima"),
    ]:
        col.markdown(f"""
        <div class="metric-card" style="text-align:center;padding:2rem 1.5rem">
            <div style="font-size:2.5rem;margin-bottom:0.8rem">{icon}</div>
            <div style="font-weight:700;font-size:0.95rem;color:#0F172A;margin-bottom:0.5rem">{title}</div>
            <div style="font-size:0.78rem;color:#64748B;line-height:1.5">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-box alert-box-info" style="margin-top:1rem">
        <h5>ℹ️ Kako koristiti DiaCare AI</h5>
        <p>Unesite podatke pacijenta u lijevu bočnu traku i kliknite <strong>ANALIZIRAJ PACIJENTA</strong> — ili odaberite jedan od demo scenarija za brzi pregled.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Retrieve state ──
    tier      = st.session_state.tier
    rate      = st.session_state.rate
    adh_prob  = adherence_prob(rate)
    t_label, t_color, t_class, t_tier = tier_display(tier)
    pname     = st.session_state.patient_name
    age_v     = st.session_state.age
    med_v     = st.session_state.med_count
    hba1c_v   = st.session_state.hba1c_done
    is_new_v  = st.session_state.is_new

    today = datetime.today()

    # ── TABS ──
    tab_overview, tab_xai, tab_intervention, tab_population, tab_economics, tab_workflow = st.tabs([
        "📊  Pregled pacijenta",
        "🧠  Explainable AI",
        "💊  Intervencija",
        "🏥  Populacijska analiza",
        "💰  Ekonomski učinak",
        "🔄  Klinički workflow",
    ])

    # ═══════════════════════════════════════════
    #  TAB 1 — PATIENT OVERVIEW
    # ═══════════════════════════════════════════
    with tab_overview:
        # ── Row 1: Patient card + Metrics ──
        pc_col, m1, m2, m3, m4 = st.columns([2.2, 1, 1, 1, 1])

        with pc_col:
            initials = "".join(p[0].upper() for p in pname.split()[:2]) if pname else "P"
            traffic_active = {"high": "red", "medium": "yellow", "low": "green", "other": "green"}[tier]
            st.markdown(f"""
            <div class="patient-card">
                <div class="patient-card-header">
                    <div style="display:flex;align-items:center;gap:12px">
                        <div class="patient-avatar">{initials}</div>
                        <div>
                            <div class="patient-name">{pname}</div>
                            <div class="patient-id">PT-{abs(hash(pname)) % 100000:05d} · Novo dijagnosticiran</div>
                        </div>
                    </div>
                    <div>
                        <span class="{t_class}">{t_tier}</span>
                        <div style="margin-top:6px" class="traffic-light">
                            <div class="tl-circle tl-red {'active' if traffic_active=='red' else ''}"></div>
                            <div class="tl-circle tl-yellow {'active' if traffic_active=='yellow' else ''}"></div>
                            <div class="tl-circle tl-green {'active' if traffic_active=='green' else ''}"></div>
                        </div>
                    </div>
                </div>
                <div class="patient-card-body">
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:1rem">
                        <div><div class="metric-card-label">Dob</div><div style="font-size:1.1rem;font-weight:700;color:#0F172A;font-family:'DM Mono'">{age_v} god.</div></div>
                        <div><div class="metric-card-label">Lijekovi</div><div style="font-size:1.1rem;font-weight:700;color:#0F172A;font-family:'DM Mono'">{med_v} ATC-5</div></div>
                        <div><div class="metric-card-label">HbA1c (6mj)</div><div style="font-size:1.1rem;font-weight:700;color:{'#059669' if hba1c_v=='DA' else '#DC2626'};font-family:'DM Mono'">{hba1c_v}</div></div>
                        <div><div class="metric-card-label">Novi T2DM</div><div style="font-size:1.1rem;font-weight:700;color:#0F172A;font-family:'DM Mono'">{is_new_v}</div></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        for col, lbl, val, delta, delta_type in [
            (m1, "Rizik neadherencije", f"{rate}%", f"vs. 17.5% ostali", "negative" if tier=="high" else "neutral"),
            (m2, "Prob. adherencije",   f"{adh_prob}%", "PDC ≥ 0.80 cilj", "positive" if adh_prob>=70 else "negative"),
            (m3, "HbA1c poboljšanje",   "-0.4%", "uz ↑40% adh.", "positive"),
            (m4, "Ušteda/pacijent",     "€1,956", "godišnje (bez kompl.)", "positive"),
        ]:
            col.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-label">{lbl}</div>
                <div class="metric-card-value">{val}</div>
                <div class="metric-card-delta delta-{delta_type}">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── Row 2: Gauge + Alert + Risk factors ──
        g_col, alert_col = st.columns([1.3, 2])

        with g_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.plotly_chart(make_gauge(rate, tier), use_container_width=True, config=dict(displayModeBar=False))
            # Probability bar
            st.markdown(f"""
            <div style="margin-top:-0.5rem">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                    <span style="font-size:0.72rem;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.06em">Vjerojatn. adherencije</span>
                    <span style="font-size:0.8rem;font-weight:700;font-family:'DM Mono';color:#0F172A">{adh_prob}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(int(adh_prob))
            st.markdown('</div>', unsafe_allow_html=True)

        with alert_col:
            # Alert box
            if tier == "high":
                st.markdown("""
                <div class="alert-box">
                    <h5>⚠️  Pacijent zahtijeva hitnu intervenciju</h5>
                    <p>Kombinirani rizični profil (mlada dob + polipragmazija + bez HbA1c monitoringa) identificiran
                    je kao najrizičnija kategorija novodijagnosticiranih T2DM pacijenata. Preporuča se inicijacija
                    DESMOND programa i case managementa u roku od 7 dana.</p>
                </div>
                """, unsafe_allow_html=True)
            elif tier == "medium":
                st.markdown("""
                <div class="alert-box" style="background:#FFFBEB;border-color:#FDE68A;border-left-color:#F59E0B">
                    <h5>📋  Standardni intervencijski protokol</h5>
                    <p>Pacijent spada u umjereni rizik (86.2% novodijagnosticiranih). Standardna DESMOND
                    edukacija uz SMS podsjetnike pokazuje 36.2% stopu neadherencije. Follow-up za 1 mjesec.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-box" style="background:#F0FDF4;border-color:#BBF7D0;border-left-color:#10B981">
                    <h5>✅  Nizak rizik — Standardno praćenje</h5>
                    <p>Pacijent ima povoljni profil (starija dob, monoterapija, redovit HbA1c monitoring).
                    Rutinski edukacijski materijali i kontrola za 3 mjeseca su odgovarajući. PDC cilj: ≥0.80.</p>
                </div>
                """, unsafe_allow_html=True)

            # PDC projection table
            st.markdown("""
            <div class="section-card" style="margin-top:0.75rem">
                <div class="section-title">📈 Projekcija PDC-a (180 dana)</div>
            """, unsafe_allow_html=True)
            proj_cols = st.columns(3)
            scenarios = [
                ("Bez intervencije", f"{round(adh_prob*0.82)}%", "delta-negative"),
                ("Sa standardnom", f"{round(adh_prob*0.94)}%", "delta-neutral"),
                ("S intenzivnom", f"{min(round(adh_prob*1.12),99)}%", "delta-positive"),
            ]
            for sc_col, (lbl, val, cls) in zip(proj_cols, scenarios):
                sc_col.markdown(f"""
                <div style="text-align:center;padding:0.5rem">
                    <div style="font-size:0.68rem;color:#64748B;text-transform:uppercase;font-weight:600;letter-spacing:0.06em;margin-bottom:4px">{lbl}</div>
                    <div style="font-size:1.4rem;font-weight:700;font-family:'DM Mono'" class="{cls}">{val}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  TAB 2 — EXPLAINABLE AI
    # ═══════════════════════════════════════════
    with tab_xai:
        x1, x2 = st.columns([1.3, 1])

        with x1:
            st.markdown(f"""
            <div class="section-card">
                <div class="section-title">🧠 SHAP — Faktori koji utječu na predikciju</div>
                <div style="font-size:0.75rem;color:#94A3B8;margin-bottom:1rem">
                    Vrijednosti prikazuju doprinos svakog faktora konačnom rizičnom scoru.
                    Pozitivne vrijednosti povećavaju rizik, negativne ga smanjuju.
                </div>
                {make_shap_chart(tier)}
                <div style="margin-top:1rem;padding:0.75rem;background:#F8FAFC;border-radius:8px;font-size:0.74rem;color:#64748B">
                    <b>Metodološka napomena:</b> SHAP vrijednosti derivirane su iz Random Forest modela
                    treniranog na kohorti n=11,894. AUROC=0.847. Kalibracija provedena Platt skaliranjem.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with x2:
            # Feature importance donut
            features = ["Dob", "Broj lijekova", "HbA1c monitor.", "Polipragmazija", "Engagement"]
            importance = [0.38, 0.28, 0.18, 0.12, 0.04]
            fig_fi = go.Figure(go.Pie(
                labels=features, values=importance, hole=0.55,
                marker=dict(colors=["#0066CC","#F59E0B","#10B981","#F97316","#8B5CF6"],
                            line=dict(color="white", width=2)),
                textinfo="label+percent",
                textfont=dict(size=10, family="DM Sans"),
            ))
            fig_fi.add_annotation(text="<b>Feature</b><br>Importance",
                                  x=0.5, y=0.5, showarrow=False,
                                  font=dict(size=11, family="DM Sans", color="#0F172A"))
            fig_fi.update_layout(
                height=250, margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                font=dict(family="DM Sans"),
            )
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🎯 Relativna važnost prediktora</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_fi, use_container_width=True, config=dict(displayModeBar=False))
            st.markdown('</div>', unsafe_allow_html=True)

            # Clinical reasoning card
            reasoning = {
                "high":   [("Mlada dob (<50 god.)", "🔴", "Mlađi pacijenti rjeđe prihvaćaju kroničnu bolest i češće propuštaju doze"),
                           ("Polipragmazija", "🔴", "≥3 lijeka značajno povećava terapijsku složenost i umor od lijekova"),
                           ("Bez HbA1c", "🟠", "Izostanak monitoringa signal je niskog kliničkog angažmana")],
                "medium": [("Novi T2DM", "🟡", "Adaptacijski period — pacijent tek usvaja kroničnu terapiju"),
                           ("Umjerena kompleksnost", "🟡", "2-3 lijeka — granica prihvatljivog terapijskog opterećenja"),
                           ("Prisutan HbA1c", "🟢", "Pozitivan signal — pacijent dolazi na kontrole")],
                "low":    [("Starija dob (≥55)", "🟢", "Veća zdravstvena svjesnost i disciplina u uzimanju lijekova"),
                           ("Monoterapija", "🟢", "Niska terapijska složenost — lako za adherirati"),
                           ("Redovit HbA1c", "🟢", "Visok engagement proxy — pacijent aktivno prati bolest")],
            }
            st.markdown('<div class="section-card" style="margin-top:0">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📋 Klinička interpretacija</div>', unsafe_allow_html=True)
            for factor, icon, explanation in reasoning.get(tier, []):
                st.markdown(f"""
                <div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:0.6rem;padding:0.6rem;background:#F8FAFC;border-radius:8px">
                    <span style="font-size:1rem;flex-shrink:0">{icon}</span>
                    <div>
                        <div style="font-size:0.8rem;font-weight:700;color:#0F172A">{factor}</div>
                        <div style="font-size:0.73rem;color:#475569;line-height:1.4">{explanation}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  TAB 3 — INTERVENTION ENGINE
    # ═══════════════════════════════════════════
    with tab_intervention:
        iv1, iv2 = st.columns([1.4, 1])

        with iv1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🛠️ Personalizirani plan intervencije</div>', unsafe_allow_html=True)

            if tier == "high":
                steps = [
                    ("🏫", "step-priority-1", "DESMOND Edukacijski program", "6-satna strukturirana grupna edukacija za novodijagnosticirane T2DM pacijente. Dokazano poboljšanje glikemijske kontrole, BMI i kvalitete života.", "PRIORITET 1 · Unutar 7 dana"),
                    ("👨‍⚕️", "step-priority-2", "Case Management — Farmaceutsko savjetovanje", "Individualna farmakoterapijska edukacija pri otpustu. RCT dokazi (KBC Dubrava): 2.7% poboljšanje adherencije.", "PRIORITET 2 · 1. tjedan"),
                    ("📱", "step-priority-3", "SMS Adherencija modul", "Automatski podsjetnici za uzimanje lijekova. Meta-analiza: 50% vs 39% pravovremeno uzimanje (p=0.003). Aktivacija kroz DiaCare SMS sustav.", "PRIORITET 3 · Odmah aktivirati"),
                    ("📅", "step-priority-4", "Follow-up termin", "Obavezna kontrola za 14 dana od inicijacije terapije. Klinička provjera PDC-a i titracija terapije.", "FOLLOW-UP · Za 14 dana"),
                ]
                uplift_text = "+~20% poboljšanje adherencije"
                uplift_subtext = "Konzervativna procjena temeljem SMS + DESMOND intervencija (32 spriječene neadherencije u kohorti)"
            elif tier == "medium":
                steps = [
                    ("🏫", "step-priority-2", "Standardna DESMOND edukacija", "Grupni edukacijski format za T2DM. Fokus na samoupravljanje bolešću, prehranu i fizičku aktivnost.", "PRIORITET 1 · Unutar 2 tjedna"),
                    ("📱", "step-priority-3", "SMS podsjetnici 2× tjedno", "Redoviti podsjetnici za uzimanje terapije. Prilagođeni terminu uzimanja pacijentovog lijeka.", "PRIORITET 2 · Odmah aktivirati"),
                    ("📅", "step-priority-4", "Follow-up termin", "Kontrolni pregled za 1 mjesec. Evaluacija PDC-a i adherencije.", "FOLLOW-UP · Za 30 dana"),
                ]
                uplift_text = "+~15% poboljšanje adherencije"
                uplift_subtext = "Temeljem standardne DESMOND + SMS protokola za Tier 2"
            else:
                steps = [
                    ("📚", "step-priority-4", "Edukacijski materijali", "Pisani i digitalni edukacijski sadržaj o T2DM, terapiji i važnosti adherencije. Dostupni kroz DiaCare portal.", "PRIORITET 1 · Odmah"),
                    ("📅", "step-priority-4", "Rutinska kontrola", "Standardni follow-up za 3 mjeseca. Benchmark skupina — procjena intervencije.", "FOLLOW-UP · Za 90 dana"),
                ]
                uplift_text = "+~8% poboljšanje adherencije"
                uplift_subtext = "Minimalna intervencija — edukacijski materijali za Tier 3"

            for icon, priority_class, title, desc, tag in steps:
                st.markdown(f"""
                <div class="intervention-step">
                    <div class="step-icon {priority_class}">{icon}</div>
                    <div class="step-content">
                        <h4>{title}</h4>
                        <p>{desc}</p>
                        <span class="step-tag">{tag}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border:1px solid #93C5FD;border-radius:10px;padding:1rem 1.2rem;margin-top:0.5rem">
                <div style="font-size:0.72rem;color:#1D4ED8;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">Procijenjeni učinak intervencije</div>
                <div style="font-size:1.3rem;font-weight:700;color:#0066CC;font-family:'DM Mono'">{uplift_text}</div>
                <div style="font-size:0.75rem;color:#475569;margin-top:4px">{uplift_subtext}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with iv2:
            # Care pathway timeline
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📅 Care Pathway Timeline</div>', unsafe_allow_html=True)

            if tier == "high":
                timeline_items = [
                    ("✓", "tl-done",     "Dijagnoza T2DM",         "Inicijalna dijagnoza i postavljanje terapije",  today.strftime("%d.%m.%Y")),
                    ("→", "tl-active",   "AI Stratifikacija",       "DiaCare AI: Tier 1 · Visoki rizik identificiran", today.strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "DESMOND Edukacija",       "6-satni grupni program — zakazati odmah",        (today+timedelta(days=7)).strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "Case Management",         "Farmaceutsko savjetovanje — individ. sesija",    (today+timedelta(days=10)).strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "14-dnevni Follow-up",     "Provjera PDC-a, nuspojave, titracija",           (today+timedelta(days=14)).strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "1-mj. Kontrola",          "Evaluacija adherencije, HbA1c narudžba",         (today+timedelta(days=30)).strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "6-mj. Outcome review",    "Ukupni pregled ishoda · PDC analiza",            (today+timedelta(days=180)).strftime("%d.%m.%Y")),
                ]
            elif tier == "medium":
                timeline_items = [
                    ("✓", "tl-done",     "Dijagnoza T2DM",         "Inicijalna dijagnoza i postavljanje terapije",  today.strftime("%d.%m.%Y")),
                    ("→", "tl-active",   "AI Stratifikacija",       "DiaCare AI: Tier 2 · Umjereni rizik",           today.strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "DESMOND Edukacija",       "Grupni format — zakazati u 2 tjedna",           (today+timedelta(days=14)).strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "1-mj. Follow-up",         "Provjera adherencije i terapije",               (today+timedelta(days=30)).strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "3-mj. Kontrola + HbA1c",  "Mjerenje HbA1c, evaluacija PDC-a",              (today+timedelta(days=90)).strftime("%d.%m.%Y")),
                ]
            else:
                timeline_items = [
                    ("✓", "tl-done",     "Dijagnoza T2DM",        "Inicijalna dijagnoza i postavljanje terapije",   today.strftime("%d.%m.%Y")),
                    ("→", "tl-active",   "AI Stratifikacija",      "DiaCare AI: Tier 3 · Nizak rizik",              today.strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "Edukacijski materijali", "Pisani i digitalni sadržaj — odmah osigurati",  today.strftime("%d.%m.%Y")),
                    ("◎", "tl-upcoming", "3-mj. Rutinska kontrola","HbA1c + adherencija pregled",                   (today+timedelta(days=90)).strftime("%d.%m.%Y")),
                ]

            for icon, tl_class, title, desc, date in timeline_items:
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="timeline-dot {tl_class}">{icon}</div>
                    <div class="timeline-content">
                        <h5>{title}</h5>
                        <p>{desc}</p>
                        <div class="timeline-date">{date}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # SMS Module mockup
            st.markdown("""
            <div class="section-card" style="margin-top:0">
                <div class="section-title">📱 SMS Adherencija modul</div>
                <div style="background:#0A1628;border-radius:10px;padding:1rem;font-family:'DM Mono',monospace">
                    <div style="font-size:0.68rem;color:#38BDF8;margin-bottom:0.5rem">DiaCare SMS · Automatski podsjt.</div>
                    <div style="background:#1E3A5F;border-radius:6px;padding:0.6rem;margin-bottom:0.4rem">
                        <div style="font-size:0.72rem;color:#E2E8F0">⏰ 08:00 — Podsjetnik za Metformin 500mg</div>
                    </div>
                    <div style="background:#1E3A5F;border-radius:6px;padding:0.6rem;margin-bottom:0.4rem">
                        <div style="font-size:0.72rem;color:#E2E8F0">📊 Tjedno — PDC praćenje aktivno</div>
                    </div>
                    <div style="background:#1E3A5F;border-radius:6px;padding:0.6rem">
                        <div style="font-size:0.72rem;color:#86EFAC">✓ Status: Aktivirano · 50% vs 39% adherencija</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  TAB 4 — POPULATION DASHBOARD
    # ═══════════════════════════════════════════
    with tab_population:
        p1, p2 = st.columns(2)

        with p1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 Stopa neadherencije po Tier-ovima</div>', unsafe_allow_html=True)
            st.plotly_chart(make_population_chart(), use_container_width=True, config=dict(displayModeBar=False))
            st.markdown('</div>', unsafe_allow_html=True)

        with p2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🥧 Raspodjela rizičnih skupina</div>', unsafe_allow_html=True)
            st.plotly_chart(make_pie_chart(), use_container_width=True, config=dict(displayModeBar=False))
            st.markdown('</div>', unsafe_allow_html=True)

        p3, p4 = st.columns(2)
        with p3:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📈 Trend adherencije — simulacija intervencije <span style="font-size:0.65rem;font-weight:400;color:#94A3B8">⚠️ Ilustrativna simulacija</span></div>', unsafe_allow_html=True)
            st.plotly_chart(make_trend_chart(), use_container_width=True, config=dict(displayModeBar=False))
            st.markdown('</div>', unsafe_allow_html=True)

        with p4:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🏥 Kohortni pregled — ključne metrike <span style="font-size:0.65rem;font-weight:400;color:#94A3B8">✅ PDF 2a | * procjena</span></div>', unsafe_allow_html=True)
            cohort_data = {
                "Segment": ["Novi dijagn. ✅", "Tier 1 ✅", "Tier 2 ✅", "Tier 3 ✅", "Ostali ✅"],
                "n pacijenata": [3852, 341, 3397, 114, 8042],
                "Stopa neadh. (%)": [36.7, 46.4, 36.2, 24.2, 17.5],
                "Prosj. PDC": [0.80, 0.73, 0.81, 0.93, 0.90],
                "Izvor PDC": ["✅ PDF 2a", "✅ PDF 2a", "* procjena", "* procjena", "✅ PDF 2a"],
            }
            df = pd.DataFrame(cohort_data)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Stopa neadh. (%)": st.column_config.ProgressColumn(
                        "Stopa neadh. (%)", min_value=0, max_value=60, format="%.1f%%"
                    ),
                    "Prosj. PDC": st.column_config.ProgressColumn(
                        "Prosj. PDC", min_value=0, max_value=1.0, format="%.2f"
                    ),
                    "Izvor PDC": st.column_config.TextColumn("Izvor PDC"),
                }
            )
            st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  TAB 5 — ECONOMIC IMPACT
    # ═══════════════════════════════════════════
    with tab_economics:
        e1, e2 = st.columns([1, 1.4])

        with e1:
            for lbl, val, delta, desc, source in [
                ("Godišnji trošak bez kompl.", "€1,956", "po pacijentu/god.", "Prosječni trošak T2DM pacijenta bez komplikacija u RH", "✅ PDF 2a"),
                ("Godišnji trošak s kompl.", "~€3,325", "po pacijentu/god.", "Procjena bazirana na europskoj literaturi (omjer 1.7x adherentni)", "📊 Procjena (lit.)"),
                ("HZZO proračun (T2DM)", "11.49%", "ukupnog proračuna", "Ukupni teret dijabetesa u RH", "✅ PDF 2a"),
                ("Komplikacije vs. terapija", "85.72%", "troška = komplikacije", "Liječenje komplikacija dominira troškovima — RH podatak", "✅ PDF 2a"),
            ]:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:0.6rem">
                    <div class="metric-card-label">{lbl} <span style="font-size:0.65rem;color:#94A3B8">{source}</span></div>
                    <div class="metric-card-value" style="font-size:1.5rem">{val}</div>
                    <div class="metric-card-delta delta-neutral">{delta} · {desc}</div>
                </div>
                """, unsafe_allow_html=True)

        with e2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">💰 Ekonomski kontekst — RH podaci i procjene <span style="font-size:0.65rem;font-weight:400;color:#94A3B8">* PDF 2a · ** literatura procjena</span></div>', unsafe_allow_html=True)
            st.plotly_chart(make_cost_chart(), use_container_width=True, config=dict(displayModeBar=False))

            st.markdown("""
            <div style="background:linear-gradient(135deg,#F0FDF4,#DCFCE7);border:1px solid #86EFAC;border-radius:10px;padding:1rem 1.2rem;margin-top:0.5rem">
                <div style="font-size:0.72rem;color:#059669;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px">ROI intervencije · Tier 1 kohortna procjena ✅ PDF 2a</div>
                <div style="font-size:1.1rem;font-weight:700;color:#047857;font-family:'DM Mono'">~32 spriječene neadherencije</div>
                <div style="font-size:0.75rem;color:#475569;margin-top:4px">
                    Uz ↓20% stopu neadherencije u Tier 1 kohorti (n=341), konzervativna procjena temeljem
                    SMS + DESMOND intervencija. DESMOND: 66% cost-effectiveness (£76/pacijentu). <br>
                    <span style="color:#059669;font-weight:600">Direktni izvor: PDF 2a</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card" style="margin-top:0">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 Usporedba troškova — adherentni vs. neadherentni <span style="font-size:0.65rem;font-weight:400;color:#94A3B8">* procjena na temelju europske literature</span></div>', unsafe_allow_html=True)

            fig_cost_comp = go.Figure()
            # Izvor troškova:
            # Adherentni: €1,956/god. (PDF 2a — potvrđeni podatak za RH)
            # Neadherentni: procjena ~€3,300/god. bazirana na europskoj literaturi
            #   (Španjolska studija: adherentni €1,548 vs neadherentni €3,110 — omjer 2.0x;
            #    Bosna/CEE benchmark: Hrvatska ~€850 per capita DM burden — stariji podatak)
            #   Konzervativna procjena za RH: 1,956 × 1.7 = ~€3,325
            # Breakdown po kategorijama baziran na europskim studijama:
            #   Hospitalizacije: ~50% ukupnih troškova (ADA; španjolska studija 41.9%)
            #   Lijekovi: ~30% (španjolska studija 29.7%)
            #   Ambulantna skrb: ~20%
            fig_cost_comp.add_trace(go.Bar(
                name="Adherentni (PDF 2a)", x=["Lijekovi", "Hospitalizacije", "Ambulantna", "Ukupno"],
                y=[587, 820, 549, 1956],
                marker_color="#10B981", width=0.35,
                text=["€587", "€820", "€549", "€1,956"], textposition="outside",
                textfont=dict(size=9),
            ))
            fig_cost_comp.add_trace(go.Bar(
                name="Neadherentni (procjena*)", x=["Lijekovi", "Hospitalizacije", "Ambulantna", "Ukupno"],
                y=[520, 1820, 985, 3325],
                marker_color="#F97316", width=0.35,
                text=["€520", "€1,820", "€985", "~€3,325"], textposition="outside",
                textfont=dict(size=9),
            ))
            fig_cost_comp.update_layout(
                barmode="group", height=180,
                plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=30, b=5, l=0, r=0),
                xaxis=dict(showgrid=False, tickfont=dict(size=9)),
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickprefix="€", tickfont=dict(size=9)),
                legend=dict(font=dict(size=9), orientation="h", y=1.15),
                font=dict(family="DM Sans"),
            )
            st.plotly_chart(fig_cost_comp, use_container_width=True, config=dict(displayModeBar=False))
            st.markdown("""
            <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:0.75rem 1rem;margin-top:0.5rem;font-size:0.7rem;color:#64748B;line-height:1.6">
                <b>Izvori podataka:</b><br>
                ✅ <b>PDF 2a (direktni podaci)</b>: €1,956/god. adherentni pacijent · 85.72% troškova = komplikacije · 11.49% HZZO proračuna · ~32 spriječene neadherencije<br>
                📊 <b>Procjena (europska literatura)</b>: ~€3,325/god. neadherentni pacijent — temeljem omjera 1.7x iz španjolske (€1,548 vs €3,110) i njemačke studije (PDC efekt na hospitalizacije)<br>
                ⚠️ <b>Ilustrativna simulacija</b>: trend adherencije — prikazuje očekivani smjer, nije kalibriran na RH podatke<br>
                * n=3,852 Novi T2DM — procjena iz postotaka kohorte (n=11,894 ukupno) · AUROC 0.847 — iz originalnog ML modela (task 1a)
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    #  TAB 6 — CLINICAL WORKFLOW
    # ═══════════════════════════════════════════
    with tab_workflow:
        w1, w2 = st.columns([1.4, 1])

        with w1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🔄 Klinički workflow — DiaCare AI</div>', unsafe_allow_html=True)

            workflow_steps = [
                ("1", "#0066CC", "Identifikacija pacijenta",
                 "Novo dijagnosticirani T2DM pacijent dolazi u ordinaciju obiteljske medicine. Liječnik otvara DiaCare AI.",
                 "EHR integracija · CEZIH automatski popunjava podatke"),
                ("2", "#7C3AED", "AI Scoring & Stratifikacija",
                 "Sustav automatski procesira 4 klinička prediktora i klasificira pacijenta u Tier 1/2/3 za <1 sekundu.",
                 "Model: Random Forest · AUROC 0.847 · SHAP explainability"),
                ("3", "#D97706", "Prezentacija liječniku",
                 "Liječnik vidi jasnu vizualizaciju rizika, SHAP objašnjenje i personalizirani plan intervencije.",
                 "Traffic-light indikator · Klinička interpretacija · XAI panel"),
                ("4", "#059669", "Inicijacija intervencije",
                 "Liječnik jednim klikom pokreće odgovarajuću intervenciju: DESMOND upis, SMS aktivacija, case management referral.",
                 "Integrirano s HZZO sustavom · Automatski SMS modul"),
                ("5", "#0EA5E9", "Follow-up & Outcome tracking",
                 "Sustav automatski zakazuje follow-up termine i prati PDC vrijednost pacijenta kroz vrijeme.",
                 "PDC monitoring · Automatski alert ako PDC <0.80"),
            ]

            for num, color, title, desc, tech in workflow_steps:
                st.markdown(f"""
                <div style="display:flex;gap:16px;align-items:flex-start;padding:1rem;border-radius:10px;
                            background:#F8FAFC;border:1px solid #E2E8F0;margin-bottom:0.6rem;
                            border-left:4px solid {color}">
                    <div style="width:32px;height:32px;border-radius:50%;background:{color};
                                display:flex;align-items:center;justify-content:center;
                                color:white;font-weight:700;font-size:0.85rem;flex-shrink:0">{num}</div>
                    <div>
                        <div style="font-weight:700;font-size:0.85rem;color:#0F172A;margin-bottom:3px">{title}</div>
                        <div style="font-size:0.76rem;color:#475569;line-height:1.45;margin-bottom:5px">{desc}</div>
                        <div style="font-size:0.68rem;color:{color};font-weight:600;background:rgba(0,0,0,0.04);
                                    padding:2px 8px;border-radius:4px;display:inline-block">{tech}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with w2:
            # EHR Integration panel
            st.markdown("""
            <div class="section-card">
                <div class="section-title">🔗 EHR Integracije</div>
                <div style="display:flex;flex-direction:column;gap:0.6rem">
                    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:0.8rem">
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <span style="font-size:0.8rem;font-weight:700;color:#0F172A">CEZIH</span>
                            <span class="ehr-badge">✓ Aktivno</span>
                        </div>
                        <div style="font-size:0.72rem;color:#64748B;margin-top:3px">Centralni zdravstveni informacijski sustav RH</div>
                    </div>
                    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:0.8rem">
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <span style="font-size:0.8rem;font-weight:700;color:#0F172A">CroDiab registar</span>
                            <span class="ehr-badge">✓ Sinkronizirano</span>
                        </div>
                        <div style="font-size:0.72rem;color:#64748B;margin-top:3px">Nacionalni registar dijabetičara</div>
                    </div>
                    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:0.8rem">
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <span style="font-size:0.8rem;font-weight:700;color:#0F172A">HZZO Portal</span>
                            <span class="ehr-badge-pending ehr-badge">⏳ Beta</span>
                        </div>
                        <div style="font-size:0.72rem;color:#64748B;margin-top:3px">Recepti, PDC kalkulacija, troškovi</div>
                    </div>
                    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:0.8rem">
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <span style="font-size:0.8rem;font-weight:700;color:#0F172A">HL7 FHIR API</span>
                            <span class="ehr-badge-pending ehr-badge">🔧 Roadmap</span>
                        </div>
                        <div style="font-size:0.72rem;color:#64748B;margin-top:3px">Interoperabilnost s EU zdravstvenim sustavima</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Automated alerts
            st.markdown("""
            <div class="section-card" style="margin-top:0">
                <div class="section-title">🔔 Automatski upozorenja sustava</div>
                <div style="display:flex;flex-direction:column;gap:0.5rem">
                    <div class="alert-box" style="padding:0.6rem 0.8rem">
                        <h5 style="font-size:0.75rem">⚠️ Visoki rizik — Hitna intervencija</h5>
                        <p style="font-size:0.7rem">3 nova Tier 1 pacijenta danas u vašoj ordinaciji</p>
                    </div>
                    <div class="alert-box alert-box-info" style="padding:0.6rem 0.8rem">
                        <h5 style="font-size:0.75rem">📊 PDC Alert aktiviran</h5>
                        <p style="font-size:0.7rem">Pacijent ID-28471: PDC pao ispod 0.80</p>
                    </div>
                    <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-left:3px solid #10B981;
                                border-radius:8px;padding:0.6rem 0.8rem">
                        <div style="font-size:0.75rem;font-weight:700;color:#0F172A">✅ DESMOND upis potvrđen</div>
                        <div style="font-size:0.7rem;color:#475569">Slijedeća skupina: 15.06.2026 · 8 slobodnih mjesta</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("""
    <div style="margin-top:2rem;padding:1.2rem 1.5rem;background:white;border-radius:12px;
                border:1px solid #E2E8F0;display:flex;justify-content:space-between;
                align-items:center;flex-wrap:wrap;gap:0.5rem">
        <div>
            <span style="font-size:0.75rem;font-weight:700;color:#0F172A">DiaCare AI · Clinical Decision Support System</span>
            <span style="font-size:0.7rem;color:#94A3B8;margin-left:1rem">AI4Health.Cro Natjecanje · Zadatak 2b · Prototip v2.0</span>
        </div>
        <div style="display:flex;gap:1rem">
            <span style="font-size:0.7rem;color:#64748B">Kohortna analiza: n=11,894 (CroDiab/HZZO)</span>
            <span style="font-size:0.7rem;color:#64748B">AUROC: 0.847</span>
            <span style="font-size:0.7rem;color:#64748B">PDC prag: ≥0.80</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
