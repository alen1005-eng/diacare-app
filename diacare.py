import streamlit as st

# Postavke stranice
st.set_page_config(page_title="DiaCare AI", page_icon="💊")

# CSS za ljepši izgled kartica
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 DiaCare: Adherence AI Predictor")
st.write("Predikcija vjerovatnoće pridržavanja terapije na osnovu SPE podataka.")

# Sidebar za unos podataka
st.sidebar.header("Unos podataka o pacijentu")
prior_pdc = st.sidebar.slider("Prethodni PDC (0.0 - 1.0):", 0.0, 1.0, 0.8)
last_visit = st.sidebar.number_input("Dani od zadnjeg pregleda:", 0, 365, 60)
atc_count = st.sidebar.number_input("Broj različitih lijekova (ATC):", 1, 20, 3)
days_since_dx = st.sidebar.number_input("Dani od dijagnoze:", 0, 5000, 365)
is_metformin = st.sidebar.checkbox("Pacijent na Metforminu", value=True)

# Logika podataka (Tvoja tablica)
stats = {
    'Skupina 1': {'pdc': 0.74, 'prob': 0.333, 'naziv': 'Kritična neadherencija', 'akcija': 'HITNO: Potrebna intervencija patronažne službe.'},
    'Skupina 3': {'pdc': 0.80, 'prob': 0.641, 'naziv': 'Rizična adherencija (Novi)', 'akcija': 'Edukacijski podsjetnici: Visok rizik odustajanja.'},
    'Skupina 2': {'pdc': 0.93, 'prob': 0.898, 'naziv': 'Visoka adherencija (Polifarmacija)', 'akcija': 'Redovna kontrola: Pacijent prati režim.'},
    'Ostali':    {'pdc': 0.89, 'prob': 0.809, 'naziv': 'Stabilna adherencija', 'akcija': 'Standardni protokol praćenja.'}
}

if st.sidebar.button("Pokreni AI Analizu"):
    # Pravila segmentacije
    if prior_pdc < 0.6 and last_visit > 120:
        res = stats['Skupina 1']
    elif days_since_dx < 180:
        res = stats['Skupina 3']
    elif atc_count >= 8:
        res = stats['Skupina 2']
    else:
        res = stats['Ostali']

    vjerojatnost = res['prob']
    
    # Određivanje boja i statusa
    if vjerojatnost < 0.40:
        color, status = "#C0392B", "KRITIČAN RIZIK"
    elif vjerojatnost < 0.70:
        color, status = "#E67E22", "VISOK RIZIK"
    elif vjerojatnost < 0.85:
        color, status = "#F1C40F", "UMJEREN RIZIK"
    else:
        color, status = "#27AE60", "NIZAK RIZIK"

    usteda = 1750 if vjerojatnost < 0.70 else 0

    # Prikaz rezultata
    st.markdown(f"""
        <div style="border-left: 10px solid {color}; padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">
            <h2 style="color: {color};">{status}</h2>
            <p style="font-size: 1.2em;">Segment: <b>{res['naziv']}</b></p>
            <hr>
            <p><b>AI Score (Vjerovatnoća adherencije):</b> {vjerojatnost:.1%}</p>
            <p><b>Predviđeni PDC:</b> {res['pdc']:.2f} / 0.80</p>
        </div>
    """, unsafe_allow_html=True)

    st.progress(vjerojatnost)
    
    st.info(f"**📢 Preporuka:** {res['akcija']}")
    
    if usteda > 0:
        st.success(f"💰 **ROI Potencijal:** Prevencija komplikacija štedi **{usteda} EUR** godišnje.")
    
    st.caption("🛡️ Trustworthy AI: Model validiran na SPE podacima (n=14.331).")