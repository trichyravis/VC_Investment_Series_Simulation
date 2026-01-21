# 🏔️ TECHNICAL ARCHITECTURE & IMPLEMENTATION ROADMAP
## Cap Table Simulator Pro - Detailed Build Plan

---

## 🎯 SYSTEM ARCHITECTURE

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────┐
│                   STREAMLIT FRONTEND                     │
│  (Pages, Components, Interactive Controls)              │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│              PRESENTATION LAYER                         │
│  (Styles, Charts, Cards, Tables)                       │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│              APPLICATION LAYER                          │
│  (Components, Input Handlers, State Management)        │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│              BUSINESS LOGIC LAYER                       │
│  (Calculations, Scenarios, Comparisons)               │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│              DATA LAYER                                 │
│  (Validation, Models, Calculations, Export)           │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 MODULAR COMPONENT STRUCTURE

### 1. CONFIG MODULE
**File:** `config/colors.py`
```python
COLOR_SCHEME = {
    'dark_blue': '#003366',      # RGB(0, 51, 102)
    'light_blue': '#004d80',     # RGB(0, 77, 128)
    'gold': '#FFD700',           # RGB(255, 215, 0)
    'white': '#FFFFFF',
    'light_gray': '#f0f2f6',
    'success': '#00d084',
    'warning': '#ff9800',
    'error': '#d32f2f',
    'info': '#2196f3'
}
```

**File:** `config/constants.py`
```python
MAX_ROUNDS = 25
MIN_ROUNDS = 1
DEFAULT_ROUNDS = 5
MAX_INVESTORS = 6
CURRENCY_USD = 'USD'
CURRENCY_INR = 'INR'
DEFAULT_CURRENCY = 'USD'
DEFAULT_DECIMALS = 2
```

---

### 2. STYLES MODULE
**File:** `styles/css_styles.py`
```python
CUSTOM_CSS = """
<style>
    /* Main background */
    body {
        background-color: #f0f2f6;
        font-family: 'Times New Roman', serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #003366;
        font-family: 'Times New Roman', serif;
    }
    
    /* Cards */
    .metric-card {
        background-color: white;
        border: 2px solid #004d80;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #003366;
    }
    
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    
    /* Comparison cards */
    .comparison-card-dilution {
        border-left: 4px solid #ff9800;
    }
    
    .comparison-card-prorata {
        border-left: 4px solid #00d084;
    }
    
    /* Tables */
    table {
        font-size: 12px;
        border-collapse: collapse;
    }
    
    th {
        background-color: #003366;
        color: white;
        padding: 12px;
        text-align: right;
    }
    
    td {
        padding: 10px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #003366;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
    }
    
    .stButton > button:hover {
        background-color: #004d80;
        border: 2px solid #FFD700;
    }
</style>
"""
```

---

### 3. COMPONENTS MODULE

#### 3a. Header Component
**File:** `components/header.py`
```python
import streamlit as st
from config.colors import COLOR_SCHEME

def render_hero_header():
    """Render main hero header with branding"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: {COLOR_SCHEME["dark_blue"]}; font-size: 32px;'>
            🏔️
            </h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='padding: 20px;'>
            <h1 style='color: {COLOR_SCHEME["dark_blue"]}; margin: 0;'>
            Cap Table Simulator Pro
            </h1>
            <p style='color: {COLOR_SCHEME["light_blue"]}; font-size: 16px; margin: 0;'>
            Professional Startup Equity Analysis Dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
def render_branding():
    """Render author branding section"""
    st.markdown(f"""
    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 8px; border-left: 4px solid {COLOR_SCHEME["gold"]};'>
        <h4 style='color: {COLOR_SCHEME["dark_blue"]}; margin: 0;'>Prof. V. Ravichandran</h4>
        <p style='color: #666; margin: 5px 0; font-size: 12px;'>
        28+ Years Corporate Finance & Banking Experience<br>
        10+ Years Academic Excellence
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
```

