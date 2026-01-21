
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
        
        # Pro-rata: existing investors (including founder) exercise rights
        prorata_allocated = 0
        
        # Founder gets pro-rata rights
        if investor_shares['Founder'] > 0:
            founder_pct = investor_shares['Founder'] / prev_total_shares
            founder_prorata = founder_pct * new_shares
            investor_shares['Founder'] += founder_prorata
            prorata_allocated += founder_prorata
        
        # Previous investors get pro-rata rights
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
    
    st.write("### 📊 Funding Rounds")
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
if hasattr(st.session_state, 'dilution_table') and st.session_state.dilution_table is not None and len(st.session_state.dilution_table) > 0:
    dilution_table = st.session_state.dilution_table
    prorata_table = st.session_state.prorata_table
    
    st.write("")
    st.write("---")
    st.subheader("📊 Cap Table Results")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 With Dilution", "🔄 Pro-Rata Protected", "⚖️ Comparison", "📈 Insights"])
    
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
        ownership_data = {'Founder': final_dilution_founder, 'Seed': seed_pct, 'Series A': seriesA_pct, 'Series B': seriesB_pct, 'Series C': seriesC_pct, 'Series D': seriesD_pct, 'Series E': seriesE_pct}
        ownership_data = {k: v for k, v in ownership_data.items() if v > 0}
        
        if len(ownership_data) > 0:
            fig_pie = go.Figure(data=[go.Pie(labels=list(ownership_data.keys()), values=list(ownership_data.values()), marker=dict(colors=['#003366', '#1e90ff', '#20b2aa', '#ff8c00', '#9932cc', '#ff1493', '#ffd700']), textposition='inside', textinfo='label+percent')])
            fig_pie.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No ownership data to display")
        
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
        ownership_data_prorata = {'Founder': final_prorata_founder, 'Seed': seed_pct_prorata, 'Series A': seriesA_pct_prorata, 'Series B': seriesB_pct_prorata, 'Series C': seriesC_pct_prorata, 'Series D': seriesD_pct_prorata, 'Series E': seriesE_pct_prorata}
        ownership_data_prorata = {k: v for k, v in ownership_data_prorata.items() if v > 0}
        
        if len(ownership_data_prorata) > 0:
            fig_pie_prorata = go.Figure(data=[go.Pie(labels=list(ownership_data_prorata.keys()), values=list(ownership_data_prorata.values()), marker=dict(colors=['#003366', '#1e90ff', '#20b2aa', '#ff8c00', '#9932cc', '#ff1493', '#ffd700']), textposition='inside', textinfo='label+percent')])
            fig_pie_prorata.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig_pie_prorata, use_container_width=True)
        else:
            st.warning("No ownership data to display")
        
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

# Footer
st.divider()
st.markdown(f"""
<div style='text-align: center; color: #999; font-size: 12px;'>
    <p>🏔️ Cap Table Simulator Pro | The Mountain Path - World of Finance</p>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking</p>
    <p>Created: {datetime.now().strftime('%B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)
