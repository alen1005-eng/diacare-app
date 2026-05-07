# 🩺 DiaCare AI — Clinical Decision Support System

> **AI4Health.Cro Natjecanje · Zadatak 2b**  
> Predikcija neadherencije terapiji kod novo dijagnosticiranih pacijenata s dijabetesom tipa 2

---

## 📋 O projektu

**DiaCare AI** je klinički prototip sustava za podršku odlučivanju (Clinical Decision Support — CDS) koji omogućuje liječnicima obiteljske medicine **automatiziranu stratifikaciju rizika neadherencije** kod novo dijagnosticiranih pacijenata s T2DM-om.

Sustav je razvijen na temelju analize kohorte od **11.894 pacijenata** (CroDiab / HZZO, PDF 2a) i implementira trostupanjski model rizika s personaliziranim planom intervencije za svakog pacijenta.

> ⚠️ **Napomena:** Ovo je prototip koji koristi rule-based logiku stratifikacije temeljenu na rezultatima analize podataka natjecanja. Nije certificirani medicinski uređaj. Konačna klinička odluka uvijek ostaje na liječniku.

---

## 🎯 Ključni rezultati (Zadatak 2a — stvarni podaci)

| Skupina | Stopa neadherencije | Prosj. PDC | n |
|---|---|---|---|
| Novo dijagnosticirani | **36.7%** | 0.80 | ~3,852* |
| Ostali pacijenti (dugogodišnji) | 17.5% | 0.90 | 8,042 |
| **Tier 1 — Visoki rizik** | **46.4%** | 0.73 | 341 |
| **Tier 2 — Umjereni rizik** | **36.2%** | 0.81** | 3,397 |
| **Tier 3 — Nizak rizik** | **24.2%** | 0.93** | 114 |

> ✅ Podaci direktno iz PDF 2a (CroDiab/HZZO kohorta n=11,894)  
> \* Procjena iz postotaka kohorte  
> \*\* Procjena — nije direktno iz PDF 2a

---

## 🤖 Model i stratifikacija

### Logika stratifikacije (rule-based, izvedena iz analize podataka)

```
Tier 1 (Visoki rizik):   Dob < 50 AND (lijekovi ≥ 3 OR bez HbA1c mjerenja)
Tier 3 (Nizak rizik):    Dob ≥ 55 AND lijekovi ≤ 1 AND HbA1c mjerenje prisutno
Tier 2 (Umjereni rizik): svi ostali slučajevi
```

### Prediktori (4 klinička prediktora)
1. **Je li dijagnoza T2DM postavljena u posljednjih 6 mjeseci?**
2. **Dob pacijenta** — mlađi pacijenti (<50 god.) pod višim rizikom
3. **Broj lijekova** — polipragmazija (≥3 lijeka) povećava rizik
4. **HbA1c monitoring** — izostanak mjerenja = nizak klinički angažman

### AUROC
AUROC 0.847 odnosi se na Random Forest model razvijen u **zadatku 1a** — nije integriran u ovaj prototip, naveden je kao referentna metrika modela.

---

## 💊 Klinički plan intervencije (✅ PDF 2a)

### Tier 1 — Visoki rizik (n=341, 46.4% neadherencija)
- 🏫 **DESMOND program** — 6-satna strukturirana grupna edukacija (£76/pacijentu, 66% cost-effectiveness)
- 👨‍⚕️ **Case management** — individualno farmaceutsko savjetovanje
- 📱 **SMS podsjetnici** — 50% vs 39% adherencija, p=0.003 (meta-analiza 9 RCT, n=1,121)
- 📅 **Follow-up za 14 dana**

### Tier 2 — Umjereni rizik (n=3,397, 36.2% neadherencija)
- 🏫 **Standardna DESMOND edukacija** — grupni format
- 📱 **SMS podsjetnici 2× tjedno**
- 📅 **Follow-up za 1 mjesec**

### Tier 3 — Nizak rizik (n=114, 24.2% neadherencija)
- 📚 **Edukacijski materijali** — pisani i digitalni
- 📅 **Rutinska kontrola za 3 mjeseca**

---

## 💰 Ekonomska opravdanost

| Metrika | Vrijednost | Izvor |
|---|---|---|
| Godišnji trošak bez komplikacija | €1,956/pacijentu | ✅ PDF 2a |
| Godišnji trošak s komplikacijama | ~€3,325/pacijentu | 📊 Procjena (europska lit.) |
| T2DM udio u HZZO proračunu | 11.49% | ✅ PDF 2a |
| Komplikacije vs. ukupni troškovi | 85.72% | ✅ PDF 2a |
| Spriječene neadherencije (Tier 1) | ~32 po kohorti | ✅ PDF 2a |