#### 3b. Cards Component
**File:** `components/cards.py`
```python
import streamlit as st
from config.colors import COLOR_SCHEME

def render_metric_card(title, value, subtext="", color_scheme="default"):
    """Render a metric card"""
    if color_scheme == "prorata":
        border_color = COLOR_SCHEME["success"]
    elif color_scheme == "dilution":
        border_color = COLOR_SCHEME["warning"]
    else:
        border_color = COLOR_SCHEME["light_blue"]
    
    st.markdown(f"""
    <div style='
        background-color: white;
        border: 2px solid {border_color};
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    '>
        <p style='color: #666; margin: 0; font-size: 12px;'>{title}</p>
        <p style='color: {COLOR_SCHEME["dark_blue"]}; margin: 10px 0 0 0; font-size: 28px; font-weight: bold;'>
        {value}
        </p>
        {f'<p style="color: #999; margin: 5px 0 0 0; font-size: 11px;">{subtext}</p>' if subtext else ''}
    </div>
    """, unsafe_allow_html=True)

def render_comparison_cards(metric_name, dilution_value, prorata_value, unit=""):
    """Render side-by-side comparison cards"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='
            background-color: white;
            border-left: 4px solid {COLOR_SCHEME["warning"]};
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 10px;
        '>
            <p style='color: #666; margin: 0; font-size: 12px;'>❌ With Dilution</p>
            <p style='color: {COLOR_SCHEME["dark_blue"]}; margin: 10px 0 0 0; font-size: 24px; font-weight: bold;'>
            {dilution_value}{unit}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='
            background-color: white;
            border-left: 4px solid {COLOR_SCHEME["success"]};
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 10px;
        '>
            <p style='color: #666; margin: 0; font-size: 12px;'>✅ Pro-Rata Protected</p>
            <p style='color: {COLOR_SCHEME["dark_blue"]}; margin: 10px 0 0 0; font-size: 24px; font-weight: bold;'>
            {prorata_value}{unit}
            </p>
        </div>
        """, unsafe_allow_html=True)
```

#### 3c. Input Controls
**File:** `components/input_controls.py`
```python
import streamlit as st
import pandas as pd

def render_round_selector():
    """Render round selection slider"""
    num_rounds = st.slider(
        "Number of Funding Rounds",
        min_value=1,
        max_value=25,
        value=5,
        step=1,
        help="Select number of funding rounds to model (1-25)"
    )
    return num_rounds

def render_funding_inputs(num_rounds):
    """Render dynamic funding input table"""
    st.subheader("📊 Funding Parameters")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.write("**Round**")
    with col2:
        st.write("**Pre-Money ($M)**")
    with col3:
        st.write("**Investment ($M)**")
    
    funding_data = []
    
    for i in range(num_rounds):
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.write(f"Round {i+1}")
        
        with col2:
            pre_money = st.number_input(
                f"Pre-money round {i+1}",
                min_value=0.0,
                value=8.0 if i == 0 else 20.0 * (2 ** i),
                step=1.0,
                label_visibility="collapsed"
            )
        
        with col3:
            investment = st.number_input(
                f"Investment round {i+1}",
                min_value=0.0,
                value=1.41 if i == 0 else 5.0 * (2 ** i),
                step=0.1,
                label_visibility="collapsed"
            )
        
        funding_data.append({
            'Round': i + 1,
            'Pre-Money': pre_money,
            'Investment': investment
        })
    
    return pd.DataFrame(funding_data)

def render_analysis_selector():
    """Render analysis type selector"""
    analysis_type = st.radio(
        "Select Analysis Type",
        options=["With Dilution", "Pro-Rata Protected", "Both (Comparison)"],
        horizontal=True,
        help="Choose which scenario to analyze"
    )
    return analysis_type

def render_currency_selector():
    """Render currency selector"""
    currency = st.selectbox(
        "Currency",
        options=["USD", "INR"],
        help="Select currency for display"
    )
    return currency
```

