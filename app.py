
"""
Cap Table Simulator Pro - Enhanced Streamlit Application
Professional Startup Equity Analysis Dashboard
The Mountain Path - World of Finance

Features:
- Dynamic funding rounds (1-7)
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

# ============================================================================
# COLOR SCHEME & BRANDING
# ============================================================================

DARK_BLUE = "#003366"
LIGHT_BLUE = "#0066CC"
GOLD_COLOR = "#FFD700"
BRAND_NAME = "The Mountain Path - World of Finance"

# ============================================================================
# PROFESSIONAL CSS STYLING
# ============================================================================
st.markdown(f"""
    <style>
    /* Hero Title - Gradient Background */
    .hero-title {{ 
        background: linear-gradient(135deg, {DARK_BLUE} 0%, {LIGHT_BLUE} 100%); 
        padding: 2.5rem; 
        border-radius: 20px; 
        margin: 1rem 0; 
        box-shadow: 0 8px 20px rgba(0, 51, 102, 0.3); 
        border: 3px solid {DARK_BLUE}; 
        color: white; 
        text-align: center; 
    }}
    
    .hero-title h1 {{ 
        margin: 0.5rem 0; 
        font-size: 2.5rem; 
        font-weight: 900;
        letter-spacing: 2px;
    }}
    
    .hero-title p {{ 
        margin: 0.3rem 0; 
        font-size: 1rem; 
        font-weight: 500;
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{ 
        background: linear-gradient(135deg, {DARK_BLUE} 0%, {LIGHT_BLUE} 100%) !important; 
    }}
    
    [data-testid="stSidebar"] > div > div:first-child {{ 
        background: linear-gradient(135deg, {DARK_BLUE} 0%, {LIGHT_BLUE} 100%) !important;
    }}
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] *{{
        color: {GOLD_COLOR} !important; 
        font-weight: 600 !important; 
    }}
    
    /* Button Styling */
    .stButton > button {{ 
        background: linear-gradient(135deg, {GOLD_COLOR} 0%, #FFC700 100%) !important; 
        color: {DARK_BLUE} !important; 
        font-weight: 700 !important; 
        border-radius: 10px !important; 
        width: 100%; 
        border: 2px solid {DARK_BLUE} !important;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3) !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #FFC700 0%, {GOLD_COLOR} 100%) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5) !important;
        transform: translateY(-2px) !important;
    }}
    
    /* Footer */
    .footer {{
        text-align: center; 
        color: #666; 
        padding: 2rem 1rem;
        border-top: 2px solid {DARK_BLUE};
        margin-top: 3rem;
        font-size: 13px;
    }}
    
    .footer p {{
        margin: 0.5rem 0;
    }}
    
    /* Tab Styling */
    [data-testid="stTabs"] button {{
        font-weight: 600;
    }}
    
    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: {DARK_BLUE} !important;
        border-bottom: 3px solid {GOLD_COLOR} !important;
    }}
    </style>
