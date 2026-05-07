import streamlit as st

# Postavke stranice - ovo mora biti prva Streamlit naredba
st.set_page_config(page_title="DiaCare AI", page_icon="💊", layout="centered")

# Prilagođeni CSS za profesionalniji izgled
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        height: 3em; 
        background-color: #ff4b4b; 
        color: white;
        font-weight: bold;
    }
    .result-card {
        padding: 25px; 
        background-color: white; 
        border-radius: 12px; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 DiaCare: Adherence AI Predictor")
st.write("Sistem za ranu identifikaciju rizika od prekida terapije na osnovu SPE analize.")

# --- SIDEBAR: UNOS PODATAKA ---
st.sidebar.header("📋 Parametri pacijenta")

with st.sidebar:
    prior_pdc = st.slider("Prethodni PDC (pokrivenost terapijom):", 0.0, 1.0, 0.8, help="Omjer dana s lijekom u prethodnom periodu.")
    last_visit = st.number_input("Dani od zadnjeg pregleda:", 0, 365, 60)
    atc_count = st.number_input("Broj različitih lijekova (ATC klasa):", 1, 20, 3)
    days_since_dx = st.number_input("Dani od dijagnoze dijabetesa:", 0, 10000, 365)
    is_metformin = st.checkbox("Pacijent prima Metformin", value=True)
    
    st.markdown("---")
    run_analysis = st.button("POKRENI AI ANALIZU")

# --- LOGIKA PODATAKA (Usklađeno sa SPE tabelom) ---
stats = {
    'Skupina 1': {
        'pdc': 0.74, 'prob': 0.333, 
        'naziv': 'Kritična neadherencija (Dezangažirani)', 
        'akcija': 'HITNO: Potrebna intervencija patronažne službe ili poziv medicinske sestre.'
    },
    'Skupina 3': {
        'pdc': 0.80, 'prob': 0.641, 
        'naziv': 'Rizična adherencija (Novi pacijenti)', 
        'akcija': 'Edukacijski podsjetnici: Pacijent je u prvoj godini terapije, potreban pojačan nadzor.'
    },
    'Skupina 2': {
        'pdc': 0.93, 'prob': 0.898, 
        'naziv': 'Visoka adherencija (Polifarmacija)', 
        'akcija': 'Redovna kontrola: Pacijent disciplinovano prati kompleksan režim uzimanja lijekova.'
    },
    'Ostali': {
        'pdc': 0.89, 'prob': 0.809, 
        'naziv': 'Stabilna adherencija', 
        'akcija': 'Nastaviti sa standardnim protokolom praćenja svaka 3-6 mjeseca.'
    }
}

# --- PRIKAZ REZULTATA ---
if run_analysis:
    # Pravila segmentacije prema analizi
    if prior_pdc < 0.6 and last_visit > 120:
        res = stats['Skupina 1']
    elif days_since_dx < 180:
        res = stats['Skupina 3']
    elif atc_count >= 8:
        res = stats['Skupina 2']
    else:
        res = stats['Ostali']

    vjerojatnost = res['prob']
    
    # Određivanje vizuelnog identiteta rizika
    if vjerojatnost < 0.40:
        color, status = "#C0392B", "KRITIČAN RIZIK PREKIDA"
    elif vjerojatnost < 0.70:
        color, status = "#E67E22", "VISOK RIZIK NEADHERENCIJE"
    elif vjerojatnost < 0.85:
        color, status = "#F1C40F", "UMJEREN RIZIK"
    else:
        color, status = "#27AE60", "NIZAK RIZIK / STABILNO"

    # ROI izračun (ušteda na hospitalizacijama)
    usteda = 1750 if vjerojatnost < 0.70 else 0

    # Generisanje kartice rezultata
    st.markdown(f"""
        <div class="result-card" style="border-left: 10px solid {color};">
            <h2 style="color: {color}; margin-bottom: 0;">{status}</h2>
            <p style="font-size: 1.1em; color: #666;">Segment pacijenta: <b>{res['naziv']}</b></p>
            <hr>
            <table style="width: 100%; font-size: 1.1em;">
                <tr>
                    <td><b>Vjerovatnoća adherencije (AI Score):</b></td>
                    <td style="text-align: right;"><b>{vjerojatnost:.1%}</b></td>
                </tr>
                <tr>
                    <td><b>Predviđeni PDC koeficijent:</b></td>
                    <td style="text-align: right;">{res['pdc']:.2f} / 0.80</td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

    # Indikator vjerovatnoće
    st.progress(vjerojatnost)
    
    # Preporuka i ROI
    st.info(f"**📢 Preporuka za ljekara:** {res['akcija']}")
    
    if usteda > 0:
        st.success(f"💰 **ROI Potencijal:** Pravovremena intervencija spriječava trošak hospitalizacije od **{usteda} EUR**.")
    
    st.caption("🛡️ **Trustworthy AI:** Analiza bazirana na historijskim podacima 14.331 pacijenta unutar SPE okruženja.")
else:
    st.info("Podesite parametre pacijenta u lijevom meniju i kliknite na dugme za analizu.")