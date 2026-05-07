import streamlit as st

# Postavke stranice
st.set_page_config(page_title="DiaCare AI - Tier Segmentation", page_icon="💊")

# Prilagođeni stilovi
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #004a99; color: white; font-weight: bold; }
    .result-box { padding: 20px; border-radius: 12px; background-color: white; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 DiaCare: Tiered Risk Predictor")
st.write("Personalizirana procjena rizika za novo dijagnosticirane pacijente (T2DM).")

# --- SIDEBAR: KLINIČKI PREDIKTORI ---
st.sidebar.header("📋 Klinički prediktori (Zadatak 2a)")

with st.sidebar:
    is_new = st.checkbox("Novo dijagnosticirani pacijent", value=True, help="Pacijent koji je u indeksnom periodu prvi put zaprimio lijek.")
    age = st.slider("Dob pacijenta:", 18, 90, 45)
    atc_count = st.number_input("Broj različitih ATC-5 lijekova (180d):", 0, 15, 4)
    hba1c_measured = st.selectbox("Broj mjerenja HbA1c u 180 dana:", [0, 1, 2, "3+"])
    st.markdown("---")
    analyze = st.button("POKRENI SEGMENTACIJU")

# --- PODACI O STOPAMA NEADHERENCIJE ---
# Podaci prema Grafičkom prikazu 4
tiers = {
    'Visoki rizik': {'rate': 0.464, 'color': '#C0392B', 'label': 'TIER 1 - Visoki rizik'},
    'Umjereni rizik': {'rate': 0.362, 'color': '#E67E22', 'label': 'TIER 2 - Umjereni rizik'},
    'Nizak rizik': {'rate': 0.242, 'color': '#27AE60', 'label': 'TIER 3 - Nizak rizik'},
    'Ostali': {'rate': 0.175, 'color': '#2E86C1', 'label': 'Dugogodišnji pacijenti'}
}

if analyze:
    if not is_new:
        res = tiers['Ostali']
        prob_adherence = 1 - res['rate'] # 82.5%
        preporuka = "Standardni protokol praćenja za dugogodišnje pacijente."
    else:
        # Logika segmentacije unutar Novo dijagnosticiranih
        # Bodovni sistem za potrebe demo prikaza
        score = 0
        if age < 50: score += 1
        if atc_count >= 3: score += 1
        if hba1c_measured == 0: score += 1

        if score >= 2:
            res = tiers['Visoki rizik']
            preporuka = "HITNA INTERVENCIJA: Strukturirana edukacija i intenzivno praćenje (Legacy Effect)."
        elif score == 1:
            res = tiers['Umjereni rizik']
            preporuka = "POJAČAN NADZOR: Uključivanje u programe samomenadžmenta."
        else:
            res = tiers['Nizak rizik']
            preporuka = "EDUKACIJA: Osnaživanje pacijenta za nastavak dobre adherencije."

        prob_adherence = 1 - res['rate']

    # --- PRIKAZ ---
    st.markdown(f"""
        <div class="result-box" style="border-left: 10px solid {res['color']};">
            <h2 style="color: {res['color']}; margin-top:0;">{res['label']}</h2>
            <p style="font-size: 1.1em;">Stopa neadherencije segmenta: <b>{res['rate']:.1%}</b></p>
            <hr>
            <table style="width:100%;">
                <tr>
                    <td><b>Vjerovatnoća adherencije (AI Score):</b></td>
                    <td style="text-align:right; font-weight:bold;">{prob_adherence:.1%}</td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

    st.progress(prob_adherence)
    st.info(f"**📢 Klinička preporuka:** {preporuka}")
    
    if res['rate'] > 0.35:
        st.error(f"💰 **ROI FOKUS:** Ovaj segment doprinosi visokim troškovima komplikacija (85.72% proračuna).")

    st.caption("🛡️ Analiza provedena na kohorti od 11.894 pacijenta. Prosječna stopa neadherencije Novih je 35.9%.")