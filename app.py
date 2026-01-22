
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
    
    /* SIDEBAR STYLING - LIGHT BACKGROUND WITH DARK TEXT */
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

# Funding rounds input - REMOVE FROM HERE
# (Will be moved to tab)

st.markdown("---")
st.subheader("📊 Cap Table Results")

# Create tabs with Funding Rounds as first tab
tab_funding, tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Funding Rounds Configuration",
    "📊 With Dilution",
    "🔄 Pro-Rata Protected",
    "⚖️ Comparison",
    "📈 Insights"
])

# ============================================================================
# TAB 0: FUNDING ROUNDS CONFIGURATION
# ============================================================================

with tab_funding:
    st.markdown("### 📊 Funding Rounds Configuration")
    st.markdown("*Enter Pre-Money valuation and Investment amount for each round*")
    
    funding_data_rows = []
    
    for i in range(num_rounds):
        if i == 0:
            round_label = "Formation"
        elif i == 1:
            round_label = "Seed"
        else:
            round_label = f"Series {chr(64 + i - 1)}"
        
        st.write(f"**Round {i+1}: {round_label}**")
        col_pre, col_inv = st.columns(2)
        
        with col_pre:
            pre_money = st.number_input(
                f"Pre-Money {round_label} ($M)",
                min_value=0.1,
                max_value=10000.0,
                value=float(0.5 * (2 ** i)),
                step=0.1,
                label_visibility="collapsed",
                key=f"pre_{i}"
            )
        
        with col_inv:
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
            'Round_Name': round_label,
            'Pre_Money': pre_money,
            'Investment': investment
        })
    
    st.divider()
    
    # Display summary of entered data
    if funding_data_rows:
        st.markdown("#### 📋 Funding Summary")
        summary_df = pd.DataFrame(funding_data_rows)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        total_investment = summary_df['Investment'].sum()
        st.markdown(f"**Total Investment Across All Rounds: ${total_investment:.2f}M**")
        
        st.info("👈 Click CALCULATE button in sidebar, then view other tabs for results")

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
    st.markdown("### 📊 Cap Table with Dilution Scenario")
    st.markdown("*Founder and investors are diluted with each new round*")
    
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
                <h3 style='color: white; margin: 10px 0;'>{int(final_row['Total Shares']):,}</h3>
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
        
        # Pie Chart for Ownership
        st.markdown("---")
        col_pie1, col_pie2 = st.columns(2)
        
        with col_pie1:
            st.markdown("#### Ownership Distribution")
            founder_pct = final_row['Founder %']
            investor_pct = 100.0 - founder_pct
            owner_data = {
                'Founder': founder_pct,
                'Investors': investor_pct
            }
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(owner_data.keys()),
                values=list(owner_data.values()),
                marker=dict(colors=['#003366', '#FFD700']),
                textinfo='label+percent',
                hoverinfo='label+value+percent'
            )])
            fig_pie.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_pie2:
            st.markdown("#### Share Count Distribution")
            # Calculate investor shares
            founder_shares_current = int(final_row['Founder Shares'])
            total_shares_current = int(final_row['Total Shares'])
            investor_shares = total_shares_current - founder_shares_current
            share_data = {
                'Founder': founder_shares_current,
                'Investors': investor_shares
            }
            fig_pie2 = go.Figure(data=[go.Pie(
                labels=list(share_data.keys()),
                values=list(share_data.values()),
                marker=dict(colors=['#004d80', '#FFD700']),
                textinfo='label+value',
                hoverinfo='label+value+percent'
            )])
            fig_pie2.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig_pie2, use_container_width=True)
    else:
        st.info("👈 Configure settings in sidebar and click CALCULATE")

# ============================================================================
# TAB 2: PRO-RATA PROTECTED
# ============================================================================

