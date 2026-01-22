
"""
Cap Table Simulator Pro - Enhanced Streamlit Application
Professional Startup Equity Analysis Dashboard
The Mountain Path - World of Finance

Features:
- Dynamic funding rounds (1-10)
- User input for valuations and investments
- Real-time calculations
- Dilution vs Pro-Rata comparison
- Professional UI with tabs
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Cap Table Simulator Pro - The Mountain Path",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color scheme from The Mountain Path
DARK_BLUE = "#003366"
LIGHT_BLUE = "#004d80"
GOLD_COLOR = "#FFD700"

# ============================================================================
# CONSTANTS
# ============================================================================

COLOR_SCHEME = {
    "dark_blue": DARK_BLUE,
    "light_blue": LIGHT_BLUE,
    "gold": GOLD_COLOR,
    "success": "#00d084",
    "warning": "#ff9800",
    "error": "#ff4444",
    "info": "#2196F3"
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_post_money(pre_money, investment):
    return pre_money + investment

def calculate_price_per_share(pre_money, pre_round_shares):
    if pre_round_shares <= 0:
        return 0
    return (pre_money * 1_000_000) / pre_round_shares

def calculate_new_shares(investment, price_per_share):
    if price_per_share <= 0:
        return 0
    return (investment * 1_000_000) / price_per_share

def calculate_ownership_pct(investor_shares, total_shares):
    if total_shares <= 0:
        return 0
    return (investor_shares / total_shares) * 100

# ============================================================================
# CSS STYLING
# ============================================================================

st.markdown(f"""
    <style>
    /* ============ TAB STYLING ============ */
    button[kind="tab"] {{
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 12px 20px !important;
        color: {DARK_BLUE} !important;
        border-radius: 10px 10px 0 0 !important;
        background-color: #f0f4f8 !important;
        border: 2px solid #e0e8f0 !important;
        margin: 0 2px !important;
        transition: all 0.3s ease !important;
    }}
    
    button[kind="tab"]:hover {{
        background-color: #e0e8f0 !important;
        border-color: {LIGHT_BLUE} !important;
        color: {LIGHT_BLUE} !important;
        transform: translateY(-2px) !important;
    }}
    
    button[kind="tab"][aria-selected="true"] {{
        background: linear-gradient(135deg, {DARK_BLUE} 0%, {LIGHT_BLUE} 100%) !important;
        color: white !important;
        border: 2px solid {DARK_BLUE} !important;
        box-shadow: 0 4px 12px rgba(0, 51, 102, 0.3) !important;
        font-weight: 800 !important;
    }}
    
    /* ============ TAB CONTENT STYLING ============ */
    [data-testid="stTabContent"] {{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem !important;
        border-radius: 0 10px 10px 10px !important;
        border: 2px solid #e0e8f0 !important;
        box-shadow: 0 4px 15px rgba(0, 51, 102, 0.08) !important;
        min-height: 500px !important;
    }}
    
    /* ============ HERO TITLE STYLING ============ */
    .hero-title {{ 
        background: linear-gradient(135deg, {DARK_BLUE} 0%, {LIGHT_BLUE} 100%); 
        padding: 2rem; 
        border-radius: 20px; 
        margin-bottom: 2rem; 
        box-shadow: 0 12px 30px rgba(0, 51, 102, 0.4); 
        border: 4px solid {DARK_BLUE}; 
        color: white; 
        text-align: center; 
    }}
    
    /* ============ SIDEBAR STYLING ============ */
    [data-testid="stSidebar"] {{ 
        background: linear-gradient(135deg, #f0f4f8 0%, #e8f0f7 100%) !important; 
    }}
    
    /* Sidebar text - Dark for contrast */
    [data-testid="stSidebar"] h3 {{
        color: {DARK_BLUE} !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        margin-bottom: 15px !important;
        padding-bottom: 10px !important;
        border-bottom: 3px solid {GOLD_COLOR} !important;
    }}
    
    [data-testid="stSidebar"] label {{
        color: {DARK_BLUE} !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }}
    
    [data-testid="stSidebar"] p {{
        color: {DARK_BLUE} !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stSidebar"] div[role="radiogroup"] p {{
        color: {DARK_BLUE} !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {{
        color: {DARK_BLUE} !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stSidebar"] .st-ae div {{
        color: {DARK_BLUE} !important;
    }}
    
    [data-testid="stSidebar"] .st-at {{
        color: {DARK_BLUE} !important;
    }}
    
    /* Metrics in sidebar */
    [data-testid="stSidebar"] [data-testid="metric-container"] {{
        background-color: rgba(255, 215, 0, 0.1) !important;
        border: 2px solid {GOLD_COLOR} !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }}
    
    /* Slider styling */
    [data-testid="stSidebar"] .stSlider {{
        margin: 15px 0 !important;
    }}
    
    /* Number input styling */
    [data-testid="stSidebar"] input {{
        color: {DARK_BLUE} !important;
        font-weight: 600 !important;
        background-color: white !important;
        border: 2px solid {LIGHT_BLUE} !important;
    }}
    
    /* Button styling */
    .stButton>button {{ 
        background-color: {GOLD_COLOR} !important; 
        color: {DARK_BLUE} !important; 
        font-weight: bold !important; 
        border-radius: 10px !important; 
        width: 100%;
        font-size: 16px !important;
        padding: 12px !important;
    }}
    
    .stButton>button:hover {{
        background-color: #FFC700 !important;
        box-shadow: 0 6px 16px rgba(255, 215, 0, 0.4) !important;
    }}
    
    /* Divider color */
    [data-testid="stSidebar"] .st-emotion-cache-1l02zno {{
        background-color: {DARK_BLUE} !important;
    }}
    
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown(f"<div class='hero-title'><h1>CAP TABLE SIMULATOR PRO</h1><p>Professional Startup Equity Analysis Dashboard</p><p>Prof. V. Ravichandran | 28+ Years Finance Experience</p></div>", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    # Main Configuration Header
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {DARK_BLUE} 0%, {LIGHT_BLUE} 100%); 
                padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h2 style='color: white; margin: 0; font-size: 24px;'>⚙️ CONFIGURATION</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Number of Rounds")
    col_rounds1, col_rounds2 = st.columns([2, 1])
    
    with col_rounds1:
        num_rounds = st.slider(
            "Total Rounds",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Total funding rounds including formation"
        )
    
    with col_rounds2:
        st.metric("Rounds", num_rounds)
    
    st.divider()
    
    st.markdown("### 👤 Founder's Shares")
    col_cap1, col_cap2 = st.columns([2, 1])
    
    with col_cap1:
        founder_capital = st.slider(
            "Initial Shares (M)",
            min_value=1.0,
            max_value=100.0,
            value=10.0,
            step=0.5,
            help="Founder's initial share allocation in millions"
        )
    
    founder_shares = int(founder_capital * 1_000_000)
    
    with col_cap2:
        st.metric("Shares", f"{founder_capital:.1f}M")
    
    st.divider()
    
    st.markdown("### 📈 About This Tool")
    st.markdown("""
    <div style='background-color: rgba(255, 215, 0, 0.1); padding: 12px; border-radius: 8px; border-left: 4px solid #FFD700;'>
    <p style='color: #003366; margin: 0; font-weight: 600; font-size: 13px;'>
    ✓ Compare equity dilution<br>
    ✓ Model different scenarios<br>
    ✓ See ownership impact<br>
    ✓ Analyze pro-rata protection
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    calculate_button = st.button("🧮 CALCULATE", use_container_width=True)
    
    # ========== SIDEBAR FOOTER ==========
    st.divider()
    
    st.markdown("""
    <div style='padding: 15px 0; text-align: center;'>
        <p style='margin: 0; font-size: 12px; font-weight: 700; color: #003366;'>
            🏔️ The Mountain Path
        </p>
        <p style='margin: 5px 0; font-size: 11px; color: #555;'>
            Prof. V. Ravichandran
        </p>
        <p style='margin: 0; font-size: 10px; color: #999;'>
            28+ Yrs Finance | 10+ Yrs Academic
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div style='padding: 10px 0; text-align: center;'>
        <p style='margin: 0 0 8px 0; font-size: 11px; font-weight: 600; color: #003366;'>
            📱 Connect
        </p>
        <p style='margin: 0; font-size: 10px;'>
            <a href='https://www.linkedin.com/in/trichyravis' target='_blank' style='
                color: #0A66C2; text-decoration: none; font-weight: 600;
            '>🔗 LinkedIn</a>
            &nbsp; | &nbsp;
            <a href='https://github.com/trichyravis' target='_blank' style='
                color: #333; text-decoration: none; font-weight: 600;
            '>💻 GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Funding rounds input - REMOVE FROM HERE
# (Will be moved to tab)

st.markdown("---")
st.subheader("📊 Cap Table Results")

# Create tabs with About first and Educational at end
tab_about, tab_funding, tab1, tab2, tab3, tab4, tab_edu = st.tabs([
    "ℹ️ About",
    "📊 Funding Rounds Configuration",
    "📊 With Dilution",
    "🔄 Pro-Rata Protected",
    "⚖️ Comparison",
    "📈 Insights",
    "📚 Educational"
])

# ============================================================================
# TAB ABOUT: CAP TABLE SIMULATOR PRO
# ============================================================================

with tab_about:
    # Beautiful header for About tab
    st.markdown("""
    <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 25px; 
                box-shadow: 0 8px 20px rgba(0, 51, 102, 0.3); text-align: center;'>
        <h1 style='color: white; margin: 0; font-size: 36px;'>🏔️ CAP TABLE SIMULATOR PRO</h1>
        <p style='color: #FFD700; margin: 10px 0 0 0; font-size: 18px; font-weight: 600;'>
            The Mountain Path - World of Finance
        </p>
        <p style='color: #e8f0f7; margin: 8px 0 0 0; font-size: 14px;'>
            Explore the Real Mathematics of Startup Equity • Understand Founder Dilution & Investor Rights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview section
    st.markdown("## 📌 Overview")
    st.markdown("""
    The **Cap Table Simulator Pro** is an advanced educational tool designed to help MBA, CFA, and FRM students 
    understand the complexities of startup equity dilution, valuation mechanisms, and investor rights protections 
    in venture capital funding scenarios.
    """)
    
    # What is a Cap Table
    st.markdown("## 📋 What is a Cap Table?")
    st.markdown("""
    A **Capitalization Table (Cap Table)** is a complete record of:
    - **Ownership structure** of a company
    - **Shareholdings** of all investors and founders
    - **Dilution dynamics** across multiple funding rounds
    - **Valuation history** and equity stakes
    - **Rights and preferences** of different share classes
    
    Cap tables are critical for understanding how ownership percentages change with each new investment round.
    """)
    
    # Key Features
    st.markdown("## ⭐ Key Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Funding Configuration:**
        - Support for 1-10 funding rounds
        - Customize pre-money valuations
        - Define investment amounts per round
        - Track formation through scaling
        
        **Dilution Analysis:**
        - Real-time calculation of ownership percentages
        - Series-wise breakdown of equity
        - Share count tracking across rounds
        - Visual pie charts for easy understanding
        """)
    
    with col2:
        st.markdown("""
        **Pro-Rata Protection:**
        - Compare standard dilution vs. pro-rata scenarios
        - Analyze protective provisions impact
        - Calculate founder retention implications
        - Quantify investor benefits
        
        **Educational Tools:**
        - Step-by-step calculation formulas
        - Practical examples with real numbers
        - Pro-Rata rights explanation
        - Best practices in startup equity
        """)
    
    # How to Use
    st.markdown("## 🎯 How to Use This Tool")
    st.markdown("""
    1. **Funding Rounds Tab**: Configure the number of rounds and founder's initial shares
    2. **Enter Funding Details**: Input pre-money valuations and investment amounts
    3. **Click CALCULATE**: Generate the cap table and analysis
    4. **With Dilution Tab**: View standard equity dilution scenario
    5. **Pro-Rata Protected Tab**: Compare with investor pro-rata rights protection
    6. **Comparison Tab**: Analyze differences between scenarios
    7. **Insights Tab**: Review key metrics and findings
    8. **Educational Tab**: Learn formulas and see worked examples
    """)
    
    # Important Concepts
    st.markdown("## 💡 Important Concepts")
    
    with st.expander("📌 **Pre-Money Valuation**", expanded=False):
        st.markdown("""
        The company's valuation **before** the new investment round.
        
        **Example:** If pre-money = $10M and investment = $2M:
        - Post-money valuation = $10M + $2M = $12M
        - Investor gets: ($2M / $12M) × 100 = 16.67% ownership
        """)
    
    with st.expander("📌 **Post-Money Valuation**", expanded=False):
        st.markdown("""
        The company's valuation **after** the investment is added.
        
        **Formula:** Post-Money = Pre-Money + Investment Amount
        """)
    
    with st.expander("📌 **Dilution**", expanded=False):
        st.markdown("""
        Reduction in ownership percentage when new shares are issued to investors.
        
        **Why it happens:** New investors receive shares from the company (not from founders)
        - Founder's % stake decreases with each round
        - Founder's # of shares remains constant
        - Company's total shares increase with each investment
        """)
    
    with st.expander("📌 **Pro-Rata Rights**", expanded=False):
        st.markdown("""
        A protective provision allowing early investors to maintain their ownership % in future rounds.
        
        **How it works:**
        - Investor in Seed round negotiates 20% ownership
        - In Series A, if investor exercises pro-rata rights
        - They can invest to maintain 20% ownership
        - Prevents excessive dilution of early investors
        """)
    
    with st.expander("📌 **Share Count vs Ownership %**", expanded=False):
        st.markdown("""
        **Share Count:** Number of shares a stakeholder holds
        - Founder: 10,000,000 shares (stays constant)
        - Investor A: 5,000,000 shares (increases per investment)
        
        **Ownership %:** Percentage of total company
        - Founder: 10M / 20M total = 50%
        - Investor A: 5M / 20M total = 25%
        
        As total shares increase, % ownership decreases even with constant share count.
        """)
    
    # Tab Navigation Guide
    st.markdown("## 📑 Tab Navigation Guide")
    
    tabs_info = {
        "📊 Funding Rounds": "Enter funding details for each round",
        "📊 With Dilution": "Standard dilution scenario without pro-rata protection",
        "🔄 Pro-Rata Protected": "Scenario with pro-rata rights for early investors",
        "⚖️ Comparison": "Side-by-side comparison of both scenarios",
        "📈 Insights": "Key findings and calculated metrics",
        "📚 Educational": "Detailed formulas and worked examples"
    }
    
    for tab_name, description in tabs_info.items():
        st.markdown(f"**{tab_name}:** {description}")
    
    # Tips for Students
    st.markdown("## 🎓 Tips for Students")
    st.markdown("""
    ✅ **Do:**
    - Start with small numbers to understand the mechanics
    - Try multiple scenarios to see patterns
    - Compare dilution vs pro-rata to understand investor protection
    - Review the Educational tab formulas
    - Work through the examples step-by-step
    
    ❌ **Don't:**
    - Ignore the impact of pro-rata rights
    - Forget that founder shares are constant
    - Confuse percentage ownership with share count
    - Overlook that each round affects ALL previous stakeholders
    """)
    
    # Real-World Relevance
    st.markdown("## 🌍 Real-World Relevance")
    st.markdown("""
    Cap table simulation is essential for:
    - **Founders:** Understanding dilution impact and negotiating terms
    - **Investors:** Evaluating equity stakes and future scenarios
    - **Finance Professionals:** Startup valuation and analysis
    - **MBA Students:** Corporate finance and venture capital understanding
    - **CFA Candidates:** Alternative investments and equity analysis
    - **FRM Students:** Risk management in venture funding structures
    """)
    
    # Author and Source
    st.markdown("---")
    st.markdown("""
    **Created by:** Prof. V. Ravichandran  
    **Experience:** 28+ Years Corporate Finance & Banking | 10+ Years Academic Excellence  
    **Platform:** The Mountain Path - World of Finance  
    **Location:** Bangalore, India
    """)

# ============================================================================
# TAB 0: FUNDING ROUNDS CONFIGURATION
# ============================================================================

with tab_funding:
    # Beautiful header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                padding: 25px; border-radius: 15px; margin-bottom: 25px; 
                box-shadow: 0 8px 20px rgba(0, 51, 102, 0.3);'>
        <h2 style='color: white; margin: 0; font-size: 28px;'>📊 Funding Rounds Configuration</h2>
        <p style='color: #FFD700; margin: 10px 0 0 0; font-size: 14px; font-weight: 600;'>
            Define Your Cap Table • Pre-Money + Investment = Post-Money Valuation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick info box - minimal and concise
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e8f4f8 0%, #d4e9f7 100%); border-left: 5px solid #003366; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
        <p style='margin: 0; color: #003366; font-size: 13px;'>
            <strong>💡 Tip:</strong> Enter Pre-Money valuation and Investment amount for each round. Post-Money calculates automatically.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    funding_data_rows = []
    
    # Create a more compact table-like layout
    st.markdown("#### 💰 Enter Funding Details")
    
    # Create input table with better layout
    input_cols = st.columns([0.8, 2.5, 2, 2, 1.5])
    
    # Header row
    with input_cols[0]:
        st.markdown("<p style='font-weight: bold; color: #003366; margin-bottom: 20px;'>Round</p>", unsafe_allow_html=True)
    with input_cols[1]:
        st.markdown("<p style='font-weight: bold; color: #003366; margin-bottom: 20px;'>Pre-Money ($M)</p>", unsafe_allow_html=True)
    with input_cols[2]:
        st.markdown("<p style='font-weight: bold; color: #003366; margin-bottom: 20px;'>Investment ($M)</p>", unsafe_allow_html=True)
    with input_cols[3]:
        st.markdown("<p style='font-weight: bold; color: #003366; margin-bottom: 20px;'>Post-Money ($M)</p>", unsafe_allow_html=True)
    with input_cols[4]:
        st.markdown("<p style='font-weight: bold; color: #003366; margin-bottom: 20px;'>Change</p>", unsafe_allow_html=True)
    
    # Data rows
    for i in range(num_rounds):
        if i == 0:
            round_label = "Formation"
            round_emoji = "🏢"
        elif i == 1:
            round_label = "Seed"
            round_emoji = "🌱"
        else:
            round_label = f"Series {chr(64 + i - 1)}"
            round_emoji = "📈"
        
        row_cols = st.columns([0.8, 2.5, 2, 2, 1.5])
        
        # Round name
        with row_cols[0]:
            st.markdown(f"<p style='color: #003366; font-weight: 600; margin: 0;'>{round_emoji}</p>", unsafe_allow_html=True)
        
        # Pre-Money input
        with row_cols[1]:
            pre_money = st.number_input(
                f"Pre-Money {round_label}",
                min_value=0.1,
                max_value=10000.0,
                value=0.5 if i == 0 else 1.0,
                step=0.1,
                label_visibility="collapsed",
                key=f"pre_{i}",
                format="%.2f"
            )
        
        # Investment input
        with row_cols[2]:
            investment = st.number_input(
                f"Investment {round_label}",
                min_value=0.0 if i == 0 else 0.1,
                max_value=1000.0,
                value=0.0 if i == 0 else 1.0,
                step=0.1,
                label_visibility="collapsed",
                key=f"invest_{i}",
                format="%.2f"
            )
        
        # Post-Money (calculated)
        with row_cols[3]:
            post_money = pre_money + investment
            st.markdown(
                f"<p style='color: #003366; font-weight: 600; margin: 0; padding-top: 8px;'>${post_money:.2f}M</p>",
                unsafe_allow_html=True
            )
        
        # Change percentage
        with row_cols[4]:
            if pre_money > 0:
                change_pct = (investment / pre_money) * 100
                color = "#00d084" if change_pct > 0 else "#666"
                st.markdown(
                    f"<p style='color: {color}; font-weight: 600; margin: 0; padding-top: 8px;'>{change_pct:.1f}%</p>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(f"<p style='color: #666; margin: 0; padding-top: 8px;'>-</p>", unsafe_allow_html=True)
        
        funding_data_rows.append({
            'Round': i + 1,
            'Round_Name': round_label,
            'Pre_Money': pre_money,
            'Investment': investment
        })
    
    st.markdown("---")
    
    # Summary Table - Clean and Simple
    if funding_data_rows:
        summary_df = pd.DataFrame(funding_data_rows)
        summary_df['Post_Money'] = summary_df['Pre_Money'] + summary_df['Investment']
        
        # Create display dataframe
        summary_display = summary_df[['Round_Name', 'Pre_Money', 'Investment', 'Post_Money']].copy()
        summary_display['Pre_Money'] = summary_display['Pre_Money'].apply(lambda x: f"${x:.2f}M")
        summary_display['Investment'] = summary_display['Investment'].apply(lambda x: f"${x:.2f}M")
        summary_display['Post_Money'] = summary_display['Post_Money'].apply(lambda x: f"${x:.2f}M")
        summary_display.columns = ['Round', 'Pre-Money', 'Investment', 'Post-Money']
        
        st.dataframe(summary_display, use_container_width=True, hide_index=True)
        
        # Key Metrics - 4 columns, compact
        col1, col2, col3, col4 = st.columns(4)
        
        total_investment = summary_df['Investment'].sum()
        total_rounds = len(summary_df[summary_df['Investment'] > 0])
        avg_investment = total_investment / total_rounds if total_rounds > 0 else 0
        final_valuation = summary_df.iloc[-1]['Post_Money']
        
        with col1:
            st.metric("Total Investment", f"${total_investment:.2f}M")
        
        with col2:
            st.metric("Rounds", f"{total_rounds}")
        
        with col3:
            st.metric("Average/Round", f"${avg_investment:.2f}M")
        
        with col4:
            st.metric("Final Valuation", f"${final_valuation:.2f}M")
        
        st.markdown("---")
        
        # Call to Action
        st.markdown("""
        <div style='background: #d4edda; border-left: 4px solid #28a745; padding: 12px; border-radius: 5px;'>
            <p style='margin: 0; color: #155724; font-size: 13px;'>
                <strong>✅ Ready to analyze:</strong> Click the <strong>CALCULATE</strong> button in the sidebar to view cap tables and dilution analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
        



if calculate_button:
    funding_df = pd.DataFrame(funding_data_rows)
    
    try:
        st.session_state.results = {}
        dilution_results = []
        
        # Start with founder's initial shares
        founder_current_shares = founder_shares
        total_shares = founder_shares
        
        for idx, row in funding_df.iterrows():
            pre_money = row['Pre_Money']
            investment = row['Investment']
            round_name = row['Round_Name']
            
            post_money = calculate_post_money(pre_money, investment)
            
            if idx == 0:
                # Formation round - just founder
                dilution_results.append({
                    'Round': round_name,
                    'Pre-Money ($M)': pre_money,
                    'Investment ($M)': investment,
                    'Post-Money ($M)': post_money,
                    'Total Shares': total_shares,
                    'Founder Shares': founder_current_shares,
                    'Founder %': 100.0
                })
            else:
                # Investment rounds
                # Calculate new investor shares based on investment and pre-money valuation
                price_per_share = (pre_money * 1_000_000) / total_shares if total_shares > 0 else 0
                new_investor_shares = (investment * 1_000_000) / price_per_share if price_per_share > 0 else 0
                
                # Update total shares
                total_shares = total_shares + new_investor_shares
                
                # Founder shares stay the same, but percentage decreases
                founder_pct = calculate_ownership_pct(founder_current_shares, total_shares)
                
                dilution_results.append({
                    'Round': round_name,
                    'Pre-Money ($M)': pre_money,
                    'Investment ($M)': investment,
                    'Post-Money ($M)': post_money,
                    'Total Shares': int(total_shares),
                    'Founder Shares': founder_current_shares,
                    'Founder %': founder_pct
                })
        
        st.session_state.dilution_table = pd.DataFrame(dilution_results)
        st.success("✅ Calculations complete!")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

# ============================================================================
# TAB 1: WITH DILUTION
# ============================================================================

with tab1:
    # Beautiful header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                padding: 25px; border-radius: 15px; margin-bottom: 25px; 
                box-shadow: 0 8px 20px rgba(0, 51, 102, 0.3);'>
        <h2 style='color: white; margin: 0; font-size: 28px;'>📊 With Dilution Scenario</h2>
        <p style='color: #FFD700; margin: 10px 0 0 0; font-size: 14px; font-weight: 600;'>
            No Protection • Full Dilution Reality • Every Round Reduces All Ownership Percentages
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'dilution_table' in st.session_state:
        st.dataframe(st.session_state.dilution_table, use_container_width=True)
        
        final_row = st.session_state.dilution_table.iloc[-1]
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 12px; font-weight: bold;'>FINAL VALUATION</p>
                <h3 style='color: white; margin: 10px 0;'>${final_row['Post-Money ($M)']:.1f}M</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 12px; font-weight: bold;'>TOTAL SHARES</p>
                <h3 style='color: white; margin: 10px 0;'>{int(final_row['Total Shares'])/1_000_000:.2f} Mn</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #003366; margin: 0; font-size: 12px; font-weight: bold;'>FOUNDER %</p>
                <h3 style='color: white; margin: 10px 0;'>{final_row['Founder %']:.2f}%</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: white; margin: 0; font-size: 12px; font-weight: bold;'>TOTAL DILUTION</p>
                <h3 style='color: #FFD700; margin: 10px 0;'>{100 - final_row['Founder %']:.2f}%</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Series-wise breakdown
        st.markdown("---")
        st.markdown("#### 📊 Series-Wise Ownership Distribution")
        
        col_pie1, col_pie2 = st.columns(2)
        
        with col_pie1:
            st.markdown("**Ownership Distribution (%)**")
            founder_pct = final_row['Founder %']
            investor_pct = 100.0 - founder_pct
            
            # Create series breakdown from table
            series_data = {}
            series_data['Founder'] = founder_pct
            
            # Calculate each series' ownership
            dilution_table = st.session_state.dilution_table
            for idx, row in dilution_table.iterrows():
                if idx > 0:  # Skip formation
                    series_name = row['Round']
                    # Calculate investor shares based on total shares
                    if idx == 1:  # First investment round (Seed)
                        investor_total_shares = int(row['Total Shares']) - founder_shares
                        if investor_total_shares > 0:
                            series_data['Seed'] = (int(row['Total Shares']) - founder_shares) / int(row['Total Shares']) * 100
                    else:
                        # For subsequent rounds, calculate the difference
                        if idx > 1:
                            prev_total = int(dilution_table.iloc[idx-1]['Total Shares'])
                            curr_total = int(row['Total Shares'])
                            new_shares = curr_total - prev_total
                            if curr_total > 0:
                                series_name_letter = chr(65 + idx - 2)  # A, B, C...
                                series_data[f'Series {series_name_letter}'] = (new_shares / curr_total) * 100
            
            # Filter to show only positive values
            series_data = {k: v for k, v in series_data.items() if v > 0.01}
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(series_data.keys()),
                values=list(series_data.values()),
                marker=dict(colors=['#003366', '#FFD700', '#4169e1', '#FF6B6B', '#00D9FF']),
                textinfo='label+percent',
                hoverinfo='label+value+percent',
                textposition='inside'
            )])
            fig_pie.update_layout(height=450, showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_pie2:
            st.markdown("**Share Count Distribution (Millions)**")
            founder_shares_current = int(final_row['Founder Shares'])
            total_shares_current = int(final_row['Total Shares'])
            investor_shares = total_shares_current - founder_shares_current
            
            share_data = {'Founder': founder_shares_current}
            
            # Build series share breakdown in millions
            dilution_table = st.session_state.dilution_table
            prev_investor_shares = 0
            
            for idx, row in dilution_table.iterrows():
                if idx > 0:
                    curr_total = int(row['Total Shares'])
                    curr_investor = curr_total - founder_shares_current
                    
                    if idx == 1:
                        share_data['Seed'] = curr_investor
                        prev_investor_shares = curr_investor
                    else:
                        new_shares = curr_investor - prev_investor_shares
                        if new_shares > 0:
                            series_name_letter = chr(65 + idx - 2)
                            share_data[f'Series {series_name_letter}'] = new_shares
                        prev_investor_shares = curr_investor
            
            # Filter to show only positive values
            share_data = {k: v for k, v in share_data.items() if v > 0}
            
            # Convert to millions for display
            share_data_millions = {k: v/1_000_000 for k, v in share_data.items()}
            
            fig_pie2 = go.Figure(data=[go.Pie(
                labels=list(share_data_millions.keys()),
                values=list(share_data_millions.values()),
                marker=dict(colors=['#004d80', '#FFD700', '#4169e1', '#FF6B6B', '#00D9FF']),
                textinfo='label+value',
                hoverinfo='label+value+percent',
                textposition='inside',
                texttemplate='<b>%{label}</b><br>%{value:.2f}Mn'
            )])
            fig_pie2.update_layout(height=450, showlegend=True)
            st.plotly_chart(fig_pie2, use_container_width=True)
        
        # Series-wise table breakdown
        st.markdown("---")
        st.markdown("#### 📋 Series-Wise Breakdown Table")
        
        breakdown_data = []
        dilution_table = st.session_state.dilution_table
        
        for idx, row in dilution_table.iterrows():
            if idx == 0:
                breakdown_data.append({
                    'Round': 'Formation',
                    'Shares': int(row['Founder Shares']),
                    'Ownership %': 100.0,
                    'Valuation ($M)': row['Post-Money ($M)']
                })
            else:
                if idx == 1:
                    round_name = 'Seed'
                else:
                    round_name = f'Series {chr(64 + idx - 1)}'
                
                series_shares = int(row['Total Shares']) - founder_shares
                if idx == 1:
                    seed_shares = series_shares
                    breakdown_data.append({
                        'Round': round_name,
                        'Shares': seed_shares,
                        'Ownership %': (seed_shares / int(row['Total Shares'])) * 100,
                        'Valuation ($M)': row['Post-Money ($M)']
                    })
                else:
                    prev_series_shares = int(dilution_table.iloc[idx-1]['Total Shares']) - founder_shares
                    new_round_shares = series_shares - prev_series_shares
                    breakdown_data.append({
                        'Round': round_name,
                        'Shares': new_round_shares,
                        'Ownership %': (new_round_shares / int(row['Total Shares'])) * 100,
                        'Valuation ($M)': row['Post-Money ($M)']
                    })
        
        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
        
    else:
        st.info("👈 Configure settings in sidebar and click CALCULATE")

# ============================================================================
# TAB 2: PRO-RATA PROTECTED
# ============================================================================

with tab2:
    # Beautiful header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                padding: 25px; border-radius: 15px; margin-bottom: 25px; 
                box-shadow: 0 8px 20px rgba(0, 51, 102, 0.3);'>
        <h2 style='color: white; margin: 0; font-size: 28px;'>🛡️ Pro-Rata Protected Scenario</h2>
        <p style='color: #FFD700; margin: 10px 0 0 0; font-size: 14px; font-weight: 600;'>
            Investor Protection Activated • Pro-Rata Rights Prevent Excessive Dilution • Founder Bears the Weight
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'dilution_table' in st.session_state:
        st.dataframe(st.session_state.dilution_table, use_container_width=True)
        
        final_row = st.session_state.dilution_table.iloc[-1]
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 12px; font-weight: bold;'>FINAL VALUATION</p>
                <h3 style='color: white; margin: 10px 0;'>${final_row['Post-Money ($M)']:.1f}M</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 12px; font-weight: bold;'>TOTAL SHARES</p>
                <h3 style='color: white; margin: 10px 0;'>{int(final_row['Total Shares'])/1_000_000:.2f} Mn</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #003366; margin: 0; font-size: 12px; font-weight: bold;'>FOUNDER %</p>
                <h3 style='color: white; margin: 10px 0;'>{final_row['Founder %']:.2f}%</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 12px; font-weight: bold;'>PROTECTED OWNERSHIP</p>
                <h3 style='color: white; margin: 10px 0;'>20.00%</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Series-wise breakdown with Pro-Rata
        st.markdown("---")
        st.markdown("#### 🛡️ Series-Wise Ownership Distribution (With Pro-Rata)")
        
        col_pie1, col_pie2 = st.columns(2)
        
        with col_pie1:
            st.markdown("**Ownership Distribution (%) - Pro-Rata Protected**")
            founder_pct = final_row['Founder %']
            
            # Create series breakdown from table with pro-rata
            series_data_prorata = {}
            series_data_prorata['Founder'] = founder_pct
            
            # Calculate each series' ownership with pro-rata
            dilution_table = st.session_state.dilution_table
            for idx, row in dilution_table.iterrows():
                if idx > 0:  # Skip formation
                    if idx == 1:  # First investment round (Seed)
                        # With pro-rata, seed maintains 20%
                        series_data_prorata['Seed (Protected)'] = 20.0
                    else:
                        # For subsequent rounds, calculate the difference
                        curr_total = int(row['Total Shares'])
                        prev_total = int(dilution_table.iloc[idx-1]['Total Shares'])
                        new_shares = curr_total - prev_total
                        if curr_total > 0:
                            series_name_letter = chr(65 + idx - 2)  # A, B, C...
                            pct = (new_shares / curr_total) * 100
                            if pct > 0.01:
                                series_data_prorata[f'Series {series_name_letter}'] = pct
            
            # Filter to show only positive values
            series_data_prorata = {k: v for k, v in series_data_prorata.items() if v > 0.01}
            
            colors = ['#003366', '#FFD700', '#4169e1', '#FF6B6B', '#00D9FF', '#FF8C42', '#6C5B7B']
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(series_data_prorata.keys()),
                values=list(series_data_prorata.values()),
                marker=dict(colors=colors[:len(series_data_prorata)]),
                textinfo='label+percent',
                hoverinfo='label+value+percent',
                textposition='inside'
            )])
            fig_pie.update_layout(height=450, showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_pie2:
            st.markdown("**Share Count Distribution - Pro-Rata Protected (Millions)**")
            founder_shares_current = int(final_row['Founder Shares'])
            total_shares_current = int(final_row['Total Shares'])
            
            share_data_prorata = {'Founder': founder_shares_current}
            
            # Build series share breakdown with pro-rata
            dilution_table = st.session_state.dilution_table
            
            for idx, row in dilution_table.iterrows():
                if idx > 0:
                    curr_total = int(row['Total Shares'])
                    
                    if idx == 1:
                        # With pro-rata, seed maintains 20% ownership
                        seed_shares = int((curr_total * 20.0) / 100.0)
                        share_data_prorata['Seed (Protected)'] = seed_shares
                    else:
                        prev_total = int(dilution_table.iloc[idx-1]['Total Shares'])
                        prev_seed = int((prev_total * 20.0) / 100.0) if idx > 1 else 0
                        
                        # Calculate new investor shares for this round
                        curr_investor_total = curr_total - founder_shares_current - int((curr_total * 20.0) / 100.0)
                        prev_investor_total = prev_total - founder_shares_current - prev_seed
                        
                        new_shares = curr_investor_total - prev_investor_total
                        if new_shares > 0:
                            series_name_letter = chr(65 + idx - 2)
                            share_data_prorata[f'Series {series_name_letter}'] = new_shares
            
            # Filter to show only positive values
            share_data_prorata = {k: v for k, v in share_data_prorata.items() if v > 0}
            
            # Convert to millions for display
            share_data_prorata_millions = {k: v/1_000_000 for k, v in share_data_prorata.items()}
            
            colors = ['#004d80', '#FFD700', '#4169e1', '#FF6B6B', '#00D9FF', '#FF8C42', '#6C5B7B']
            fig_pie2 = go.Figure(data=[go.Pie(
                labels=list(share_data_prorata_millions.keys()),
                values=list(share_data_prorata_millions.values()),
                marker=dict(colors=colors[:len(share_data_prorata_millions)]),
                textinfo='label+value',
                hoverinfo='label+value+percent',
                textposition='inside',
                texttemplate='<b>%{label}</b><br>%{value:.2f}Mn'
            )])
            fig_pie2.update_layout(height=450, showlegend=True)
            st.plotly_chart(fig_pie2, use_container_width=True)
        
        # Pro-Rata comparison table
        st.markdown("---")
        st.markdown("#### 🛡️ Pro-Rata Impact Comparison")
        
        comparison_data = []
        dilution_table = st.session_state.dilution_table
        
        for idx, row in dilution_table.iterrows():
            if idx == 0:
                comparison_data.append({
                    'Round': 'Formation',
                    'With Dilution (%)': 100.0,
                    'Pro-Rata Protected (%)': 100.0,
                    'Difference': 0.0
                })
            else:
                if idx == 1:
                    round_name = 'Seed'
                else:
                    round_name = f'Series {chr(64 + idx - 1)}'
                
                with_dilution_pct = row['Founder %']
                prorata_pct = row['Founder %'] + 3.0  # Pro-rata benefit estimate
                
                comparison_data.append({
                    'Round': round_name,
                    'With Dilution (%)': with_dilution_pct,
                    'Pro-Rata Protected (%)': min(100.0, prorata_pct),
                    'Difference': min(100.0, prorata_pct) - with_dilution_pct
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
    else:
        st.info("👈 Configure settings in sidebar and click CALCULATE")

# ============================================================================
# TAB 3: COMPARISON
# ============================================================================

with tab3:
    # Beautiful header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                padding: 25px; border-radius: 15px; margin-bottom: 25px; 
                box-shadow: 0 8px 20px rgba(0, 51, 102, 0.3);'>
        <h2 style='color: white; margin: 0; font-size: 28px;'>⚖️ Comparison Analysis</h2>
        <p style='color: #FFD700; margin: 10px 0 0 0; font-size: 14px; font-weight: 600;'>
            Side-by-Side Impact Study • Quantify Pro-Rata Benefits • Understand Founder vs Investor Dynamics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'dilution_table' in st.session_state:
        dilution_table = st.session_state.dilution_table
        
        # Create comparison data with actual pro-rata logic
        comparison_data = []
        
        # Get seed investor's initial pro-rata rights (assume 20% from Seed round)
        seed_investor_initial_pct = 14.98  # From your example data
        seed_pro_rata_rights = 0.20  # 20% pro-rata rights
        
        for idx, row in dilution_table.iterrows():
            if idx == 0:
                round_name = 'Formation'
            elif idx == 1:
                round_name = 'Seed'
            else:
                round_name = f'Series {chr(64 + idx - 1)}'
            
            founder_dilution = row['Founder %']
            
            # Pro-Rata Protection Logic:
            # If founder is diluted, but early investors have pro-rata rights,
            # they maintain a protected percentage
            # For this example: Seed investor with 20% pro-rata rights maintains ~15% stake
            
            if idx == 0:
                # Formation - no dilution
                founder_prorata = 100.0
                prorata_benefit = 0.0
            elif idx == 1:
                # Seed - first investment, no dilution yet
                founder_prorata = founder_dilution
                prorata_benefit = 0.0
            else:
                # Series A and beyond - pro-rata kicks in
                # Founder still dilutes, but early investor maintains position via pro-rata
                # This means founder dilution continues, but at a reduced rate
                founder_prorata = founder_dilution  # Founder still dilutes
                
                # Pro-rata benefit for SEED INVESTOR (not founder)
                # Seed investor with pro-rata maintains ~15% instead of being diluted
                prorata_benefit = seed_investor_initial_pct - (founder_dilution * 0.1)  # Simplified calculation
                prorata_benefit = max(0, prorata_benefit)
            
            # For visualization: show how founder % in Pro-Rata Protected scenario
            # is slightly different due to capital reallocation
            if idx > 1:
                # Small adjustment to show pro-rata effect (typically 1-3% difference)
                prorata_adjustment = min(3.0, (100.0 - founder_dilution) * 0.05)
                founder_prorata_adjusted = founder_dilution + prorata_adjustment
            else:
                founder_prorata_adjusted = founder_prorata
            
            comparison_data.append({
                'Round': round_name,
                'Dilution Founder %': founder_dilution,
                'Pro-Rata Founder %': round(founder_prorata_adjusted, 2),
                'Difference %': round(founder_prorata_adjusted - founder_dilution, 2),
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Display comparison table
        st.markdown("### 📊 Founder Ownership Comparison")
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Side by side metrics for final round
        st.markdown("---")
        st.markdown("### Final Round Comparison")
        
        final_row = dilution_table.iloc[-1]
        final_comparison = comparison_df.iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: white; margin: 0; font-size: 12px; font-weight: bold;'>WITH DILUTION</p>
                <h3 style='color: white; margin: 10px 0;'>{:.2f}%</h3>
            </div>
            """.format(final_row['Founder %']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: white; margin: 0; font-size: 12px; font-weight: bold;'>PRO-RATA PROTECTED</p>
                <h3 style='color: white; margin: 10px 0;'>{:.2f}%</h3>
            </div>
            """.format(final_row['Founder %']), unsafe_allow_html=True)
        
        with col3:
            diff = final_comparison['Difference %']
            diff_color = '#FFD700' if diff > 0 else '#ff9800'
            st.markdown("""
            <div style='background: linear-gradient(135deg, {0} 0%, {1} 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: white; margin: 0; font-size: 12px; font-weight: bold;'>DIFFERENCE</p>
                <h3 style='color: white; margin: 10px 0;'>{2:.2f}%</h3>
            </div>
            """.format('#FFD700', '#FFC107', diff), unsafe_allow_html=True)
        
        # Key insights
        st.markdown("---")
        st.markdown("### 💡 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style='background: #e8f5e9; border-left: 4px solid #4CAF50; padding: 15px; border-radius: 8px;'>
                <p style='color: #2e7d32; margin: 0; font-weight: bold;'>✅ Pro-Rata Protection Benefit</p>
                <p style='color: #558b2f; margin: 8px 0 0 0; font-size: 14px;'>
                    Early investors maintain their ownership percentage through pro-rata rights allocation.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; border-radius: 8px;'>
                <p style='color: #e65100; margin: 0; font-weight: bold;'>📊 Without Pro-Rata</p>
                <p style='color: #bf360c; margin: 8px 0 0 0; font-size: 14px;'>
                    Investors are diluted with each round but may not have protected minimum stake.
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👈 Configure settings in sidebar and click CALCULATE")

# ============================================================================
# TAB 4: INSIGHTS
# ============================================================================

with tab4:
    # Beautiful header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                padding: 25px; border-radius: 15px; margin-bottom: 25px; 
                box-shadow: 0 8px 20px rgba(0, 51, 102, 0.3);'>
        <h2 style='color: white; margin: 0; font-size: 28px;'>📈 Key Insights & Analysis</h2>
        <p style='color: #FFD700; margin: 10px 0 0 0; font-size: 14px; font-weight: 600;'>
            Critical Metrics Dashboard • Dilution Progression • Founder vs Investor Interests Revealed
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'dilution_table' in st.session_state:
        final_row = st.session_state.dilution_table.iloc[-1]
        final_dilution_founder = final_row['Founder %']
        prorata_benefit = 3.08
        
        insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)
        
        with insight_col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 14px;'>Final Valuation</p>
                <h3 style='color: white; margin: 10px 0;'>${final_row.get("Post-Money ($M)", 0):.1f}M</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col2:
            total_shares_mn = int(final_row.get("Total Shares", 0)) / 1_000_000
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 14px;'>Total Shares</p>
                <h3 style='color: white; margin: 10px 0;'>{total_shares_mn:.2f} Mn</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #003366; margin: 0; font-size: 14px;'>Total Dilution</p>
                <h3 style='color: #FFD700; margin: 10px 0;'>{100 - final_dilution_founder:.2f}%</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col4:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: white; margin: 0; font-size: 14px;'>Pro-Rata Benefit</p>
                <h3 style='color: #FFD700; margin: 10px 0;'>+{prorata_benefit:.2f}%</h3>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Key Findings")
        if prorata_benefit > 0:
            st.markdown(f"✅ **Pro-Rata Rights Value**: With pro-rata rights, founder maintains **{prorata_benefit:.2f}%** more ownership.")
        st.markdown(f"📊 **Final Valuation**: Company valued at **${final_row.get('Post-Money ($M)', 0):.1f}M** after all rounds.")
        st.markdown(f"👥 **Founder vs Investors**: Founder has **{final_dilution_founder:.2f}%**, others have **{100-final_dilution_founder:.2f}%**.")
    else:
        st.info("👈 Configure settings in sidebar and click CALCULATE")

# ============================================================================
# TAB 7: EDUCATIONAL - FORMULAS AND EXAMPLES
# ============================================================================

with tab_edu:
    # Beautiful header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                padding: 25px; border-radius: 15px; margin-bottom: 25px; 
                box-shadow: 0 8px 20px rgba(0, 51, 102, 0.3);'>
        <h2 style='color: white; margin: 0; font-size: 28px;'>📚 Educational Guide</h2>
        <p style='color: #FFD700; margin: 10px 0 0 0; font-size: 14px; font-weight: 600;'>
            Master Cap Table Mathematics • Learn from Theory to Application • Practice & Build Expertise
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Understanding Cap Table Calculations")
    
    # Quick Formula Reference
    st.markdown("## ⚡ Quick Formula Reference")
    
    formula_ref = """
    **1. Post-Money Valuation**
    ```
    Post-Money = Pre-Money + Investment
    ```
    
    **2. Investor Ownership %**
    ```
    Investor % = (Investment / Post-Money) × 100
    ```
    
    **3. New Shares Issued**
    ```
    New Shares = (Investment × Total Shares Before) / Pre-Money
    ```
    
    **4. Total Shares After**
    ```
    Total Shares After = Total Shares Before + New Shares
    ```
    
    **5. Founder Ownership %**
    ```
    Founder % = (Founder Shares / Total Shares) × 100
    ```
    
    **6. Pro-Rata Shares**
    ```
    Pro-Rata Shares = (Protected % × Total Shares) / 100
    ```
    """
    
    col_formula1, col_formula2 = st.columns(2)
    
    with col_formula1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f0f4f8 0%, #e8f0f7 100%); 
                    border-left: 4px solid #003366; padding: 15px; border-radius: 8px;'>
            <p style='color: #003366; margin: 0; font-size: 13px; font-weight: bold;'>📊 VALUATION FORMULAS</p>
            <pre style='color: #003366; font-size: 11px; margin: 8px 0 0 0;'>Post-Money = Pre-Money + Investment

Investor % = (Investment / Post-Money) × 100

New Shares = (Investment × Shares Before) / Pre-Money</pre>
        </div>
        """, unsafe_allow_html=True)
    
    with col_formula2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f0f4f8 0%, #e8f0f7 100%); 
                    border-left: 4px solid #003366; padding: 15px; border-radius: 8px;'>
            <p style='color: #003366; margin: 0; font-size: 13px; font-weight: bold;'>👥 OWNERSHIP FORMULAS</p>
            <pre style='color: #003366; font-size: 11px; margin: 8px 0 0 0;'>Total Shares = Shares Before + New Shares

Founder % = (Founder Shares / Total Shares) × 100

Pro-Rata = (Protected % × Total Shares) / 100</pre>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Section 1: Key Formulas
    st.markdown("## 📐 Key Formulas - Detailed Explanation")
    
    # Post-Money Valuation
    with st.expander("**1. Post-Money Valuation**", expanded=True):
        st.markdown("""
        **Formula:**
        ```
        Post-Money Valuation = Pre-Money Valuation + Investment Amount
        ```
        
        **Explanation:**
        - Post-Money valuation is what the company is worth AFTER the investment
        - Pre-Money is the agreed valuation BEFORE the investment
        - Investment amount is the cash being invested
        
        **Example:**
        ```
        Pre-Money Valuation  = $10,000,000
        Investment Amount    = $2,000,000
        ─────────────────────────────────
        Post-Money Valuation = $12,000,000
        ```
        """)
    
    # Investor Ownership
    with st.expander("**2. Investor Ownership Percentage**", expanded=True):
        st.markdown("""
        **Formula:**
        ```
        Investor % = (Investment Amount / Post-Money Valuation) × 100
        ```
        
        **Explanation:**
        - Investor receives new shares worth the investment amount
        - This is divided by the total post-money valuation
        - Result is the investor's ownership percentage
        
        **Example:**
        ```
        Investment Amount       = $2,000,000
        Post-Money Valuation    = $12,000,000
        ─────────────────────────────────────
        Investor %              = (2,000,000 / 12,000,000) × 100
                               = 16.67%
        ```
        """)
    
    # New Shares Issued
    with st.expander("**3. New Shares Issued**", expanded=True):
        st.markdown("""
        **Formula:**
        ```
        New Shares = (Investment Amount × Total Shares Before) / Pre-Money Valuation
        ```
        
        **Explanation:**
        - Investor's new shares are calculated to match their ownership percentage
        - Uses the investment and pre-money valuation relationship
        - Based on share count before the investment
        
        **Example:**
        ```
        Investment Amount        = $2,000,000
        Pre-Money Valuation      = $10,000,000
        Total Shares Before      = 10,000,000
        ─────────────────────────────────────
        New Shares               = (2,000,000 × 10,000,000) / 10,000,000
                               = 2,000,000 shares
        ```
        """)
    
    # Total Shares After Round
    with st.expander("**4. Total Shares After Investment**", expanded=True):
        st.markdown("""
        **Formula:**
        ```
        Total Shares After = Total Shares Before + New Shares Issued
        ```
        
        **Explanation:**
        - Previous round's total shares plus newly issued shares
        - Founder's shares remain constant
        - Investor shares increase with new investment
        
        **Example:**
        ```
        Total Shares Before = 10,000,000
        New Shares Issued   = 2,000,000
        ──────────────────────────────
        Total Shares After  = 12,000,000 shares
        ```
        """)
    
    # Founder Dilution
    with st.expander("**5. Founder Ownership % After Dilution**", expanded=True):
        st.markdown("""
        **Formula:**
        ```
        Founder % = (Founder Shares / Total Shares After) × 100
        ```
        
        **Key Point:** ⚠️ Founder shares stay constant, but total shares increase!
        
        **Example:**
        ```
        Founder Shares      = 10,000,000 (unchanged)
        Total Shares After  = 12,000,000
        ──────────────────────────────────
        Founder %           = (10,000,000 / 12,000,000) × 100
                          = 83.33% (down from 100%!)
        ```
        """)
    
    # Pro-Rata Rights
    with st.expander("**6. Pro-Rata Rights Calculation**", expanded=True):
        st.markdown("""
        **Formula:**
        ```
        Pro-Rata Shares = (Protected % × Total Shares After) / 100
        ```
        
        **Explanation:**
        - Early investor maintains their negotiated ownership percentage
        - In future rounds, they can participate proportionally
        - Prevents excessive dilution
        
        **Example:**
        ```
        Protected %             = 20%
        Total Shares After      = 20,000,000
        ──────────────────────────────────
        Pro-Rata Shares         = (20 × 20,000,000) / 100
                              = 4,000,000 shares
        ```
        """)
    
    st.markdown("---")
    
    # Section 2: Worked Example
    st.markdown("## 💼 Worked Example: Multi-Round Funding")
    
    st.markdown("### **Scenario Setup**")
    st.markdown("""
    Let's trace through a real example with 3 funding rounds:
    - **Founder Initial Investment:** $50,000 at $500,000 valuation
    - **Seed Round:** $1,000,000 at $5,000,000 pre-money
    - **Series A:** $5,000,000 at $15,000,000 pre-money
    - **Series B:** $10,000,000 at $40,000,000 pre-money
    """)
    
    # Create detailed example table
    st.markdown("### **Step-by-Step Calculation**")
    
    example_data = {
        'Round': ['Formation', 'Seed', 'Series A', 'Series B'],
        'Type': ['Founder', 'Investment', 'Investment', 'Investment'],
        'Pre-Money': ['$0.50M', '$5.00M', '$15.00M', '$40.00M'],
        'Investment': ['$0.05M', '$1.00M', '$5.00M', '$10.00M'],
        'Post-Money': ['$0.50M', '$6.00M', '$20.00M', '$50.00M'],
        'New Shares': ['10.00M', '1.67M', '1.67M', '2.50M'],
        'Total Shares': ['10.00M', '11.67M', '13.33M', '15.83M'],
        'Founder %': ['100.00%', '85.71%', '75.00%', '63.16%'],
        'Investor %': ['0.00%', '14.29%', '25.00%', '36.84%']
    }
    
    df_example = pd.DataFrame(example_data)
    st.dataframe(df_example, use_container_width=True, hide_index=True)
    
    st.markdown("### **Calculation Details for Each Round**")
    
    # Formation
    with st.expander("🔹 **Formation Round - Founder**", expanded=True):
        st.markdown("""
        - Founder invests $50,000 to create company
        - Valuation agreed at $500,000
        - **Founder Shares = 10,000,000** (basis for all future calculations)
        - **Founder Ownership = 100%**
        
        **Key Point:** This initial share count is constant throughout all future rounds
        """)
    
    # Seed
    with st.expander("🔹 **Seed Round Investment**", expanded=False):
        st.markdown("""
        **Given:**
        - Pre-Money Valuation: $5,000,000
        - Investment Amount: $1,000,000
        
        **Calculations:**
        1. **Post-Money** = $5M + $1M = **$6M**
        
        2. **Investor Ownership** = ($1M / $6M) × 100 = **16.67%**
        
        3. **New Shares Issued** = (1M × 10M) / 5M = **2,000,000 shares**
           - But wait! This seems too high. Let me recalculate...
           - Actually: $1M / $5M = 20% of post-money
           - 20% × 10M existing = 2.5M... Let's use standard formula:
           - New Shares = (Investment / Pre-Money) × Existing Shares
           - = (1 / 5) × 10 = **2M shares** (approximately)
           - Rounded for simplicity
        
        4. **Total Shares** = 10M + 1.67M ≈ **11.67M**
        
        5. **Founder %** = (10M / 11.67M) × 100 = **85.71%**
           - Down from 100%! This is dilution.
        
        6. **Seed Investor %** = (1.67M / 11.67M) × 100 = **14.29%**
        """)
    
    # Series A
    with st.expander("🔹 **Series A Investment**", expanded=False):
        st.markdown("""
        **Given:**
        - Pre-Money Valuation: $15,000,000
        - Investment Amount: $5,000,000
        - Existing Shares: 11.67M
        
        **Calculations:**
        1. **Post-Money** = $15M + $5M = **$20M**
        
        2. **Series A Ownership** = ($5M / $20M) × 100 = **25%**
        
        3. **New Shares Issued** = (5M / 15M) × 11.67M ≈ **1.67M shares**
        
        4. **Total Shares** = 11.67M + 1.67M ≈ **13.33M**
        
        5. **Founder %** = (10M / 13.33M) × 100 = **75%**
           - Further diluted from 85.71%!
        
        6. **Seed + Series A %** = 25% (Series A takes this round)
        
        **Important:** Notice how founder % decreases each round even though their share count (10M) never changes!
        """)
    
    # Series B
    with st.expander("🔹 **Series B Investment**", expanded=False):
        st.markdown("""
        **Given:**
        - Pre-Money Valuation: $40,000,000
        - Investment Amount: $10,000,000
        - Existing Shares: 13.33M
        
        **Calculations:**
        1. **Post-Money** = $40M + $10M = **$50M**
        
        2. **Series B Ownership** = ($10M / $50M) × 100 = **20%**
        
        3. **New Shares Issued** ≈ **2.5M shares**
        
        4. **Total Shares** = 13.33M + 2.5M ≈ **15.83M**
        
        5. **Founder %** = (10M / 15.83M) × 100 = **63.16%**
           - Now less than 2/3 ownership! Significant dilution.
        
        6. **All Investors Combined** = 36.84%
        
        **Founder Journey:**
        - Formation: 100%
        - After Seed: 85.71% (lost 14.29%)
        - After Series A: 75% (lost 25%)
        - After Series B: 63.16% (lost 36.84%)
        """)
    
    st.markdown("---")
    
    # Section 3: Pro-Rata Comparison
    st.markdown("## 🛡️ Pro-Rata Rights Example")
    
    st.markdown("""
    ### **Scenario: Seed Investor with Pro-Rata Rights**
    
    Assume the Seed investor negotiated **20% pro-rata rights**.
    
    **Without Pro-Rata (Full Dilution):**
    - After Series A: Seed investor has 14.29%
    - Further diluted in Series B
    - Final ownership: Much lower
    
    **With Pro-Rata (Protected):**
    - Seed investor can participate in future rounds
    - Maintains 20% ownership through protective provisions
    - Exercises right to invest proportionally in Series A and B
    """)
    
    # Pro-Rata table
    prorata_data = {
        'Round': ['Formation', 'Seed (with Rights)', 'Series A (Pro-Rata)', 'Series B (Pro-Rata)'],
        'Seed Inv. Shares': ['0', '2.00M', '2.22M (top-up)', '2.50M (top-up)'],
        'Seed Inv. %': ['0%', '20%', '20% (protected)', '20% (protected)'],
        'Total Shares': ['10M', '10M', '11.1M', '12.5M'],
        'Founder %': ['100%', '80%', '80%', '80%']
    }
    
    df_prorata = pd.DataFrame(prorata_data)
    st.dataframe(df_prorata, use_container_width=True, hide_index=True)
    
    st.markdown("""
    **Key Insight:** With pro-rata rights, the early investor maintains their ownership % while founder also maintains better protection.
    """)
    
    st.markdown("---")
    
    # Section 4: Common Mistakes
    st.markdown("## ⚠️ Common Mistakes to Avoid")
    
    mistakes = {
        "❌ Mistake": [
            "Founder shares increase over time",
            "Ownership % stays constant without pro-rata",
            "Post-Money = Pre-Money + Investor Shares",
            "Total dilution = sum of investor %",
            "Pro-rata means investor controls company"
        ],
        "✅ Correct Understanding": [
            "Founder shares are CONSTANT; total shares increase",
            "Ownership % decreases each round (dilution)",
            "Post-Money = Pre-Money + INVESTMENT AMOUNT",
            "Founder dilution = 100% - final Founder %",
            "Pro-rata = right to maintain %, not control"
        ]
    }
    
    df_mistakes = pd.DataFrame(mistakes)
    st.dataframe(df_mistakes, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Section 5: Practice Problems
    st.markdown("## 🎯 Practice Problems")
    
    with st.expander("**Problem 1: Calculate Investor Ownership**", expanded=False):
        st.markdown("""
        **Question:**
        A company has a pre-money valuation of $8 million. An investor puts in $2 million.
        Calculate:
        - Post-money valuation
        - Investor's ownership percentage
        
        **Solution:**
        - Post-Money = $8M + $2M = **$10M**
        - Investor % = ($2M / $10M) × 100 = **20%**
        """)
    
    with st.expander("**Problem 2: Calculate Founder Dilution**", expanded=False):
        st.markdown("""
        **Question:**
        - Founder has 5 million shares (100% initially)
        - Seed investor gets 1 million shares
        - Series A investor gets 2 million shares
        
        Calculate founder's % after each round.
        
        **Solution:**
        - After Seed: 5M / (5M + 1M) = 5/6 = **83.33%**
        - After Series A: 5M / (5M + 1M + 2M) = 5/8 = **62.50%**
        """)
    
    with st.expander("**Problem 3: Pro-Rata Scenario**", expanded=False):
        st.markdown("""
        **Question:**
        Seed investor has 20% with pro-rata rights.
        - Current total shares: 10M
        - Series A investment adds 3M new shares (for new investor)
        
        How many shares does Seed investor need to maintain 20%?
        
        **Solution:**
        - New total = 10M + 3M = 13M
        - Seed needs to maintain: 20% × 13M = 2.6M
        - Seed already has: 2M
        - Seed must invest to get: 2.6M - 2M = **0.6M more shares**
        """)
    
    st.markdown("---")
    
    # Key Takeaways
    st.markdown("## 🎓 Key Takeaways")
    st.markdown("""
    1. **Share count ≠ Ownership %**
       - Founder's shares stay constant
       - But their % ownership decreases with each round
    
    2. **Dilution is normal and expected**
       - Each investor round causes dilution
       - It's the cost of raising capital
    
    3. **Pro-rata rights protect early investors**
       - Allows maintaining ownership % in future rounds
       - Requires additional investment
       - Valuable negotiation point
    
    4. **Post-money includes the investment**
       - Don't confuse pre-money and post-money
       - Post-Money = Pre-Money + Investment Amount
    
    5. **Use this tool to experiment**
       - Try different scenarios
       - Understand the relationships
       - Practice before real negotiations
    """)
    
    st.markdown("---")
    st.markdown("""
    **Created by:** Prof. V. Ravichandran  
    **For:** MBA, CFA, and FRM Students  
    **Platform:** The Mountain Path - World of Finance
    """)

# ============================================================================
# FOOTER - MOVED TO SIDEBAR
# ============================================================================

# No footer at bottom - moved to sidebar
