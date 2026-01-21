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

# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Cap Table Simulator Pro",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONSTANTS
# ============================================================================

FOUNDER_INITIAL_SHARES = 10_000_000
COLOR_SCHEME = {
    "dark_blue": "#003366",
    "light_blue": "#004d80",
    "gold": "#FFD700",
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
        
        if pre_money <= 0 or investment <= 0:
            continue
        
        post_money = calculate_post_money(pre_money, investment)
        price_per_share = calculate_price_per_share(pre_money, prev_total_shares)
        new_shares = calculate_new_shares(investment, price_per_share)
        
        # Dilution: only new investor gets shares
        current_investor = investor_names[idx] if idx < len(investor_names) else f'Series {idx+1}'
        investor_shares[current_investor] = new_shares
        
        total_shares = sum(investor_shares.values())
        
        # Build row
        row_data = {
            'Round': f'Series {chr(64 + idx)}' if idx > 0 else 'Seed',
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
        
        if pre_money <= 0 or investment <= 0:
            continue
        
        post_money = calculate_post_money(pre_money, investment)
        price_per_share = calculate_price_per_share(pre_money, prev_total_shares)
        new_shares = calculate_new_shares(investment, price_per_share)
        
        # Pro-rata: existing investors exercise rights
        prorata_allocated = 0
        for investor in investor_names[:idx]:
            if investor in investor_shares and investor_shares[investor] > 0:
                investor_pct = investor_shares[investor] / prev_total_shares
                prorata_new = investor_pct * new_shares
                investor_shares[investor] += prorata_new
                prorata_allocated += prorata_new
        
        # New investor gets remainder
        current_investor = investor_names[idx] if idx < len(investor_names) else f'Series {idx+1}'
        investor_shares[current_investor] = new_shares - prorata_allocated
        
        total_shares = sum(investor_shares.values())
        
        # Build row
        row_data = {
            'Round': f'Series {chr(64 + idx)}' if idx > 0 else 'Seed',
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
    """Render main header"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: {COLOR_SCHEME["dark_blue"]}; font-size: 48px; margin: 0;'>
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
            <p style='color: {COLOR_SCHEME["light_blue"]}; font-size: 16px; margin: 5px 0;'>
            Professional Startup Equity Analysis Dashboard
            </p>
            <p style='color: #666; font-size: 12px; margin: 5px 0;'>
            Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking | 10+ Years Academic Excellence
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

render_header()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    num_rounds = st.slider(
        "Number of Rounds",
        min_value=1,
        max_value=7,
        value=5,
        step=1
    )
    
    st.divider()
    
    founder_capital = st.number_input(
        "Founder's Initial Capital ($M)",
        min_value=0.1,
        max_value=100.0,
        value=10.0,
        step=0.5
    )
    
    st.divider()
    
    scenario_type = st.radio(
        "Scenario Type",
        options=["Dilution", "Pro-Rata Protected"]
    )
    
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
    
    # Input rows
    for i in range(num_rounds):
        col_round, col_pre, col_investment = st.columns([1, 1.5, 1.5], gap="small")
        
        with col_round:
            st.write(f"Round {i+1}")
        
        with col_pre:
            pre_money = st.number_input(
                f"Pre-money round {i+1}",
                min_value=0.5,
                max_value=10000.0,
                value=float(8 * (2 ** i)),
                step=1.0,
                label_visibility="collapsed",
                key=f"pre_{i}"
            )
        
        with col_investment:
            investment = st.number_input(
                f"Investment round {i+1}",
                min_value=0.1,
                max_value=1000.0,
                value=float(1.5 * (2 ** (i-0.5))) if i > 0 else 1.41,
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
    st.metric("Founder Shares", f"{FOUNDER_INITIAL_SHARES:,}")
    total_investment = funding_df['Investment ($M)'].sum()
    st.metric("Total Investment", f"${total_investment:.2f}M")

# ============================================================================
# CALCULATIONS & RESULTS
# ============================================================================

if calculate_btn:
    try:
        with st.spinner("🔄 Calculating cap tables..."):
            dilution_table = calculate_cap_table_dilution(funding_df, num_rounds, FOUNDER_INITIAL_SHARES)
            prorata_table = calculate_cap_table_prorata(funding_df, num_rounds, FOUNDER_INITIAL_SHARES)
            
            st.session_state.dilution_table = dilution_table
            st.session_state.prorata_table = prorata_table
            
            st.success("✅ Calculations complete!")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Display results
if hasattr(st.session_state, 'dilution_table'):
    dilution_table = st.session_state.dilution_table
    prorata_table = st.session_state.prorata_table
    
    st.write("")
    st.write("---")
    st.subheader("📊 Cap Table Results")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 With Dilution", "🔄 Pro-Rata Protected", "⚖️ Comparison", "📈 Insights"])
    
    with tab1:
        st.subheader("Dilution Scenario - No Follow-On Investment")
        st.dataframe(dilution_table, use_container_width=True, hide_index=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            founder_final = dilution_table.iloc[-1]['Founder %']
            st.metric("Final Founder %", f"{founder_final:.2f}%")
        with col2:
            seed_final = dilution_table.iloc[-1]['Seed %']
            st.metric("Final Seed %", f"{seed_final:.2f}%")
        with col3:
            total_capital = dilution_table['Investment ($M)'].sum()
            st.metric("Total Capital", f"${total_capital:.2f}M")
        with col4:
            final_valuation = dilution_table.iloc[-1]['Post-Money ($M)']
            st.metric("Final Post-Money", f"${final_valuation:.2f}M")
    
    with tab2:
        st.subheader("Pro-Rata Protected Scenario - Investors Follow-On")
        st.dataframe(prorata_table, use_container_width=True, hide_index=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            founder_final = prorata_table.iloc[-1]['Founder %']
            st.metric("Final Founder %", f"{founder_final:.2f}%")
        with col2:
            seed_final = prorata_table.iloc[-1]['Seed %']
            st.metric("Final Seed %", f"{seed_final:.2f}%")
        with col3:
            total_capital = prorata_table['Investment ($M)'].sum()
            st.metric("Total Capital", f"${total_capital:.2f}M")
        with col4:
            final_valuation = prorata_table.iloc[-1]['Post-Money ($M)']
            st.metric("Final Post-Money", f"${final_valuation:.2f}M")
    
    with tab3:
        st.subheader("Side-by-Side Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            dilution_founder = dilution_table.iloc[-1]['Founder %']
            st.metric("With Dilution", f"{dilution_founder:.2f}%")
        
        with col2:
            prorata_founder = prorata_table.iloc[-1]['Founder %']
            st.metric("Pro-Rata Protected", f"{prorata_founder:.2f}%")
        
        benefit = prorata_founder - dilution_founder
        st.metric("Pro-Rata Benefit", f"{benefit:.2f}%")
    
    with tab4:
        st.subheader("📈 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Dilution Impact**")
            founder_dilution = 100 - dilution_table.iloc[-1]['Founder %']
            st.write(f"- Founder dilution: **{founder_dilution:.2f}%**")
            st.write(f"- Final ownership: **{dilution_table.iloc[-1]['Founder %']:.2f}%**")
        
        with col2:
            st.write("**Pro-Rata Benefits**")
            benefit = dilution_table.iloc[-1]['Founder %'] - prorata_table.iloc[-1]['Founder %']
            st.write(f"- Pro-rata benefit: **{benefit:.2f}%**")
            st.write(f"- Better ownership protection with rights**")

# Footer
st.divider()
st.markdown(f"""
<div style='text-align: center; color: #999; font-size: 12px;'>
    <p>🏔️ Cap Table Simulator Pro | The Mountain Path - World of Finance</p>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking</p>
    <p>Created: {datetime.now().strftime('%B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)