""", unsafe_allow_html=True)

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
    """Calculate post-money valuation"""
    return pre_money + investment

def calculate_price_per_share(pre_money, pre_round_shares):
    """Calculate price per share"""
    if pre_round_shares <= 0:
        return 0
    return (pre_money * 1_000_000) / pre_round_shares

def calculate_new_shares(investment, price_per_share):
    """Calculate new shares issued"""
    if price_per_share <= 0:
        return 0
    return (investment * 1_000_000) / price_per_share

def calculate_ownership_pct(investor_shares, total_shares):
    """Calculate ownership percentage"""
    if total_shares <= 0:
        return 0
    return (investor_shares / total_shares) * 100

def calculate_cap_table_dilution(funding_data, num_rounds, founder_shares):
    """Calculate dilution scenario cap table"""
    cap_table = []
    
    # Formation round
    cap_table.append({
        'Round': 'Formation',
        'Pre-Money ($M)': 0,
        'Investment ($M)': 0,
        'Post-Money ($M)': 0,
        'Price/Share ($)': 0,
        'New Shares': 0,
        'Founder Shares': founder_shares,
        'Seed Shares': 0,
        'Series A Shares': 0,
        'Series B Shares': 0,
        'Series C Shares': 0,
        'Series D Shares': 0,
        'Series E Shares': 0,
        'Total Shares': founder_shares,
        'Founder %': 100.0,
        'Seed %': 0.0,
        'Series A %': 0.0,
        'Series B %': 0.0,
        'Series C %': 0.0,
        'Series D %': 0.0,
        'Series E %': 0.0
    })
    
    investor_shares = {
        'Founder': founder_shares,
        'Seed': 0,
        'Series A': 0,
        'Series B': 0,
        'Series C': 0,
        'Series D': 0,
        'Series E': 0
    }
    
    prev_total_shares = founder_shares
    investor_names = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D', 'Series E']
    
    for idx, row in funding_data.iterrows():
        if idx >= num_rounds:
            break
        
        pre_money = row.get('Pre-Money ($M)', 0)
        investment = row.get('Investment ($M)', 0)
        
        # For Formation (idx=0), don't process in loop - already added above
        if idx == 0:
            continue
        
        # Skip other rounds if both pre_money and investment are 0
        if pre_money <= 0 or investment <= 0:
            continue
        
        post_money = calculate_post_money(pre_money, investment)
        price_per_share = calculate_price_per_share(pre_money, prev_total_shares)
        new_shares = calculate_new_shares(investment, price_per_share)
        
        # Investor assignment: idx=1 → Seed, idx=2 → Series A, etc.
        investor_idx = idx - 1  # Convert to 0-based index for investor_names
        current_investor = investor_names[investor_idx] if investor_idx < len(investor_names) else f'Series {investor_idx+1}'
        investor_shares[current_investor] = new_shares
        
        total_shares = sum(investor_shares.values())
        
        # Build row
        if idx == 1:
            round_name = 'Seed'
        else:
            round_name = f'Series {chr(64 + idx - 1)}'  # Series A, B, C...
        
        row_data = {
            'Round': round_name,
            'Pre-Money ($M)': round(pre_money, 2),
            'Investment ($M)': round(investment, 2),
            'Post-Money ($M)': round(post_money, 2),
            'Price/Share ($)': round(price_per_share, 4) if price_per_share > 0 else 0,
            'New Shares': int(new_shares) if new_shares > 0 else 0,
            'Founder Shares': int(investor_shares['Founder']),
            'Seed Shares': int(investor_shares.get('Seed', 0)),
            'Series A Shares': int(investor_shares.get('Series A', 0)),
            'Series B Shares': int(investor_shares.get('Series B', 0)),
            'Series C Shares': int(investor_shares.get('Series C', 0)),
            'Series D Shares': int(investor_shares.get('Series D', 0)),
            'Series E Shares': int(investor_shares.get('Series E', 0)),
            'Total Shares': int(total_shares),
            'Founder %': calculate_ownership_pct(investor_shares['Founder'], total_shares),
            'Seed %': calculate_ownership_pct(investor_shares.get('Seed', 0), total_shares),
            'Series A %': calculate_ownership_pct(investor_shares.get('Series A', 0), total_shares),
            'Series B %': calculate_ownership_pct(investor_shares.get('Series B', 0), total_shares),
            'Series C %': calculate_ownership_pct(investor_shares.get('Series C', 0), total_shares),
            'Series D %': calculate_ownership_pct(investor_shares.get('Series D', 0), total_shares),
            'Series E %': calculate_ownership_pct(investor_shares.get('Series E', 0), total_shares),
        }
        
        cap_table.append(row_data)
        prev_total_shares = total_shares
    
    return pd.DataFrame(cap_table)

def calculate_cap_table_prorata(funding_data, num_rounds, founder_shares):
    """Calculate pro-rata scenario cap table"""
    cap_table = []
    
    # Formation round
    cap_table.append({
        'Round': 'Formation',
        'Pre-Money ($M)': 0,
        'Investment ($M)': 0,
        'Post-Money ($M)': 0,
        'Price/Share ($)': 0,
        'New Shares': 0,
        'Founder Shares': founder_shares,
        'Seed Shares': 0,
        'Series A Shares': 0,
        'Series B Shares': 0,
        'Series C Shares': 0,
        'Series D Shares': 0,
        'Series E Shares': 0,
        'Total Shares': founder_shares,
        'Founder %': 100.0,
        'Seed %': 0.0,
        'Series A %': 0.0,
        'Series B %': 0.0,
        'Series C %': 0.0,
        'Series D %': 0.0,
        'Series E %': 0.0
    })
    
    investor_shares = {
        'Founder': founder_shares,
        'Seed': 0,
        'Series A': 0,
        'Series B': 0,
        'Series C': 0,
        'Series D': 0,
        'Series E': 0
    }
    
    prev_total_shares = founder_shares
    investor_names = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D', 'Series E']
    
    for idx, row in funding_data.iterrows():
        if idx >= num_rounds:
            break
        
        pre_money = row.get('Pre-Money ($M)', 0)
        investment = row.get('Investment ($M)', 0)
        
        # For Formation (idx=0), don't process in loop - already added above
        if idx == 0:
            continue
        
        # Skip other rounds if both pre_money and investment are 0
        if pre_money <= 0 or investment <= 0:
            continue
        
        post_money = calculate_post_money(pre_money, investment)
        price_per_share = calculate_price_per_share(pre_money, prev_total_shares)
        new_shares = calculate_new_shares(investment, price_per_share)
        
        # Pro-rata Protection Model:
        # - New investor gets their shares normally
        # - BUT existing investors ALSO get pro-rata bonus in later rounds
        #
        # In Seed round: New investor (Seed) gets their shares
        # In Series A: Founder (80%) + Seed (20%) get pro-rata to maintain that %
        #             This means they collectively get a % of Series A's shares as bonus
        
        investor_idx = idx - 1  # Convert to 0-based index
        current_investor = investor_names[investor_idx] if investor_idx < len(investor_names) else f'Series {investor_idx+1}'
        
        # Step 1: Calculate bonus shares for existing investors (pro-rata protection)
        prorata_bonus = 0
        if idx > 1:  # Only applies to rounds after Seed
            # Existing investors (founder + previous) get pro-rata
            # They get: their_total_% * new_shares as BONUS
            existing_total_pct = 0
            
            # Add founder %
            if investor_shares['Founder'] > 0:
                existing_total_pct += investor_shares['Founder'] / prev_total_shares
            
            # Add all previous investors' %
            for investor in investor_names[:investor_idx]:
                if investor in investor_shares and investor_shares[investor] > 0:
                    existing_total_pct += investor_shares[investor] / prev_total_shares
            
            # Bonus shares for existing investors
            prorata_bonus = existing_total_pct * new_shares * 0.5  # 50% of new shares go to pro-rata
            
            # Distribute bonus to existing investors proportionally
            if prorata_bonus > 0:
                # Founder gets their share of the bonus
                if investor_shares['Founder'] > 0:
                    founder_pct_of_existing = investor_shares['Founder'] / (investor_shares['Founder'] + sum(investor_shares.get(inv, 0) for inv in investor_names[:investor_idx]))
                    investor_shares['Founder'] += founder_pct_of_existing * prorata_bonus
                
                # Previous investors get their share of the bonus
                for investor in investor_names[:investor_idx]:
                    if investor in investor_shares and investor_shares[investor] > 0:
                        investor_pct_of_existing = investor_shares[investor] / (investor_shares['Founder'] + sum(investor_shares.get(inv, 0) for inv in investor_names[:investor_idx]))
                        investor_shares[investor] += investor_pct_of_existing * prorata_bonus
        
        # Step 2: New investor gets remaining shares
        investor_shares[current_investor] = new_shares - prorata_bonus
        
        total_shares = sum(investor_shares.values())
        
        # Build row
        if idx == 1:
            round_name = 'Seed'
        else:
            round_name = f'Series {chr(64 + idx - 1)}'  # Series A, B, C...
        
        row_data = {
            'Round': round_name,
            'Pre-Money ($M)': round(pre_money, 2),
            'Investment ($M)': round(investment, 2),
            'Post-Money ($M)': round(post_money, 2),
            'Price/Share ($)': round(price_per_share, 4) if price_per_share > 0 else 0,
            'New Shares': int(new_shares) if new_shares > 0 else 0,
            'Founder Shares': int(investor_shares['Founder']),
            'Seed Shares': int(investor_shares.get('Seed', 0)),
            'Series A Shares': int(investor_shares.get('Series A', 0)),
            'Series B Shares': int(investor_shares.get('Series B', 0)),
            'Series C Shares': int(investor_shares.get('Series C', 0)),
            'Series D Shares': int(investor_shares.get('Series D', 0)),
            'Series E Shares': int(investor_shares.get('Series E', 0)),
            'Total Shares': int(total_shares),
            'Founder %': calculate_ownership_pct(investor_shares['Founder'], total_shares),
            'Seed %': calculate_ownership_pct(investor_shares.get('Seed', 0), total_shares),
            'Series A %': calculate_ownership_pct(investor_shares.get('Series A', 0), total_shares),
            'Series B %': calculate_ownership_pct(investor_shares.get('Series B', 0), total_shares),
            'Series C %': calculate_ownership_pct(investor_shares.get('Series C', 0), total_shares),
            'Series D %': calculate_ownership_pct(investor_shares.get('Series D', 0), total_shares),
            'Series E %': calculate_ownership_pct(investor_shares.get('Series E', 0), total_shares),
        }
        
        cap_table.append(row_data)
        prev_total_shares = total_shares
    
    return pd.DataFrame(cap_table)

# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render professional hero title header"""
    st.markdown(f"""
    <div class='hero-title'>
        <h1>CAP TABLE SIMULATOR PRO</h1>
        <p>Professional Startup Equity Analysis Dashboard</p>
        <p>Prof. V. Ravichandran | 28+ Years Finance Experience | 10+ Years Academic Excellence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

render_header()

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    col_rounds1, col_rounds2 = st.columns([2, 1])
    
    with col_rounds1:
        num_rounds = st.slider(
            "Number of Rounds",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Total funding rounds including formation"
        )
    
    with col_rounds2:
        st.metric("Total Rounds", num_rounds)
    
    # Show stage info
    st.divider()
    if num_rounds == 1:
        st.info("🏛️ **Formation Only** - No external funding")
    elif num_rounds == 2:
        st.info("🌱 **Early Stage** - Seed round")
    elif num_rounds == 3:
        st.info("📈 **Early Growth** - Seed + Series A")
    elif num_rounds == 4:
        st.info("💼 **Growth Stage** - Through Series B")
    elif num_rounds == 5:
        st.info("📊 **Expansion** - Through Series C")
    elif num_rounds <= 7:
        st.info("🚀 **Mature Company** - Series D+")
    else:
        st.info("🌟 **Late Stage** - Multiple institutional rounds")
    
    st.divider()
    
    st.write("### 👤 Founder's Shares")
    col_cap1, col_cap2 = st.columns([2, 1])
    
    with col_cap1:
        founder_capital = st.slider(
            "Initial Shares (Millions)",
            min_value=1.0,
            max_value=100.0,
            value=10.0,
            step=0.5,
            help="Founder's initial share allocation in millions"
        )
    
    # Convert to actual shares
    founder_shares = int(founder_capital * 1_000_000)
    
    with col_cap2:
        st.metric("Shares", f"{founder_shares/1_000_000:.1f}M")
    
    st.divider()
    
    st.write("**📊 About This Tool**")
    st.write("""
    - Compare equity dilution
    - Model different scenarios
    - See ownership impact
    - Analyze pro-rata protection
    """)

# Main content
st.subheader("📊 Funding Inputs & Analysis")

col_input, col_summary = st.columns([2, 1])

with col_input:
    st.write("### 💰 Enter Funding Details for Each Round")
    
    # Show helper text with round count
    st.markdown(f"""
    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
    <p style='margin: 0; font-size: 14px;'>📌 <strong>Entering {num_rounds} rounds</strong> - Formation + {num_rounds-1} funding rounds</p>
    </div>
    """, unsafe_allow_html=True)
    
    funding_data_rows = []
    
    # Header
    col_round, col_pre, col_investment = st.columns([1, 1.5, 1.5], gap="small")
    with col_round:
        st.write("**Round**")
    with col_pre:
        st.write("**Pre-Money ($M)**")
    with col_investment:
        st.write("**Investment ($M)**")
    
    st.divider()
    
    # Get round names
    round_names = ["Formation", "Seed", "Series A", "Series B", "Series C", "Series D", "Series E", "Series F", "Series G", "Series H"]
    
    # Input rows
    for i in range(num_rounds):
        col_round, col_pre, col_investment = st.columns([1, 1.5, 1.5], gap="small")
        
        round_label = round_names[i] if i < len(round_names) else f"Round {i+1}"
        
        with col_round:
            st.write(f"<div style='padding: 10px; background: linear-gradient(135deg, #003366 0%, #004d80 100%); color: white; border-radius: 5px; text-align: center;'><strong>{round_label}</strong></div>", unsafe_allow_html=True)
        
        with col_pre:
            pre_money = st.number_input(
                f"Pre-money {round_label}",
                min_value=0.0 if i == 0 else 0.5,
                max_value=100000.0,
                value=0.0 if i == 0 else float(8 * (2 ** (i-1))),
                step=1.0,
                label_visibility="collapsed",
                key=f"pre_{i}"
            )
        
        with col_investment:
            investment = st.number_input(
                f"Investment {round_label}",
                min_value=0.0 if i == 0 else 0.1,
                max_value=1000.0,
                value=0.0 if i == 0 else float(1.5 * (2 ** (i-0.5))),
                step=0.1,
                label_visibility="collapsed",
                key=f"invest_{i}"
            )
        
        funding_data_rows.append({
            'Round': i + 1,
            'Pre-Money ($M)': pre_money,
            'Investment ($M)': investment
        })
    
    funding_df = pd.DataFrame(funding_data_rows)
    
    st.divider()
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📊 Load Sample", use_container_width=True):
            st.success("✅ Sample data loaded!")
    
    with col3:
        calculate_btn = st.button("🧮 Calculate", use_container_width=True, type="primary")
    
    with col4:
        st.write("")

with col_summary:
    st.write("### 📈 Quick Summary")
    st.metric("Rounds", num_rounds)
    st.metric("Founder Shares", f"{founder_shares:,}")
    total_investment = funding_df['Investment ($M)'].sum()
    st.metric("Total Investment", f"${total_investment:.2f}M")

# ============================================================================
# CALCULATIONS & RESULTS
# ============================================================================

if calculate_btn:
    try:
        with st.spinner("🔄 Calculating cap tables..."):
            dilution_table = calculate_cap_table_dilution(funding_df, num_rounds, founder_shares)
            prorata_table = calculate_cap_table_prorata(funding_df, num_rounds, founder_shares)
            
            st.session_state.dilution_table = dilution_table
            st.session_state.prorata_table = prorata_table
            
            st.success("✅ Calculations complete!")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Display results
st.write("")
st.write("---")
st.subheader("📊 Cap Table Results")

tab_about, tab1, tab2, tab3, tab4, tab_educational = st.tabs([
    "ℹ️ About", 
    "📊 With Dilution", 
    "🔄 Pro-Rata Protected", 
    "⚖️ Comparison", 
    "📈 Insights",
    "📚 Educational"
])

# Check if results exist
has_results = hasattr(st.session_state, 'dilution_table') and st.session_state.dilution_table is not None and len(st.session_state.dilution_table) > 0

if has_results:
    dilution_table = st.session_state.dilution_table
    prorata_table = st.session_state.prorata_table
    
    # ABOUT TAB
    with tab_about:
        st.markdown(f"""
        # 📖 About Cap Table Simulator Pro
        
        ## What is a Cap Table?
        
        A **Cap Table (Capitalization Table)** is a spreadsheet that shows the ownership structure of a startup at any point in time.
        It lists all shareholders, their share counts, and their ownership percentages.
        
        ### Key Components:
        - **Founders:** Original owners who started the company
        - **Investors:** VCs, angels, and institutions who fund the company
        - **Employees:** May hold options or shares via ESOP
        - **Ownership %:** Each party's stake in the company
        
        ---
        
        ## What is Dilution?
        
        **Dilution** is the reduction in ownership percentage that occurs when a company issues new shares.
        
        ### How It Works:
        ```
        Example: Founder owns 10M shares (100%)
        
        Series A: Company issues 2.625M new shares
        
        Total shares now: 12.625M
        
        Founder's % = 10M / 12.625M = 79.25%
        Series A investor: 2.625M / 12.625M = 20.75%
        ```
        
        **Key Insight:** The founder's share count didn't change (still 10M), but their ownership % dropped from 100% to 79.25%.
        
        ---
        
        ## What are Pro-Rata Rights?
        
        **Pro-Rata Rights** give an investor the right (but not obligation) to participate in future funding rounds 
        in proportion to their current ownership stake.
        
        ### Example:
        - You own 20% after Seed round
        - Series A sells 20% new equity to Series A investors
        - With pro-rata: You can invest to buy 20% of that new 20% = 4% of company
        - Result: You maintain your 20% ownership
        
        **Without Pro-Rata:** Your ownership would drop to ~16%
        
        ---
        
        ## How This App Works
        
        ### Two Scenarios:
        
        **1. WITH DILUTION (Standard):**
        - New investors get their shares
        - All existing shareholders diluted equally
        - Simple math: each new round dilutes everyone
        
        **2. PRO-RATA PROTECTED:**
        - Early investors can exercise pro-rata rights
        - They get bonus shares to maintain ownership %
        - More realistic VC scenario
        
        ### What You Can Do:
        
        ✅ **Set Configuration:**
        - Number of funding rounds (1-10)
        - Founder's initial share count (1M-100M)
        
        ✅ **View Results:**
        - Dilution scenarios side-by-side
        - Ownership percentages across all shareholders
        - Share counts and valuations
        
        ✅ **Compare:**
        - See difference between dilution and pro-rata
        - Understand founder protection
        - Analyze shareholder impact
        
        ---
        
        ## Key Formulas (Simplified)
        
        ### Dilution Formula:
        ```
        New Ownership % = Old Ownership % × (1 - Dilution %)
        ```
        
        ### Pro-Rata Formula:
        ```
        To maintain ownership p% when new equity s% is issued:
        Investor must buy: p% × s% of new shares
        Result: Ownership stays at p%
        ```
        
        ### Founder Dilution (always same):
        ```
        Founder % = (1 - Dilution %) ^ Number of Rounds
        
        Example: 3 rounds at 20% dilution each
        Founder = (0.8)³ = 51.2%
        ```
        
        ---
        
        ## Important Insights
        
        ### 1. Founder Dilution is Inevitable
        - Whether there's pro-rata or not, founders get diluted
        - This is how companies fund growth
        - Pro-rata doesn't protect founders, it protects investors
        
        ### 2. Pro-Rata Controls WHO Gets the Equity
        - Not WHETHER dilution happens
        - Example: Seed investor gets 20% vs 12.8% after Series A
        - But founder gets diluted same amount in both cases
        
        ### 3. Each Round Tells a Story
        - Formation: 100% founder
        - Seed: Founder diluted, new investor enters
        - Series A: Both diluted, new investor enters
        - Series B+: Further dilution, more players
        
        ---
        
        ## Real-World Application
        
        ### Why This Matters:
        
        **For Founders:**
        - Understand how much control you'll lose each round
        - Plan for future fundraising impact
        - Negotiate pro-rata protections for key investors
        
        **For Investors:**
        - See how your ownership changes
        - Decide whether to exercise pro-rata
        - Understand control implications
        
        **For Employees:**
        - Know the company's cap table
        - Understand option pool impact
        - Estimate future dilution of equity
        
        ---
        
        ## About The Mountain Path
        
        **The Mountain Path - World of Finance** provides advanced financial education for:
        - MBA students
        - CFA candidates  
        - FRM professionals
        - Startup founders
        - VC professionals
        
        **Prof. V. Ravichandran**
        - 28+ Years Corporate Finance & Banking
        - 10+ Years Academic Excellence
        - Expert in VC Finance, Risk Management, Financial Modeling
        
        ---
        
        ## Next Steps
        
        1. **Configure your scenario** in the sidebar
        2. **Click Calculate** to run the analysis
        3. **View results** in the tabs
        4. **Compare scenarios** to understand implications
        5. **Learn more** in the Educational tab
        """)
    
    with tab1:
        st.subheader("📊 Cap Table with Dilution Scenario")
        st.markdown("*Founder and investors are diluted with each new round*")
        
        try:
            final_dilution_row = dilution_table.iloc[-1]
            final_dilution_founder = final_dilution_row['Founder %']
        except Exception as e:
            st.error(f"Error reading dilution table: {str(e)}")
            st.stop()
        
        st.markdown("### Ownership Breakdown (Final Round)")
        
        # Extract all percentages first (before column blocks)
        seed_pct = final_dilution_row.get("Seed %", 0)
        seriesA_pct = final_dilution_row.get("Series A %", 0)
        seriesB_pct = final_dilution_row.get("Series B %", 0)
        seriesC_pct = final_dilution_row.get("Series C %", 0)
        seriesD_pct = final_dilution_row.get("Series D %", 0)
        seriesE_pct = final_dilution_row.get("Series E %", 0)
        
        cols = st.columns(4)
        
        with cols[0]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>🏔️ Founder</h3>
                <h2 style='color: #FFD700; margin: 10px 0;'>{final_dilution_founder:.2f}%</h2>
                <p style='color: white; margin: 0;'>{int(final_dilution_row.get("Founder Shares", 0)):,} shares</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>🌱 Seed</h3>
                <h2 style='color: #FFD700; margin: 10px 0;'>{seed_pct:.2f}%</h2>
                <p style='color: white; margin: 0;'>{int(final_dilution_row.get("Seed Shares", 0)):,} shares</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>📈 Series A</h3>
                <h2 style='color: #FFD700; margin: 10px 0;'>{seriesA_pct:.2f}%</h2>
                <p style='color: white; margin: 0;'>{int(final_dilution_row.get("Series A Shares", 0)):,} shares</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[3]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ff8c00 0%, #ffa500 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>📊 Series B+</h3>
                <h2 style='color: #FFD700; margin: 10px 0;'>{seriesB_pct + seriesC_pct + seriesD_pct + seriesE_pct:.2f}%</h2>
                <p style='color: white; margin: 0;'>Combined investors</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Pie Chart Distribution")
        try:
            ownership_data = {'Founder': final_dilution_founder, 'Seed': seed_pct, 'Series A': seriesA_pct, 'Series B': seriesB_pct, 'Series C': seriesC_pct, 'Series D': seriesD_pct, 'Series E': seriesE_pct}
            ownership_data = {k: v for k, v in ownership_data.items() if v > 0}
            
            if len(ownership_data) > 0:
                fig_pie = go.Figure(data=[go.Pie(labels=list(ownership_data.keys()), values=list(ownership_data.values()), marker=dict(colors=['#003366', '#1e90ff', '#20b2aa', '#ff8c00', '#9932cc', '#ff1493', '#ffd700']), textposition='inside', textinfo='label+percent')])
                fig_pie.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig_pie, use_container_width=True, key="pie_dilution")
            else:
                st.warning("No ownership data to display")
        except Exception as e:
            st.error(f"Error creating pie chart: {str(e)}")
        
        st.markdown("### Detailed Cap Table")
        st.dataframe(dilution_table, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("🔄 Cap Table with Pro-Rata Protection")
        st.markdown("*Investors exercise pro-rata rights to maintain ownership percentage*")
        
        try:
            final_prorata_row = prorata_table.iloc[-1]
            final_prorata_founder = final_prorata_row['Founder %']
        except Exception as e:
            st.error(f"Error reading pro-rata table: {str(e)}")
            st.stop()
        
        st.markdown("### Ownership Breakdown (Final Round)")
        
        # Extract all percentages first (before column blocks)
        seed_pct_prorata = final_prorata_row.get("Seed %", 0)
        seriesA_pct_prorata = final_prorata_row.get("Series A %", 0)
        seriesB_pct_prorata = final_prorata_row.get("Series B %", 0)
        seriesC_pct_prorata = final_prorata_row.get("Series C %", 0)
        seriesD_pct_prorata = final_prorata_row.get("Series D %", 0)
        seriesE_pct_prorata = final_prorata_row.get("Series E %", 0)
        
        cols = st.columns(4)
        
        with cols[0]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>🏔️ Founder</h3>
                <h2 style='color: #FFD700; margin: 10px 0;'>{final_prorata_founder:.2f}%</h2>
                <p style='color: white; margin: 0;'>{int(final_prorata_row.get("Founder Shares", 0)):,} shares</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>🌱 Seed</h3>
                <h2 style='color: #FFD700; margin: 10px 0;'>{seed_pct_prorata:.2f}%</h2>
                <p style='color: white; margin: 0;'>{int(final_prorata_row.get("Seed Shares", 0)):,} shares</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>📈 Series A</h3>
                <h2 style='color: #FFD700; margin: 10px 0;'>{seriesA_pct_prorata:.2f}%</h2>
                <p style='color: white; margin: 0;'>{int(final_prorata_row.get("Series A Shares", 0)):,} shares</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[3]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ff8c00 0%, #ffa500 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>📊 Series B+</h3>
                <h2 style='color: #FFD700; margin: 10px 0;'>{seriesB_pct_prorata + seriesC_pct_prorata + seriesD_pct_prorata + seriesE_pct_prorata:.2f}%</h2>
                <p style='color: white; margin: 0;'>Combined investors</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Pie Chart Distribution")
        try:
            ownership_data_prorata = {'Founder': final_prorata_founder, 'Seed': seed_pct_prorata, 'Series A': seriesA_pct_prorata, 'Series B': seriesB_pct_prorata, 'Series C': seriesC_pct_prorata, 'Series D': seriesD_pct_prorata, 'Series E': seriesE_pct_prorata}
            ownership_data_prorata = {k: v for k, v in ownership_data_prorata.items() if v > 0}
            
            if len(ownership_data_prorata) > 0:
                fig_pie_prorata = go.Figure(data=[go.Pie(labels=list(ownership_data_prorata.keys()), values=list(ownership_data_prorata.values()), marker=dict(colors=['#003366', '#1e90ff', '#20b2aa', '#ff8c00', '#9932cc', '#ff1493', '#ffd700']), textposition='inside', textinfo='label+percent')])
                fig_pie_prorata.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig_pie_prorata, use_container_width=True, key="pie_prorata")
            else:
                st.warning("No ownership data to display")
        except Exception as e:
            st.error(f"Error creating pie chart: {str(e)}")
        
        st.markdown("### Detailed Cap Table")
        st.dataframe(prorata_table, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("⚖️ Side-by-Side Comparison")
        st.markdown("*Compare dilution vs pro-rata scenarios*")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                        padding: 30px; border-radius: 15px; text-align: center;'>
                <h2 style='color: #FFD700; margin: 0;'>With Dilution</h2>
                <h1 style='color: white; margin: 20px 0;'>{final_dilution_founder:.2f}%</h1>
                <p style='color: white; margin: 0;'>Founder Ownership</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%); 
                        padding: 30px; border-radius: 15px; text-align: center;'>
                <h2 style='color: #003366; margin: 0;'>Pro-Rata Protected</h2>
                <h1 style='color: #FFD700; margin: 20px 0;'>{final_prorata_founder:.2f}%</h1>
                <p style='color: white; margin: 0;'>Founder Ownership</p>
            </div>
            """, unsafe_allow_html=True)
        
        prorata_benefit = final_prorata_founder - final_dilution_founder
        benefit_color = '#28a745' if prorata_benefit > 0 else '#6c757d'
        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {benefit_color} 0%, {benefit_color} 100%); 
                        padding: 30px; border-radius: 15px; text-align: center;'>
                <h2 style='color: white; margin: 0;'>Pro-Rata Benefit</h2>
                <h1 style='color: #FFD700; margin: 20px 0;'>+{prorata_benefit:.2f}%</h1>
                <p style='color: white; margin: 0;'>Additional Ownership</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Ownership Comparison Table")
        comparison_df = pd.DataFrame({
            'Investor': ['Founder', 'Seed', 'Series A', 'Series B', 'Series C', 'Series D', 'Series E'],
            'Dilution %': [final_dilution_row.get(col, 0) for col in ['Founder %', 'Seed %', 'Series A %', 'Series B %', 'Series C %', 'Series D %', 'Series E %']],
            'Pro-Rata %': [final_prorata_row.get(col, 0) for col in ['Founder %', 'Seed %', 'Series A %', 'Series B %', 'Series C %', 'Series D %', 'Series E %']]
        })
        comparison_df = comparison_df[comparison_df['Dilution %'] > 0]
        comparison_df['Difference %'] = comparison_df['Pro-Rata %'] - comparison_df['Dilution %']
        st.dataframe(comparison_df.style.format({'Dilution %': '{:.2f}%', 'Pro-Rata %': '{:.2f}%', 'Difference %': '{:.2f}%'}).background_gradient(subset=['Difference %'], cmap='RdYlGn', vmin=-5, vmax=5), use_container_width=True)
    
    with tab4:
        st.subheader("📈 Key Insights & Analysis")
        
        insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)
        
        with insight_col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 14px;'>Final Valuation</p>
                <h3 style='color: white; margin: 10px 0;'>${final_dilution_row.get("Post-Money ($M)", 0):.1f}M</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 14px;'>Total Shares</p>
                <h3 style='color: white; margin: 10px 0;'>{int(final_dilution_row.get("Total Shares", 0)):,}</h3>
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
        st.markdown(f"📊 **Final Valuation**: Company valued at **${final_dilution_row.get('Post-Money ($M)', 0):.1f}M** after all rounds.")
        st.markdown(f"👥 **Founder vs Investors**: Founder has **{final_dilution_founder:.2f}%**, others have **{100-final_dilution_founder:.2f}%**.")
    
    # EDUCATIONAL TAB
    with tab_educational:
        st.markdown("""
        # 📚 Educational Hub: Cap Table Mathematics & Pro-Rata Rights
        
        ## Understanding the Mathematics Behind Cap Tables
        
        This section provides the mathematical foundations for understanding cap table dilution 
        and pro-rata rights. Learn the formulas, see detailed examples, and understand why pro-rata 
        rights are valuable for investors (but not founders).
        
        ---
        
        ## 1. FUNDAMENTALS: Understanding Cap Table Dilution
        
        ### What is Cap Table Dilution?
        
        **Definition:** Cap table dilution is the reduction in ownership percentage that occurs when 
        a company issues new shares in subsequent funding rounds.
        
        **The Key Mechanism:**
        - Each new funding round introduces new shares
        - These new shares become part of the company's total outstanding shares
        - Existing shareholders' percentages are mathematically reduced
        
        **Why This Matters:**
        - As a company raises multiple rounds, early investors' ownership shrinks
        - Without action, their control and voting power diminish
        - Founders face increasing dilution
        - This is why pro-rata rights exist—to allow investors to maintain ownership by participating in subsequent rounds
        
        ---
        
        ### What is a Pro-Rata Right?
        
        **Definition:** Pro-rata rights give an investor the right (but not obligation) to participate 
        in future funding rounds in proportion to their current ownership stake.
        
        **In simple terms:** If you own 20% of the company, you have the right to invest in the next 
        round to maintain that 20% ownership.
        
        **Critical word:** RIGHT not obligation. The investor chooses whether to exercise it.
        
        ---
        
        ## 2. THE CORE MATHEMATICS
        
        ### Master Formula: Pro-Rata Preservation
        
        To maintain ownership percentage **p%** in a round that sells **s%** new equity:
        
        ```
        Amount to Invest = p% × s% × Post-Money Valuation
        ```
        
        **Simplified Result:**
        ```
        Ownership Maintained = p% (if you buy p × s each round)
        ```
        
        ### Founder Dilution Formula
        
        Founders (who don't buy pro-rata) experience dilution using:
        
        ```
        Founder % after n rounds = (1 - s)^n
        ```
        
        Where:
        - s = fraction of post-money equity sold per round
        - n = number of rounds
        
        **Example: 3 rounds at 20% dilution each:**
        ```
        Founder % = (1 - 0.20)³ = (0.8)³ = 51.2%
        ```
        
        ---
        
        ## 3. DETAILED THREE-ROUND EXAMPLE
        
        ### Setup: Three Rounds at 20% Each
        
        **Initial State:**
        - Founder owns 100%
        - Company raises Seed, Series A, Series B
        - Each round sells 20% post-money equity
        
        ### Case 1: WITH DILUTION (No Follow-On Investment)
        
        **After Seed Round (20% sold):**
        ```
        Founder = 100% × (1 - 0.20) = 80.0%
        Seed Investor = 20.0% (new issue)
        ```
        
        **After Series A (20% of new post-money):**
        ```
        Founder = 80% × (1 - 0.20) = 64.0%
        Seed Investor = 20% × (1 - 0.20) = 16.0%
        Series A = 20.0% (new issue)
        ```
        
        **After Series B (20% of new post-money):**
        ```
        Founder = 64% × (1 - 0.20) = 51.2%
        Seed Investor = 16% × (1 - 0.20) = 12.8%
        Series A = 20% × (1 - 0.20) = 16.0%
        Series B = 20.0% (new issue)
        ```
        
        ### Case 2: WITHOUT DILUTION (With Pro-Rata Rights)
        
        **Key Rule:** To maintain 20% ownership when a round sells 20%, must buy:
        ```
        20% × 20% = 4% of post-money
        ```
        
        **After Seed Round:**
        ```
        Founder = 80.0%
        Seed Investor = 20.0%
        ```
        
        **After Series A (Seed invests 4% of post-money):**
        ```
        Founder = 80% × (1 - 0.20) = 64.0%
        Seed Investor = 20.0% (maintained via pro-rata)
        Series A = 16.0% (remainder of 20%)
        ```
        
        **Why does Seed stay at 20%?**
        - Seed owned 20% and needs to maintain it
        - Round sells 20% total new equity
        - Seed's pro-rata = 20% × 20% = 4% new
        - Seed now owns 20% + 4% = 24% of 120% = 20% ✓
        
        **After Series B (Seed invests another 4% of post-money):**
        ```
        Founder = 64.0% × (1 - 0.20) = 51.2%
        Seed Investor = 20.0% (maintained again)
        Series A = 16.0% × (1 - 0.20) = 12.8%
        Series B = 16.0% (remainder of 20%)
        ```
        
        ---
        
        ## 4. SIDE-BY-SIDE COMPARISON
        
        ### Ownership Percentages: With vs Without Dilution
        
        | Round | Holder | With Dilution | Without Dilution | Difference |
        |-------|--------|---------------|------------------|-----------|
        | Start | Founder | 100.0% | 100.0% | 0% |
        | Seed | Founder | 80.0% | 80.0% | 0% |
        | | Seed | 20.0% | 20.0% | 0% |
        | Series A | Founder | 64.0% | 64.0% | 0% |
        | | Seed | 16.0% | 20.0% | +4.0% |
        | | Series A | 20.0% | 16.0% | -4.0% |
        | Series B | Founder | 51.2% | 51.2% | 0% |
        | | Seed | 12.8% | 20.0% | +7.2% |
        | | Series A | 16.0% | 12.8% | -3.2% |
        | | Series B | 20.0% | 16.0% | -4.0% |
        
        ### Key Observations:
        
        ✅ **Founder ownership identical in both cases (51.2%)**
        - Pro-rata rights don't protect founders!
        
        ✅ **Seed investor protected to 20% with pro-rata rights**
        - Without pro-rata: drops to 12.8%
        - With pro-rata: maintains 20.0%
        
        ✅ **Later-round investors get smaller stakes with pro-rata**
        - Series A/B investors bear the cost of Seed's pro-rata rights
        
        ✅ **Total ownership always equals 100%**
        - Math always balances
        
        ---
        
        ## 5. CRITICAL INSIGHTS
        
        ### Does Pro-Rata Protect Founders?
        
        **Answer: NO.**
        
        Pro-rata rights protect INVESTORS, not founders.
        
        In both Case 1 (with dilution) and Case 2 (without dilution):
        - Founder ownership falls from 100% to 51.2%
        - Dilution percentage is identical: (0.8)³ = 51.2%
        - Founders bear the same burden in both scenarios
        
        **What differs:**
        - WHO gets the new equity (Seed vs later investors)
        - NOT how much dilution happens
        
        ### What Pro-Rata Controls
        
        Pro-rata rights control:
        - ✅ WHO owns the equity founders give up
        - ❌ NOT how much dilution happens
        
        **Impact:**
        - **With Pro-Rata:** Early investor stays involved & controls their stake (20%)
        - **Without Pro-Rata:** Early investor fades (12.8%), later investors grow
        - **Founder Dilution:** Same either way (51.2%)
        
        **Why it matters:** Pro-rata rights are valuable for investors, not founders.
        
        ---
        
        ## 6. PRACTICAL IMPLICATIONS
        
        ### For Different Stakeholders:
        
        **Founders:**
        - Dilution is inevitable with each round
        - Pro-rata doesn't affect founder dilution directly
        - But pro-rata investors remain strong voices (may be good or bad)
        
        **Seed Investors:**
        - Pro-rata rights maintain control and influence
        - But requires capital commitment in each subsequent round
        - Decision: "Do I want to stay involved with this company?"
        
        **Series A/B Investors:**
        - Early investors' pro-rata means smaller stakes for you
        - But also means early investors stay committed
        - May provide valuable guidance and networks
        
        **Employees:**
        - More dilution = option pool becomes less valuable
        - Pro-rata vs non-pro-rata doesn't matter for employees directly
        - What matters is total dilution and vesting schedules
        
        ---
        
        ## 7. KEY TAKEAWAYS
        
        ### The Most Important Insights:
        
        1️⃣ **Founder Dilution is Independent**
           - Happens through formula: Founder% = (1-s)^n
           - Independent of whether early investors exercise pro-rata
           
        2️⃣ **Pro-Rata is About Control, Not Protection**
           - For founders: Same dilution either way
           - For investors: Maintains control and voting power
           
        3️⃣ **Economics of Pro-Rata**
           - With Pro-Rata: Early investor maintains 20%, later investors get less
           - Without Pro-Rata: Early investor fades to 12.8%, later investors get more
           
        4️⃣ **The Real Decision**
           - "Do we want early investors as ongoing strong partners?"
           - If YES → Support pro-rata rights
           - If NO → Let them dilute with future rounds
        
        ---
        
        ## 8. FORMULAS REFERENCE
        
        ### Master Formulas:
        
        **Pro-Rata Rights Master Formula:**
        ```
        To maintain ownership p% in a round that sells s%:
        Invest = p% × s% × Post-Money Valuation
        
        Simplified:
        Ownership Maintained = p% (if you buy p×s each round)
        
        For constant ownership across n rounds:
        Ownership_n = p% (constant)
        ```
        
        **Founder (No Pro-Rata):**
        ```
        Founder_n = (1 - s)^n
        
        Where:
        s = fraction of post-money sold per round
        n = number of rounds
        ```
        
        ### Application Example: 20% Per Round
        
        **Pro-Rata Buy Amount Each Round:**
        ```
        p × s = 0.20 × 0.20 = 0.04 = 4%
        
        Investor maintains 20% if they buy 4% of post-money each round
        ```
        
        **Founder Always Experiences:**
        ```
        Founder = (0.8)³ = 51.2%
        
        Regardless of investor pro-rata choice
        ```
        
        ---
        
        ## 9. ABOUT THE MATERIAL
        
        This educational content is based on **"Pro-Rata Rights & Cap Table Dilution"** 
        from **The Mountain Path - World of Finance**.
        
        **Creator:** Prof. V. Ravichandran
        - 28+ Years Corporate Finance & Banking Experience
        - 10+ Years Academic Excellence
        - Specializing in VC Finance, Financial Modeling, and Risk Management
        
        **Purpose:** Bridging theory with practical application for:
        - MBA students
        - CFA candidates
        - FRM professionals
        - Startup founders and investors
        
        ---
        """)

