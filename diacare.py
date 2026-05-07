import streamlit as st

# Postavke stranice - Profesionalni medicinski stil
st.set_page_config(page_title="DiaCare AI - Klinička Podrška", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { background-color: #1e40af; color: white; border-radius: 8px; font-weight: 600; }
    .risk-card { padding: 25px; border-radius: 15px; background-color: white; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .benefit-box { background-color: #eff6ff; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 DiaCare: Sustav za podršku odlučivanju (CDS)")
st.caption("Alat za automatiziranu stratifikaciju rizika novo dijagnosticiranih T2DM pacijenata u RH.")

# --- SIDEBAR: INPUT VARIJABLE (Prema odjeljku 6.2 dokumenta) ---
st.sidebar.header("📋 Klinički ulazni podaci")
with st.sidebar:
    # 4 ključne varijable iz odjeljka 6.2 [cite: 304]
    is_new = st.radio("Je li dijagnoza postavljena u posljednjih 6 mjeseci?", ["DA", "NE"])
    age = st.number_input("Dob pacijenta (godine):", 18, 100, 45)
    med_count = st.number_input("Broj različitih lijekova u tekućoj terapiji:", 0, 20, 3)
    hba1c_done = st.radio("HbA1c mjerenje u posljednjih 6 mjeseci?", ["DA", "NE"])
    st.markdown("---")
    run_analysis = st.button("POKRENI STRATIFIKACIJU")

# --- LOGIKA I PRIKAZ (Prema odjeljku 6.3 i 6.4 dokumenta) ---
if run_analysis:
    if is_new == "NE":
        tier_label = "Ostali pacijenti (Dugogodišnji)"
        rate = "17.5%"
        color = "#64748b"
        plan = ["Standardni protokol praćenja i kontrole."]
    else:
        # Logika iz vašeg dokumenta (Odjeljak 6.3)
        if age < 50 and (med_count >= 3 or hba1c_done == "NE"):
            tier_label = "VISOKI RIZIK (Tier 1)"
            rate = "46.4%"
            color = "#ef4444"
            plan = [
                "**DESMOND program:** 6-satna grupna edukacija [cite: 270]",
                "**Case management:** Individualno farmaceutsko savjetovanje [cite: 272]",
                "**Digitalna podrška:** SMS podsjetnici (povećanje adherencije na 50%) [cite: 273]",
                "**Follow-up:** Obavezan pregled za 14 dana [cite: 275]"
            ]
        elif age > 55 and med_count <= 1 and hba1c_done == "DA":
            tier_label = "NIZAK RIZIK (Tier 3)"
            rate = "24.2%"
            color = "#22c55e"
            plan = ["Edukacijski materijali (pisani i digitalni)", "Rutinska kontrola za 3 mjeseca [cite: 282]"]
        else:
            tier_label = "UMJERENI RIZIK (Tier 2)"
            rate = "36.2%"
            color = "#f59e0b"
            plan = ["Standardna DESMOND edukacija", "SMS podsjetnici 2x tjedno", "Follow-up za 1 mjesec [cite: 279]"]

    # --- GLAVNI PRIKAZ REZULTATA ---
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown(f"""
            <div class="risk-card" style="border-top: 10px solid {color};">
                <h3 style="color: {color}; margin: 0;">{tier_label}</h3>
                <p style="font-size: 1.1em; color: #475569;">Očekivana stopa neadherencije: <b>{rate}</b></p>
                <hr>
                <p><b>Napomena:</b> Rana adherencija stvara <i>'Legacy Effect'</i> koji smanjuje rizik od budućih komplikacija.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.metric("Potencijal poboljšanja HbA1c", "-0.1%", "za svakih +10% adherencije")

    with col2:
        st.subheader("🛠️ Predloženi plan intervencije")
        for step in plan:
            st.markdown(f"- {step}")
        
        st.markdown(f"""
            <div class="benefit-box">
                <b>Ekonomska opravdanost:</b><br>
                Liječenje komplikacija čini 85,72% troškova dijabetesa u RH[cite: 163]. 
                Godišnji trošak pacijenta bez komplikacija iznosi cca <b>1.956 EUR</b>.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Izvor podataka: Analiza kohorte n=11.894 (CroDiab / HZZO) | DiaCare CDS Prototip V1.0")
else:
    st.info("Molimo unesite podatke o pacijentu kako biste generirali plan intervencije.")