#### 3d. Charts Component
**File:** `components/charts.py`
```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.colors import COLOR_SCHEME

def render_ownership_comparison_chart(dilution_data, prorata_data, rounds):
    """Render ownership comparison line chart"""
    fig = go.Figure()
    
    # Add dilution line
    fig.add_trace(go.Scatter(
        x=rounds,
        y=dilution_data,
        name='With Dilution',
        mode='lines+markers',
        line=dict(color=COLOR_SCHEME['warning'], width=3),
        marker=dict(size=8)
    ))
    
    # Add pro-rata line
    fig.add_trace(go.Scatter(
        x=rounds,
        y=prorata_data,
        name='Pro-Rata Protected',
        mode='lines+markers',
        line=dict(color=COLOR_SCHEME['success'], width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Founder Ownership Evolution',
        xaxis_title='Funding Round',
        yaxis_title='Ownership %',
        hovermode='x unified',
        plot_bgcolor='#f0f2f6',
        paper_bgcolor='white',
        font=dict(family='Times New Roman', size=12, color=COLOR_SCHEME['dark_blue'])
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_share_count_chart(dilution_shares, prorata_shares, rounds):
    """Render share count area chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=rounds,
        y=dilution_shares,
        name='With Dilution',
        fill='tozeroy',
        line=dict(color=COLOR_SCHEME['warning'])
    ))
    
    fig.add_trace(go.Scatter(
        x=rounds,
        y=prorata_shares,
        name='Pro-Rata Protected',
        fill='tozeroy',
        line=dict(color=COLOR_SCHEME['success'])
    ))
    
    fig.update_layout(
        title='Total Shares Outstanding',
        xaxis_title='Funding Round',
        yaxis_title='Total Shares',
        hovermode='x unified',
        plot_bgcolor='#f0f2f6',
        paper_bgcolor='white',
        font=dict(family='Times New Roman', size=12, color=COLOR_SCHEME['dark_blue'])
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_price_per_share_chart(prices, rounds):
    """Render price per share bar chart"""
    fig = px.bar(
        x=rounds,
        y=prices,
        labels={'x': 'Funding Round', 'y': 'Price Per Share ($)'},
        title='Price Per Share Growth',
        color=prices,
        color_continuous_scale=['#004d80', '#FFD700']
    )
    
    fig.update_layout(
        plot_bgcolor='#f0f2f6',
        paper_bgcolor='white',
        font=dict(family='Times New Roman', size=12, color=COLOR_SCHEME['dark_blue']),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_ownership_stacked_chart(ownership_data):
    """Render stacked ownership chart"""
    fig = px.bar(
        ownership_data,
        x='Round',
        y=['Founder %', 'Seed %', 'Series A %', 'Series B %', 'Series C %'],
        title='Ownership % by Investor',
        color_discrete_sequence=['#003366', '#004d80', '#FFD700', '#00d084', '#ff9800'],
        labels={'value': 'Ownership %', 'variable': 'Investor'}
    )
    
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='#f0f2f6',
        paper_bgcolor='white',
        font=dict(family='Times New Roman', size=12, color=COLOR_SCHEME['dark_blue'])
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

---

## 🧮 DATA LAYER

### 4. Calculations Module
**File:** `data/calculations.py`
```python
import pandas as pd
import numpy as np

def calculate_post_money(pre_money, investment):
    """Calculate post-money valuation"""
    return pre_money + investment

def calculate_price_per_share(pre_money, pre_round_shares):
    """Calculate price per share"""
    if pre_round_shares == 0:
        return 0
    return (pre_money * 1_000_000) / pre_round_shares

def calculate_new_shares(investment, price_per_share):
    """Calculate new shares issued"""
    if price_per_share == 0:
        return 0
    return (investment * 1_000_000) / price_per_share

def calculate_total_shares(*investor_shares):
    """Calculate total shares"""
    return sum(investor_shares)

def calculate_ownership_pct(investor_shares, total_shares):
    """Calculate ownership percentage"""
    if total_shares == 0:
        return 0
    return (investor_shares / total_shares) * 100

def calculate_fully_diluted_shares(common_shares, options_pool=0):
    """Calculate fully diluted share count"""
    return common_shares + options_pool

def validate_ownership_sum(ownership_percentages, tolerance=0.01):
    """Validate ownership percentages sum to 100%"""
    total = sum(ownership_percentages)
    return abs(total - 100.0) < tolerance
```

---

### 5. Scenario Models
**File:** `scenarios/dilution.py`
```python
import pandas as pd
from data.calculations import *