> 📊 Procjena troška neadherentnog pacijenta (~€3,325) bazirana na europskoj literaturi:  
> Španjolska studija (Catalonia): adherentni €1,548 vs neadherentni €3,110 (omjer ~2.0x);  
> konzervativna procjena za RH: omjer 1.7x primjenjen na €1,956 (PDF 2a)

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
streamlit run diacare.py
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
├── diacare.py              # Glavna aplikacija
├── requirements.txt        # Python dependencies
├── README.md               # Dokumentacija
└── .streamlit/
    └── config.toml         # Streamlit tema
```

### Sekcije aplikacije

| Tab | Opis | Status |
|---|---|---|
| 📊 Pregled pacijenta | Demografija, risk score, adherencija, PDC projekcija | ✅ Implementirano |
| 🧠 Explainable AI | SHAP-like panel, feature importance, klinička interpretacija | ✅ Implementirano |
| 💊 Intervencija | Personalizirani plan, care pathway timeline, SMS modul (mock) | ✅ Implementirano |
| 🏥 Populacijska analiza | Kohortni pregled, trendovi, distribucija rizika | ✅ Implementirano |
| 💰 Ekonomski učinak | Troškovi s izvorima, ROI intervencija, usporedbe | ✅ Implementirano |
| 🔄 Klinički workflow | Procesni dijagram, EHR roadmap, mock alarmi | ✅ Implementirano |

---

## ⚡ Demo scenariji (sintetski pacijenti)

Aplikacija uključuje 3 predefinirana demo scenarija s **fiktivnim pacijentima** za brzu prezentaciju.  
Statistike prikazane u aplikaciji temelje se na **stvarnim podacima** (CroDiab/HZZO, n=11,894).

| Scenarij | Ime | Dob | Lijekovi | HbA1c | Tier |
|---|---|---|---|---|---|
| 🔴 Visoki rizik | Marko Horvat | 42 god. | 4 lijeka | NE | Tier 1 |
| 🟡 Srednji rizik | Ana Kovač | 52 god. | 2 lijeka | DA | Tier 2 |
| 🟢 Nizak rizik | Ivan Blažević | 61 god. | 1 lijek | DA | Tier 3 |

---

## 🔗 EHR Integracije — Roadmap

| Sustav | Status |
|---|---|
| CEZIH | 🔧 Planirana integracija |
| CroDiab registar | 🔧 Planirana integracija |
| HZZO Portal | 🔧 Planirana integracija |
| HL7 FHIR API | 🔧 Dugoročni roadmap |

---

## ⚠️ Ograničenja i etičke napomene

- Prototip koristi **rule-based logiku** — ne stvarni ML model (AUROC 0.847 odnosi se na task 1a model)
- Analiza provedena na retroaktivnim administrativnim podacima — ograničeni kauzalni zaključci
- Kriteriji segmentacije temelje se na 3 prediktora dostupna u podacima natjecanja
- Sociodemografski faktori (obrazovanje, udaljenost, psihosocijalni) nisu bili dostupni
- Generalizacija na širu populaciju zahtijeva prospektivnu validaciju
- **Konačna klinička odluka uvijek ostaje na liječniku**
- Nije certificirani medicinski uređaj

---

## 📚 Literatura i izvori

- IDF Diabetes Atlas 2024
- CroDiab Registar 2024
- EUROASPIRE V studija
- Pharmacy Quality Alliance (PQA) — PDC standard
- DESMOND Program RCT dokazi
- SMS adherencija meta-analiza (9 RCT, n=1,121)
- KBC Dubrava — farmaceutsko savjetovanje RCT
- Španjolska studija troškova T2DM (European Journal of Health Economics, 2015)
- Njemačka studija PDC-troškovi (Applied Health Economics and Health Policy, 2023)

---

## 👨‍💻 Autor

Razvijeno za **AI4Health.Cro natjecanje** — Zadatak 2b  
Klinička primjena: Ordinacije obiteljske medicine u Republici Hrvatskoj  
Target deployment: HZZO / Primarna zdravstvena zaštita RH

---

*DiaCare AI · Clinical Decision Support System · Prototip v2.0 · 2026*  
*AI4Health.Cro · Zadatak 2b · Kohortna analiza: n=11,894 (CroDiab/HZZO)*
