import streamlit as st

# Postavke stranice za profesionalni medicinski izgled
st.set_page_config(page_title="DiaCare AI - Final CDS Tool", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { width: 100%; background-color: #004a99; color: white; font-weight: bold; border-radius: 8px; height: 3.5em; }
    .metric-card { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e6ed; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .intervention-card { background-color: #ffffff; padding: 25px; border-radius: 15px; border-left: 10px solid #004a99; }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 DiaCare: Klinički AI sustav za podršku odlučivanju (CDS)")
st.write("Personalizirana stratifikacija rizika i plan intervencije za novo dijagnosticirane T2DM pacijente.")

# --- SIDEBAR: ULAZNE VARIJABLE (Izvor: 6_1.png / 6_2.png) ---
st.sidebar.header("📋 Ulazni podaci o pacijentu")
with st.sidebar:
    is_new_dx = st.radio("Dijagnoza postavljena u posljednjih 6 mjeseci?", ["DA", "NE"])
    age = st.number_input("Dob pacijenta (godine):", 18, 100, 45)
    drug_count = st.number_input("Broj različitih lijekova u tekućoj terapiji:", 0, 20, 4)
    hba1c_present = st.radio("HbA1c mjerenje u posljednjih 6 mjeseci?", ["DA", "NE"])
    st.markdown("---")
    if st.button("POKRENI ANALIZU"):
        st.session_state.analyzed = True

# --- LOGIKA STRATIFIKACIJE (Izvor: 6_1.png) ---
if st.session_state.get('analyzed'):
    if is_new_dx == "NE":
        tier = "Ostali"
        rate = "17.5%"
        risk_label = "STABILAN RIZIK"
        color = "#2E86C1"
        plan = ["Standardni protokol praćenja (svakih 6-12 mjeseci)."]
    else:
        # Primjena logike iz odjeljka 6.3 dokumenta
        if age < 50 and (drug_count >= 3 or hba1c_present == "NE"):
            tier = "Visoki rizik"
            rate = "46.4%"
            risk_label = "VISOKI RIZIK (TIER 1)"
            color = "#C0392B"
            plan = [
                "**DESMOND program:** Šestosatna strukturirana edukacija",
                "**Case management:** Individualno farmaceutsko savjetovanje",
                "**SMS podsjetnici:** Automatizirana podrška (poboljšava adherenciju do 50%)",
                "**Follow-up:** Obavezan pregled za 2 tjedna"
            ]
        elif age >= 55 and drug_count <= 1 and hba1c_present == "DA":
            tier = "Nizak rizik"
            rate = "24.2%"
            risk_label = "NIZAK RIZIK (TIER 3)"
            color = "#27AE60"
            plan = ["Edukacijski materijali (pisani + digitalni)", "Rutinski follow-up za 3 mjeseca"]
        else:
            tier = "Umjereni rizik"
            rate = "36.2%"
            risk_label = "UMJERENI RIZIK (TIER 2)"
            color = "#E67E22"
            plan = [
                "Standardna DESMOND edukacija u grupi",
                "SMS podsjetnici 2x tjedno",
                "Follow-up za 1 mjesec"
            ]

    # --- PRIKAZ REZULTATA ---
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown(f"""
            <div class="metric-card" style="border-top: 8px solid {color};">
                <h3 style="color: {color}; margin-bottom: 5px;">{risk_label}</h3>
                <p style="font-size: 1.2em;">Procijenjena neadherencija: <b>{rate}</b></p>
                <hr>
                <p><b>Pacijent profil:</b> Novo dijagnosticirani T2DM</p>
                <p><b>Target PDC prag:</b> ≥ 0.80</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.metric("Povezanost s ishodom", "-0.1% HbA1c", "po +10% adherencije", delta_color="normal")

    with col2:
        st.markdown(f"""<div class="intervention-card">
            <h4>📋 Preporučeni plan intervencije</h4>""", unsafe_allow_html=True)
        for p in plan:
            st.write(p)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- EKONOMSKI OKVIR (Izvor: 5_1.png) ---
    st.markdown("---")
    st.subheader("📊 Ekonomska i klinička opravdanost")
    ec1, ec2, ec3 = st.columns(3)
    ec1.metric("Trošak komplikacija u RH", "85.72%", "ukupnih izdataka T2DM")
    ec2.metric("Trošak intervencije (cca)", "£76", "po pacijentu")
    ec3.metric("Godišnja ušteda", "1.750 EUR", "per adherentni pacijent")

    st.caption("🛡️ Trustworthy AI: Procjena utemeljena na modelu validiranom unutar SPE okruženja na 11.894 pacijenata.")
else:
    st.info("Dobrodošli u DiaCare CDS alat. Unesite parametre pacijenta u izbornik s lijeve strane za početak trijaže.")