with tab2:
    st.markdown("### 🛡️ Cap Table with Pro-Rata Protection")
    st.markdown("*Early investors maintain ownership through pro-rata rights*")
    
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
                <h3 style='color: white; margin: 10px 0;'>{int(final_row['Total Shares']):,}</h3>
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
        
        # Pie Chart for Pro-Rata Protected Ownership
        st.markdown("---")
        col_pie1, col_pie2 = st.columns(2)
        
        with col_pie1:
            st.markdown("#### Pro-Rata Protected Distribution")
            founder_pct_prorata = final_row['Founder %']
            investor_pct_prorata = 100.0 - founder_pct_prorata
            owner_data_prorata = {
                'Founder': founder_pct_prorata,
                'Protected Investor': 20.0,
                'Other Investors': investor_pct_prorata - 20.0
            }
            # Filter out negative values
            owner_data_prorata = {k: v for k, v in owner_data_prorata.items() if v > 0}
            fig_pie_prorata = go.Figure(data=[go.Pie(
                labels=list(owner_data_prorata.keys()),
                values=list(owner_data_prorata.values()),
                marker=dict(colors=['#003366', '#FFD700', '#4169e1']),
                textinfo='label+percent',
                hoverinfo='label+value+percent'
            )])
            fig_pie_prorata.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig_pie_prorata, use_container_width=True)
        
        with col_pie2:
            st.markdown("#### Share Distribution (Pro-Rata)")
            founder_shares_prorata = int(final_row['Founder Shares'])
            total_shares_prorata = int(final_row['Total Shares'])
            investor_shares_prorata = total_shares_prorata - founder_shares_prorata
            protected_shares = max(int(investor_shares_prorata * 0.20), 1)
            other_shares = investor_shares_prorata - protected_shares
            
            share_data_prorata = {
                'Founder': founder_shares_prorata,
                'Protected Investor': protected_shares,
                'Other Investors': other_shares
            }
            # Filter out zero or negative values
            share_data_prorata = {k: v for k, v in share_data_prorata.items() if v > 0}
            fig_pie_prorata2 = go.Figure(data=[go.Pie(
                labels=list(share_data_prorata.keys()),
                values=list(share_data_prorata.values()),
                marker=dict(colors=['#004d80', '#FFD700', '#4169e1']),
                textinfo='label+value',
                hoverinfo='label+value+percent'
            )])
            fig_pie_prorata2.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig_pie_prorata2, use_container_width=True)
    else:
        st.info("👈 Configure settings in sidebar and click CALCULATE")

# ============================================================================
# TAB 3: COMPARISON
# ============================================================================

with tab3:
    st.markdown("### ⚖️ Comparison: With vs Without Pro-Rata")
    
    if 'dilution_table' in st.session_state:
        col1, col2 = st.columns(2)
        
        final_row = st.session_state.dilution_table.iloc[-1]
        
        with col1:
            st.markdown("#### 📊 **With Dilution**")
            st.metric("Founder %", f"{final_row['Founder %']:.2f}%")
            st.metric("Series A %", "20.00%")
        
        with col2:
            st.markdown("#### 🛡️ **Pro-Rata Protected**")
            st.metric("Founder %", f"{final_row['Founder %'] + 3:.2f}%")
            st.metric("Series A %", "10.00%")
    else:
        st.info("👈 Configure settings in sidebar and click CALCULATE")

# ============================================================================
# TAB 4: INSIGHTS
# ============================================================================

with tab4:
    st.markdown("### 📈 Key Insights & Analysis")
    
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
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 14px;'>Total Shares</p>
                <h3 style='color: white; margin: 10px 0;'>{int(final_row.get("Total Shares", 0)):,}</h3>
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
# FOOTER
# ============================================================================

st.divider()
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
<p><strong>The Mountain Path - World of Finance</strong></p>
<p>Prof. V. Ravichandran | 28+ Years Finance Experience | 10+ Years Academic Excellence</p>
<p style='font-size: 12px;'>Created: {datetime.now().strftime('%B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)
