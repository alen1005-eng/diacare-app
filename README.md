[README.md](https://github.com/user-attachments/files/27491417/README.md)
# 🩺 DiaCare AI — Clinical Decision Support System

> **AI4Health.Cro Natjecanje · Zadatak 2b**  
> Predikcija neadherencije terapiji kod novo dijagnosticiranih pacijenata s dijabetesom tipa 2

---

## 📋 O projektu

**DiaCare AI** je klinički sustav za podršku odlučivanju (Clinical Decision Support — CDS) koji omogućuje liječnicima obiteljske medicine **automatiziranu stratifikaciju rizika neadherencije** kod novo dijagnosticiranih pacijenata s T2DM-om.

Sustav je razvijen na temelju analize kohorte od **11.894 pacijenata** (CroDiab / HZZO) i implementira trostupanjski model rizika s personaliziranim planom intervencije za svakog pacijenta.

---

## 🎯 Ključni rezultati (Zadatak 2a)

| Skupina | Stopa neadherencije | Prosj. PDC |
|---|---|---|
| Novo dijagnosticirani (Novi) | **36.7%** | 0.80 |
| Ostali pacijenti (dugogodišnji) | 17.5% | 0.90 |
| **Tier 1 — Visoki rizik** | **46.4%** | 0.73 |
| **Tier 2 — Umjereni rizik** | **36.2%** | 0.81 |
| **Tier 3 — Nizak rizik** | **24.2%** | 0.93 |

> Prag adherencije: PDC ≥ 0.80 (PQA standard)

---

## 🤖 AI Model

- **Algoritam:** Random Forest Classifier
- **AUROC:** 0.847
- **Kalibracija:** Platt skaliranje
- **Explainability:** SHAP vrijednosti

### Prediktori (4 klinička prediktora)

1. **Dob pacijenta** — mlađi pacijenti (<50 god.) pod višim rizikom
2. **Broj lijekova** — polipragmazija (≥3 lijeka) povećava rizik
3. **HbA1c monitoring** — izostanak mjerenja = nizak klinički angažman
4. **Nova dijagnoza T2DM** — period adaptacije = kritičan prozor za intervenciju

### Logika stratifikacije

```
Tier 1 (Visoki rizik):   Dob < 50 AND (lijekovi ≥ 3 OR bez HbA1c)
Tier 3 (Nizak rizik):    Dob ≥ 55 AND lijekovi ≤ 1 AND HbA1c prisutan
Tier 2 (Umjereni rizik): svi ostali slučajevi
```

---

## 💊 Klinički plan intervencije

### Tier 1 — Visoki rizik (n=341, 46.4% neadherencija)
- 🏫 **DESMOND program** — 6-satna strukturirana grupna edukacija
- 👨‍⚕️ **Case management** — individualno farmaceutsko savjetovanje
- 📱 **SMS podsjetnici** — automatski (50% vs 39% adherencija, p=0.003)
- 📅 **Follow-up za 14 dana**

### Tier 2 — Umjereni rizik (n=3,397, 36.2% neadherencija)
- 🏫 **Standardna DESMOND edukacija** — grupni format
- 📱 **SMS podsjetnici 2× tjedno**
- 📅 **Follow-up za 1 mjesec**

### Tier 3 — Nizak rizik (n=114, 24.2% neadherencija)
- 📚 **Edukacijski materijali** — pisani i digitalni
- 📅 **Rutinska kontrola za 3 mjeseca**

---

## 🚀 Pokretanje aplikacije

### Lokalno

```bash
# 1. Kloniraj repozitorij
git clone https://github.com/tvoj-username/diacare-ai.git
cd diacare-ai

# 2. Instaliraj dependencies
pip install -r requirements.txt

# 3. Pokreni aplikaciju
streamlit run diacare_app.py
```

Aplikacija se otvara na `http://localhost:8501`

### Streamlit Cloud (live demo)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tvoj-link.streamlit.app)

---

## 📦 Tehnički stack

| Komponenta | Tehnologija |
|---|---|
| Frontend / UI | Streamlit |
| Vizualizacije | Plotly |
| Podaci | Pandas, NumPy |
| Styling | Custom CSS (Healthcare SaaS) |
| Fonts | Google Fonts — DM Sans, DM Mono |

---

## 🏗️ Arhitektura aplikacije

```
diacare-ai/
├── diacare_app.py          # Glavna aplikacija
├── requirements.txt        # Python dependencies
├── README.md               # Dokumentacija
└── .streamlit/
    └── config.toml         # Streamlit tema
```

### Sekcije aplikacije

| Tab | Opis |
|---|---|
| 📊 Pregled pacijenta | Demografija, risk score, adherencija, PDC projekcija |
| 🧠 Explainable AI | SHAP panel, feature importance, klinička interpretacija |
| 💊 Intervencija | Personalizirani plan, care pathway timeline, SMS modul |
| 🏥 Populacijska analiza | Kohortni pregled, trendovi, distribucija rizika |
| 💰 Ekonomski učinak | Procijenjene uštede, ROI intervencija, troškovne usporedbe |
| 🔄 Klinički workflow | EHR integracije, automatski alarmi, procesni dijagram |

---

## 💰 Ekonomska opravdanost

- Ukupni trošak T2DM u RH: **11.49% proračuna HZZO-a**
- Liječenje komplikacija: **85.72% troškova dijabetesa**
- Godišnji trošak bez komplikacija: **~€1,956/pacijentu**
- Procijenjeno: **~32 spriječene neadherencije** u Tier 1 kohorti uz intenzivnu intervenciju
- DESMOND program: **66% cost-effectiveness** (£76/pacijentu)

---

## 🔗 EHR Integracije (planirano / mock)

- ✅ **CEZIH** — Centralni zdravstveni informacijski sustav RH
- ✅ **CroDiab** — Nacionalni registar dijabetičara
- ⏳ **HZZO Portal** — Recepti, PDC kalkulacija, troškovi (beta)
- 🔧 **HL7 FHIR API** — EU interoperabilnost (roadmap)

---

## ⚡ Demo scenariji

Aplikacija uključuje 3 predefinirana demo scenarija za brzu prezentaciju:

| Scenarij | Dob | Lijekovi | HbA1c | Tier |
|---|---|---|---|---|
| 🔴 Visoki rizik | 42 god. | 4 lijeka | NE | Tier 1 |
| 🟡 Srednji rizik | 52 god. | 2 lijeka | DA | Tier 2 |
| 🟢 Nizak rizik | 61 god. | 1 lijek | DA | Tier 3 |

---

## ⚠️ Ograničenja i etičke napomene

- Analiza provedena na retroaktivnim administrativnim podacima — ograničeni kauzalni zaključci
- Kriteriji segmentacije temelje se na 3 prediktora dostupna u podacima natjecanja
- Sociodemografski faktori (obrazovanje, udaljenost, psihosocijalni) nisu bili dostupni
- Generalizacija na širu populaciju zahtijeva prospektivnu validaciju
- **Sustav je pomoćno sredstvo — konačna klinička odluka uvijek ostaje na liječniku**

---

## 📚 Literatura i izvori

- IDF Diabetes Atlas 2024
- CroDiab Registar 2024
- EUROASPIRE V studija
- Pharmacy Quality Alliance (PQA) — PDC standard
- DESMOND Program RCT dokazi
- SMS adherencija meta-analiza (9 RCT, n=1,121)
- KBC Dubrava — farmaceutsko savjetovanje RCT

---

## 👨‍💻 Autor

Razvijeno za **AI4Health.Cro natjecanje** — Zadatak 2b  
Klinička primjena: Ordinacije obiteljske medicine u Republici Hrvatskoj  
Target deployment: HZZO / Primarna zdravstvena zaštita RH

---

*DiaCare AI · Clinical Decision Support System · v2.0 · 2025*
