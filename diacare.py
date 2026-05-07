import streamlit as st

# Postavke stranice
st.set_page_config(page_title="DiaCare AI - Final T2DM", page_icon="💊")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #d32f2f; color: white; font-weight: bold; height: 3em; }
    .tier-card { padding: 20px; border-radius: 12px; background-color: white; border: 1px solid #eee; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 DiaCare: Klinički AI Kopilot")
st.write("Specijalizirana trijaža za novo dijagnosticirane T2DM pacijente (n=11.894).")

# --- SIDEBAR: PREDIKTORI ---
st.sidebar.header("📋 Parametri pacijenta")
with st.sidebar:
    is_new = st.checkbox("Novo dijagnosticirani (prva godina)", value=True)
    age = st.slider("Dob pacijenta:", 18, 90, 45)
    atc_count = st.number_input("Broj ATC-5 lijekova (180 dana):", 1, 15, 4)
    hba1c_count = st.radio("Broj HbA1c mjerenja (180 dana):", [0, 1, 2, "3+"])
    st.markdown("---")
    btn = st.button("ANALIZIRAJ RIZIK")

# --- STATISTIKE IZ GRAFIKA (3_1.png i 3_2.png) ---
risk_data = {
    'Visoki': {
        'pop_pct': '9.8%', 'median_pdc': 0.82, 'neadherencija': '46.4%', 
        'color': '#C0392B', 'tier': 'TIER 1 - Visoki rizik'
    },
    'Umjereni': {
        'pop_pct': '86.2%', 'median_pdc': 0.91, 'neadherencija': '36.2%', 
        'color': '#E67E22', 'tier': 'TIER 2 - Umjereni rizik'
    },
    'Nizak': {
        'pop_pct': '3.9%', 'median_pdc': 0.97, 'neadherencija': '24.2%', 
        'color': '#27AE60', 'tier': 'TIER 3 - Nizak rizik'
    }
}

if btn:
    if not is_new:
        st.info("Pacijent pripada skupini 'Ostali' (Dugogodišnji T2DM). Rizik neadherencije: 17.5%.")
    else:
        # Logika bodovanja temeljena na Metodološkoj osnovi (2_2.png)
        score = 0
        if age < 50: score += 1
        if atc_count >= 3: score += 1
        if hba1c_count == 0: score += 1
        
        # Određivanje Tiera
        if score >= 2: tier_res = risk_data['Visoki']
        elif score == 1: tier_res = risk_data['Umjereni']
        else: tier_res = risk_data['Nizak']
        
        # Izračun vjerovatnoće adherencije (1 - stopa neadherencije iz 2_3.png)
        prob_val = 1 - float(tier_res['neadherencija'].strip('%'))/100

        # PRIKAZ REZULTATA
        st.markdown(f"""
            <div class="tier-card" style="border-left: 10px solid {tier_res['color']};">
                <h2 style="color: {tier_res['color']}; margin-top:0;">{tier_res['tier']}</h2>
                <p>Udio u populaciji Novih: <b>{tier_res['pop_pct']}</b></p>
                <hr>
                <table style="width:100%; font-size: 1.1em;">
                    <tr>
                        <td><b>AI Adherence Score (Vjerojatnost):</b></td>
                        <td style="text-align:right;"><b>{prob_val:.1%}</b></td>
                    </tr>
                    <tr>
                        <td><b>Medijan PDC segmenta:</b></td>
                        <td style="text-align:right;">{tier_res['median_pdc']:.2f}</td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

        st.progress(prob_val)
        
        # Klinička i poslovna preporuka
        if tier_res['neadherencija'] == '46.4%':
            st.error("🚨 **KLINIČKI PRIORITET:** Skoro svaki drugi pacijent u ovom segmentu će postati neadherentan. Potrebna hitna intervencija.")
        else:
            st.success("✅ **STATUS:** Pacijent pokazuje dobar potencijal za adherenciju. Nastaviti s podrškom.")

    st.caption("🛡️ Model validiran na SPE podacima. Distribucija i boxplot analize (n=11.894).")