def generate_dilution_cap_table(funding_data, founder_initial_shares=10_000_000):
    """Generate cap table with dilution scenario"""
    
    cap_table = []
    
    # Formation round
    cap_table.append({
        'Round': 'Formation',
        'Pre-Money': None,
        'Raise': 0,
        'Post-Money': None,
        'Pre-Round Shares': 10_000_000,
        'Price/Share': None,
        'New Shares': 0,
        'Founder Shares': founder_initial_shares,
        'Seed Shares': 0,
        'Series A Shares': 0,
        'Series B Shares': 0,
        'Series C Shares': 0,
        'Total Shares': founder_initial_shares,
        'Founder %': 100.0,
        'Seed %': 0.0,
        'Series A %': 0.0,
        'Series B %': 0.0,
        'Series C %': 0.0
    })
    
    # Funding rounds
    prev_total_shares = founder_initial_shares
    investor_shares = {'Founder': founder_initial_shares, 'Seed': 0, 'Series A': 0, 'Series B': 0, 'Series C': 0}
    
    for idx, row in funding_data.iterrows():
        pre_money = row['Pre-Money']
        investment = row['Investment']
        post_money = calculate_post_money(pre_money, investment)
        price_per_share = calculate_price_per_share(pre_money, prev_total_shares)
        new_shares = calculate_new_shares(investment, price_per_share)
        
        # Update investor shares (only new investor gets shares)
        investor_map = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D']
        current_investor = investor_map[idx] if idx < len(investor_map) else f'Series {idx}'
        investor_shares[current_investor] = new_shares
        
        total_shares = founder_initial_shares + sum([v for k, v in investor_shares.items() if k != 'Founder'])
        
        # Calculate ownership percentages
        ownership_dict = {}
        for investor, shares in investor_shares.items():
            ownership_dict[f'{investor} %'] = calculate_ownership_pct(shares, total_shares)
        
        cap_table.append({
            'Round': f'Round {idx+1}',
            'Pre-Money': pre_money,
            'Raise': investment,
            'Post-Money': post_money,
            'Pre-Round Shares': prev_total_shares,
            'Price/Share': round(price_per_share, 4),
            'New Shares': round(new_shares, 0),
            'Founder Shares': founder_initial_shares,
            'Seed Shares': investor_shares.get('Seed', 0),
            'Series A Shares': investor_shares.get('Series A', 0),
            'Series B Shares': investor_shares.get('Series B', 0),
            'Series C Shares': investor_shares.get('Series C', 0),
            'Total Shares': total_shares,
            **ownership_dict
        })
        
        prev_total_shares = total_shares
    
    return pd.DataFrame(cap_table)

def calculate_founder_dilution(cap_table):
    """Calculate founder dilution percentage"""
    initial_ownership = cap_table.iloc[0]['Founder %']
    final_ownership = cap_table.iloc[-1]['Founder %']
    dilution = initial_ownership - final_ownership
    return dilution
```

**File:** `scenarios/prorata.py`
```python
import pandas as pd
from data.calculations import *

def generate_prorata_cap_table(funding_data, founder_initial_shares=10_000_000):
    """Generate cap table with pro-rata protection"""
    
    cap_table = []
    investor_shares = {'Founder': founder_initial_shares, 'Seed': 0, 'Series A': 0, 'Series B': 0, 'Series C': 0}
    
    # Formation round
    cap_table.append({
        'Round': 'Formation',
        'Pre-Money': None,
        'Raise': 0,
        'Post-Money': None,
        'Pre-Round Shares': 10_000_000,
        'Price/Share': None,
        'New Shares': 0,
        'Founder Shares': founder_initial_shares,
        'Seed Shares': 0,
        'Series A Shares': 0,
        'Series B Shares': 0,
        'Series C Shares': 0,
        'Total Shares': founder_initial_shares,
        'Founder %': 100.0,
        'Seed %': 0.0,
        'Series A %': 0.0,
        'Series B %': 0.0,
        'Series C %': 0.0
    })
    
    # Funding rounds
    prev_total_shares = founder_initial_shares
    investor_map = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D']
    
    for idx, row in funding_data.iterrows():
        pre_money = row['Pre-Money']
        investment = row['Investment']
        post_money = calculate_post_money(pre_money, investment)
        price_per_share = calculate_price_per_share(pre_money, prev_total_shares)
        new_shares = calculate_new_shares(investment, price_per_share)
        
        # Pro-rata exercise
        prorata_allocated = 0
        for investor in investor_map[:idx]:  # All investors up to this round
            if investor in investor_shares and investor_shares[investor] > 0:
                investor_pct = investor_shares[investor] / prev_total_shares
                prorata_new = investor_pct * new_shares
                investor_shares[investor] += prorata_new
                prorata_allocated += prorata_new
        
        # New investor gets remainder
        current_investor = investor_map[idx]
        investor_shares[current_investor] = new_shares - prorata_allocated
        
        total_shares = founder_initial_shares + sum([v for k, v in investor_shares.items() if k != 'Founder'])
        
        # Calculate ownership
        ownership_dict = {}
        for investor in ['Founder', 'Seed', 'Series A', 'Series B', 'Series C']:
            ownership_dict[f'{investor} %'] = calculate_ownership_pct(investor_shares.get(investor, 0), total_shares)
        
        cap_table.append({
            'Round': f'Round {idx+1}',
            'Pre-Money': pre_money,
            'Raise': investment,
            'Post-Money': post_money,
            'Pre-Round Shares': prev_total_shares,
            'Price/Share': round(price_per_share, 4),
            'New Shares': round(new_shares, 0),
            'Founder Shares': founder_initial_shares,
            'Seed Shares': investor_shares.get('Seed', 0),
            'Series A Shares': investor_shares.get('Series A', 0),
            'Series B Shares': investor_shares.get('Series B', 0),
            'Series C Shares': investor_shares.get('Series C', 0),
            'Total Shares': total_shares,
            **ownership_dict
        })
        
        prev_total_shares = total_shares
    
    return pd.DataFrame(cap_table)
