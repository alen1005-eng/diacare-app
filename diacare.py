import streamlit as st

# Postavke stranice
st.set_page_config(page_title="DiaCare AI - Clinical Intervention", page_icon="💊")

st.markdown("""
    <style>
    .report-card { padding: 25px; border-radius: 15px; background-color: white; border: 1px solid #eee; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .intervention-box { background-color: #f0f7ff; padding: 15px; border-radius: 8px; border-left: 5px solid #2e86c1; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 DiaCare: Klinička AI Intervencija")
st.write("Stratificirani pristup poboljšanju adherencije temeljen na risk tierima.")

# --- SIDEBAR: PRECIZNI UNOS ---
st.sidebar.header("📋 Profil pacijenta")
with st.sidebar:
    age = st.slider("Dob pacijenta:", 18, 95, 40)
    atc_count = st.number_input("Broj ATC-5 lijekova (180 dana):", 0, 20, 6)
    hba1c_val = st.number_input("Broj HbA1c mjerenja (180 dana):", 0.0, 10.0, 0.0, step=0.1)
    st.markdown("---")
    analyze = st.button("GENERIRAJ KLINIČKI PLAN")

# --- PODACI IZ ANALIZE (4_1.png i 4_2.png) ---
if analyze:
    # Logika dodjele tiera prema karakteristikama iz 4_1.png
    if age < 50 and hba1c_val < 1.0:
        tier = "Tier 1: Visoki rizik"
        n_pac = 341
        rate = "46.4%"
        color = "#d32f2f"
        # Intervencije iz 4_2.png
        plan = [
            "**Strukturirana edukacija:** DESMOND program (6-satni grupni program)",
            "**Case management:** Individualno farmaceutsko savjetovanje",
            "**Digitalna podrška:** SMS podsjetnici (dokazano povećanje na 50%)",
            "**Follow-up:** Obavezan pregled za 2 tjedna"
        ]
    elif age < 65 or atc_count >= 3:
        tier = "Tier 2: Umjereni rizik"
        n_pac = 3397
        rate = "36.2%"
        color = "#f57c00"
        plan = [
            "**Edukacija:** Standardni DESMOND format (grupni)",
            "**Digitalna podrška:** SMS podsjetnici 2x tjedno",
            "**Follow-up:** Kontrola za 1 mjesec"
        ]
    else:
        tier = "Tier 3: Nizak rizik"
        n_pac = "Nepoznato"
        rate = "24.2%"
        color = "#388e3c"
        plan = ["Standardni protokol i osnaživanje pacijenta za samomenadžment."]

    # PRIKAZ REZULTATA
    st.markdown(f"""
        <div class="report-card" style="border-top: 10px solid {color};">
            <h2 style="color: {color}; margin-top:0;">{tier}</h2>
            <p>Identificirana stopa neadherencije: <b>{rate}</b> (n={n_pac})</p>
            <hr>
            <h4>🛠️ Predloženi plan intervencije:</h4>
        </div>
    """, unsafe_allow_html=True)

    for item in plan:
        st.markdown(f"- {item}")

    with st.expander("🔍 Metodološka osnova (Zadatak 4.2)"):
        st.write(f"Intervencija za ovaj tier osigurava racionalnu alokaciju resursa u sustavu primarne zaštite.")
        if "Tier 1" in tier:
            st.write("DESMOND program pokazuje 66% vjerojatnost troškovne učinkovitosti uz trošak od ~£76 po pacijentu.")

    # ROI Kalkulator
    st.success(f"💰 **ROI Procjena:** Primjenom SMS podsjetnika očekuje se poboljšanje adherencije za **11%** (s 39% na 50%).")
else:
    st.info("Unesite parametre pacijenta kako biste dobili personalizirani plan kliničke intervencije.")