else:
    # Show message when no results yet
    with tab_about:
        st.info("👈 **Configure your inputs in the sidebar and click 'Calculate' to see the analysis**")
        st.markdown("""
        ### Quick Start Guide:
        
        1. **Set Number of Rounds** (1-10)
        2. **Adjust Founder's Initial Shares** (1M-100M)
        3. **Enter funding round details** (Pre-Money Valuation & Investment)
        4. **Click Calculate button**
        5. **View results** in the tabs
        
        All tabs will populate with data once you run the analysis!
        """)
    
    with tab1:
        st.info("👈 Click Calculate to see Dilution analysis")
    
    with tab2:
        st.info("👈 Click Calculate to see Pro-Rata analysis")
    
    with tab3:
        st.info("👈 Click Calculate to see Comparison")
    
    with tab4:
        st.info("👈 Click Calculate to see Insights")
    
    with tab_educational:
        st.markdown("""
        # 📚 Educational Hub: Cap Table Mathematics & Pro-Rata Rights
        
        This educational section is always available for learning, regardless of whether you have run calculations.
        
        ## Understanding the Mathematics Behind Cap Tables
        
        This section provides the mathematical foundations for understanding cap table dilution 
        and pro-rata rights. Learn the formulas, see detailed examples, and understand why pro-rata 
        rights are valuable for investors (but not founders).
        
        ### Ready to learn?
        
        Explore the sections below to understand:
        - **Fundamentals:** What are cap tables and dilution?
        - **Mathematics:** Master formulas explained
        - **Examples:** Detailed 3-round scenario
        - **Insights:** Critical findings about pro-rata
        - **Applications:** Real-world implications
        
        Then, configure your scenario in the sidebar and click Calculate to see these concepts in action!
        """)

# Footer
st.divider()
st.markdown(f"""
<div class='footer'>
    <p><strong>{BRAND_NAME}</strong></p>
    <p>Prof. V. Ravichandran | 28+ Years Finance Experience | 10+ Years Academic Excellence</p>
    <p style='font-size: 12px; color: #999;'>Created: {datetime.now().strftime('%B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)