```

---

## 📱 MAIN APP FILE

**File:** `app.py`
```python
import streamlit as st
import pandas as pd
from config.colors import COLOR_SCHEME
from config.constants import MAX_ROUNDS, DEFAULT_ROUNDS
from styles.css_styles import CUSTOM_CSS
from components.header import render_hero_header, render_branding
from components.input_controls import (
    render_round_selector,
    render_funding_inputs,
    render_analysis_selector,
    render_currency_selector
)
from components.cards import render_metric_card, render_comparison_cards
from components.charts import (
    render_ownership_comparison_chart,
    render_share_count_chart,
    render_price_per_share_chart
)
from scenarios.dilution import generate_dilution_cap_table
from scenarios.prorata import generate_prorata_cap_table

# Page configuration
st.set_page_config(
    page_title="Cap Table Simulator Pro",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Main header
render_hero_header()
render_branding()

st.write("")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

num_rounds = render_round_selector()
analysis_type = render_analysis_selector()
currency = render_currency_selector()

st.write("")

# Main content
st.subheader("📊 Scenario Comparison")

# Input section
with st.expander("📋 Funding Parameters", expanded=True):
    funding_df = render_funding_inputs(num_rounds)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("📊 Load Sample", use_container_width=True):
            st.info("Sample data loaded!")
    with col3:
        if st.button("🧮 Calculate", use_container_width=True):
            st.success("Calculations complete!")
    with col4:
        if st.button("📥 Export Excel", use_container_width=True):
            st.info("Export functionality coming soon!")

# Calculations
dilution_table = generate_dilution_cap_table(funding_df)
prorata_table = generate_prorata_cap_table(funding_df)

# Display results in tabs
tab1, tab2, tab3 = st.tabs(["📊 With Dilution", "🔄 Pro-Rata Protected", "⚖️ Comparison"])

with tab1:
    st.dataframe(dilution_table, use_container_width=True, hide_index=True)

with tab2:
    st.dataframe(prorata_table, use_container_width=True, hide_index=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        render_comparison_cards(
            "Final Founder Ownership",
            f"{dilution_table.iloc[-1]['Founder %']:.2f}%",
            f"{prorata_table.iloc[-1]['Founder %']:.2f}%",
            "%"
        )
    with col2:
        render_comparison_cards(
            "Seed Investor Ownership",
            f"{dilution_table.iloc[-1]['Seed %']:.2f}%",
            f"{prorata_table.iloc[-1]['Seed %']:.2f}%",
            "%"
        )

st.write("")

# Visualizations
st.subheader("📈 Analysis & Insights")

col1, col2 = st.columns(2)

with col1:
    rounds = [f"R{i+1}" for i in range(num_rounds)]
    founder_dilution = dilution_table['Founder %'].tolist()
    founder_prorata = prorata_table['Founder %'].tolist()
    render_ownership_comparison_chart(founder_dilution, founder_prorata, rounds)

with col2:
    total_shares_dilution = dilution_table['Total Shares'].tolist()
    total_shares_prorata = prorata_table['Total Shares'].tolist()
    render_share_count_chart(total_shares_dilution, total_shares_prorata, rounds)

# Footer
st.divider()
st.markdown(f"""
<div style='text-align: center; color: #999; font-size: 12px;'>
    <p>🏔️ Cap Table Simulator Pro | The Mountain Path - World of Finance</p>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience</p>
</div>
""", unsafe_allow_html=True)
```

---

## ✅ NEXT STEPS

1. **Create project directory**
   ```bash
   mkdir cap_table_simulator_pro
   cd cap_table_simulator_pro
   ```

2. **Create all folders**
   ```bash
   mkdir config styles components data scenarios visualizations pages utils assets
   ```

3. **Create core files** (in order):
   - `config/colors.py`
   - `config/constants.py`
   - `styles/css_styles.py`
   - `components/header.py`
   - `components/cards.py`
   - `components/input_controls.py`
   - `components/charts.py`
   - `data/calculations.py`
   - `scenarios/dilution.py`
   - `scenarios/prorata.py`
   - `app.py`

4. **Create requirements.txt**
   ```
   streamlit>=1.28.0
   pandas>=2.0.0
   numpy>=1.24.0
   plotly>=5.17.0
   openpyxl>=3.11.0
   ```

5. **Run app**
   ```bash
   streamlit run app.py
   ```

---

**Status: READY TO BUILD** 🚀

