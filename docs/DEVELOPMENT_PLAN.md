# 🏔️ CAP TABLE SIMULATOR PRO - COMPLETE DEVELOPMENT PLAN
## Scalable App for 1-25 Funding Rounds

---

## 📊 PROJECT VISION

### App Overview
**"Cap Table Simulator Pro"** - Professional startup equity analysis dashboard

- **Framework:** Streamlit
- **Design System:** Mountain Path (Dark Blue #003366, Light Blue #004d80, Gold #FFD700)
- **Scalability:** 1-25 funding rounds
- **Features:** Dilution vs Pro-Rata comparison, dynamic inputs, professional visualizations
- **Target Users:** Founders, VCs, MBA students, Finance professionals

### Key Differentiators
- ✅ Dynamic round configuration (1-25 rounds)
- ✅ Real-time calculations & updates
- ✅ Side-by-side scenario comparison
- ✅ Professional Mountain Path branding
- ✅ Educational content & explanations
- ✅ Export capabilities (Excel, PDF, CSV)
- ✅ Data verification & validation checks

---

## 🎨 DESIGN SYSTEM (THE MOUNTAIN PATH)

### Color Palette
```python
COLORS = {
    'dark_blue': '#003366',      # Primary: Headers, text
    'light_blue': '#004d80',     # Secondary: Highlights
    'gold': '#FFD700',           # Accent: Important values
    'white': '#FFFFFF',          # Background
    'light_gray': '#f0f2f6',     # Subtle backgrounds
    'success': '#00d084',        # Pro-rata benefits
    'warning': '#ff9800',        # Dilution caution
    'info': '#2196f3'            # Information
}
```

### Typography
```
Headings: Times New Roman, Bold, 24-28pt, Dark Blue
Subheadings: Times New Roman, Bold, 18-20pt, Dark Blue
Body: Times New Roman, Regular, 12-14pt, Dark Blue
Mono: Courier, Regular, 11-12pt (for numbers)
```

---

## 📁 PROJECT STRUCTURE

```
cap_table_simulator_pro/
├── app.py                              # Main Streamlit application
├── config/
│   ├── colors.py                       # Color definitions
│   ├── constants.py                    # App constants
│   └── paths.py                        # File paths
├── styles/
│   ├── css_styles.py                   # Custom CSS
│   └── theme.py                        # Streamlit theme
├── components/
│   ├── header.py                       # Hero header
│   ├── sidebar.py                      # Sidebar navigation
│   ├── input_controls.py               # Input form controls
│   ├── cards.py                        # Metric cards
│   ├── tables.py                       # Data tables
│   └── charts.py                       # Chart components
├── data/
│   ├── calculations.py                 # Financial calculations
│   ├── models.py                       # Data models
│   └── validation.py                   # Data validation
├── scenarios/
│   ├── dilution.py                     # Dilution scenario
│   ├── prorata.py                      # Pro-rata scenario
│   └── comparator.py                   # Scenario comparison
├── visualizations/
│   ├── charts.py                       # Chart generation
│   └── exporters.py                    # Export functionality
├── pages/
│   ├── 01_scenario_comparison.py       # Main comparison
│   ├── 02_dilution_analysis.py         # Dilution deep-dive
│   ├── 03_prorata_analysis.py          # Pro-rata deep-dive
│   ├── 04_ownership_timeline.py        # Ownership evolution
│   ├── 05_investor_returns.py          # Return calculations
│   ├── 06_cap_table_explorer.py        # Data exploration
│   └── 07_settings.py                  # App settings
├── utils/
│   ├── helpers.py                      # Helper functions
│   ├── formatters.py                   # Number formatting
│   └── exporters.py                    # Export to Excel/PDF/CSV
├── assets/
│   ├── logo.png                        # Mountain Path logo
│   └── sample_data.csv                 # Sample datasets
├── requirements.txt                    # Dependencies
└── README.md                           # Documentation
```

---

## 🎯 APP PAGES & FEATURES (7 Main Sections)

### PAGE 1: SCENARIO COMPARISON (Main Page)

**Features:**
```
LEFT SIDEBAR:
├── Number of Rounds: Slider (1-25)
├── Analysis Type: Radio (Dilution / Pro-Rata / Both)
├── Currency: Select (USD / INR)
└── Navigation: Page selector

MAIN CONTENT:
├── Input Section:
│   ├── Dynamic table (round | pre-money | investment)
│   └── Buttons: Reset, Load Sample, Calculate, Export
│
├── Comparison View (Tabs):
│   ├── With Dilution table
│   ├── Pro-Rata Protected table
│   └── Side-by-Side comparison
│
├── Key Metrics Cards:
│   ├── Total Capital Raised
│   ├── Final Founder %
│   ├── Final Seed %
│   └── Pro-Rata Impact
│
└── Visualizations:
    ├── Ownership Evolution (Line Chart)
    ├── Share Count Growth (Area Chart)
    ├── Price Per Share (Bar Chart)
    └── Comparison Dashboard
```

---

### PAGE 2: DILUTION ANALYSIS
**Content:** Formula explanation, step-by-step walkthrough, charts

---

### PAGE 3: PRO-RATA ANALYSIS
**Content:** Pro-rata formula, investor eligibility, benefits

---

### PAGE 4: OWNERSHIP TIMELINE
**Content:** Ownership evolution, share tracking, downloadable data

---

### PAGE 5: INVESTOR RETURNS
**Content:** Exit scenarios, ROI calculations, return rankings

---

### PAGE 6: CAP TABLE EXPLORER
**Content:** Filterable data, custom grouping, export

---

### PAGE 7: SETTINGS
**Content:** Display options, export preferences, defaults

---

## 🔄 DEVELOPMENT PHASES

### PHASE 0: SETUP & CONFIGURATION (2-3 days)

**Deliverables:**
- Project structure
- config/ with colors, fonts, constants
- styles/ with CSS
- requirements.txt

**Key Files:**
```python
# config/colors.py
COLORS = {
    'dark_blue': '#003366',
    'light_blue': '#004d80',
    'gold': '#FFD700',
    'success': '#00d084',
    'warning': '#ff9800'
}

# config/constants.py
MAX_ROUNDS = 25
MIN_ROUNDS = 1
CURRENCY_OPTIONS = ['USD', 'INR']
DEFAULT_DECIMALS = 2

# requirements.txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
openpyxl>=3.11.0
```

---

### PHASE 1: COMPONENTS LIBRARY (3-4 days)

**Components:**
```python
# components/header.py
- HeroHeader()
- BrandingSection()

# components/cards.py
- MetricCard()
- ComparisonCard()

# components/tables.py
- CapTableDisplay()
- ComparisonTableDisplay()

# components/charts.py
- OwnershipChart()
- ShareCountChart()
- PriceChart()
```

---

### PHASE 2: DATA LAYER (4-5 days)

**Functions:**
```python
# data/calculations.py
- calculate_post_money()
- calculate_price_per_share()
- calculate_new_shares()
- calculate_ownership_pct()

# scenarios/dilution.py
- apply_dilution_scenario()
- distribute_shares_dilution()
- generate_dilution_cap_table()

# scenarios/prorata.py
- apply_prorata_scenario()
- calculate_prorata_shares()
- calculate_remainder_shares()
- generate_prorata_cap_table()

# scenarios/comparator.py
- compare_scenarios()
- calculate_differences()
```

---

### PHASE 3: MAIN PAGE (5-6 days)

**Features:**
- Round selector (1-25)
- Dynamic input table
- Real-time calculations
- Side-by-side comparison
- Export functionality

---

### PHASE 4: DEEP-DIVE PAGES (4-5 days)

**Pages:**
- Dilution Analysis
- Pro-Rata Analysis
- Ownership Timeline
- Investor Returns

---

### PHASE 5: EXPLORER & SETTINGS (2-3 days)

**Pages:**
- Cap Table Explorer
- Settings

---

### PHASE 6: POLISH & TESTING (2-3 days)

**Tasks:**
- Code cleanup
- Performance optimization
- Error handling
- User testing

---

## 🛠️ TECHNICAL STACK

### Frontend
- Streamlit (layout="wide")
- Custom CSS via st.markdown()

### Data Processing
- pandas
- numpy

### Visualization
- plotly (interactive charts)
- matplotlib (if needed)

### Export
- openpyxl (Excel)
- csv

### Deployment
- Streamlit Cloud

---

## 📊 KEY CALCULATIONS

### Basic Formulas
```
POST_MONEY = PRE_MONEY + INVESTMENT
PRICE_PER_SHARE = (PRE_MONEY × 1,000,000) / PRE_ROUND_SHARES
NEW_SHARES = (INVESTMENT × 1,000,000) / PRICE_PER_SHARE
TOTAL_SHARES = SUM(ALL_INVESTOR_SHARES)
OWNERSHIP_PCT = INVESTOR_SHARES / TOTAL_SHARES
```

### Dilution
```
Each investor gets shares only in their round
Ownership drops as new investors enter
Founder dilution is inevitable
```

### Pro-Rata
```
PRORATA_SHARES = INVESTOR_PCT_BEFORE × NEW_SHARES_ISSUED
NEW_INVESTOR = NEW_SHARES - SUM(PRORATA_SHARES)
Maintains investor ownership percentages
```

---

## ✅ QUALITY CHECKLIST

- ✅ Supports 1-25 rounds
- ✅ Real-time calculations
- ✅ Zero calculation errors
- ✅ Ownership % always 100%
- ✅ Mountain Path branding
- ✅ Professional styling
- ✅ Mobile-responsive
- ✅ Export functionality
- ✅ Educational content

---

## 🚀 SUCCESS CRITERIA

✅ Dynamic round configuration (1-25)
✅ Dilution vs Pro-Rata comparison
✅ Professional Mountain Path design
✅ Real-time calculations
✅ Export to Excel
✅ Mobile-responsive
✅ Fast performance (<2s)
✅ Intuitive UI
✅ Educational explanations
✅ Zero errors

---

## 📞 CLARIFICATION QUESTIONS

1. Logo/Branding: Use Mountain Path logo from image?
2. Sample Data: Use 5-round example or custom scenarios?
3. Export Priority: Excel first? PDF later?
4. Target Users: Students? Or professionals?
5. Investor Management: Custom names or generic (Seed, Series A)?
6. Localization: USD only or INR support?
7. Additional Metrics: IRR, MOIC calculations?
8. Deployment: Streamlit Cloud? Self-hosted?

---

**STATUS: READY TO BUILD** 🚀

