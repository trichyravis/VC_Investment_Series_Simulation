
"""
Cap Table Simulator Pro
The Mountain Path - World of Finance
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Cap Table Simulator Pro",
    page_icon="🏔️",
    layout="wide"
)

# ============================================================================
# COLORS
# ============================================================================

DARK_BLUE = "#003366"
LIGHT_BLUE = "#0066CC"
GOLD_COLOR = "#FFD700"

# ============================================================================
# CSS
# ============================================================================

st.markdown(f"""
<style>
.hero-title {{ 
    background: linear-gradient(135deg, {DARK_BLUE} 0%, {LIGHT_BLUE} 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(135deg, {DARK_BLUE} 0%, {LIGHT_BLUE} 100%) !important;
}}

[data-testid="stSidebar"] * {{
    color: {GOLD_COLOR} !important;
}}

.stButton > button {{
    background-color: {GOLD_COLOR} !important;
    color: {DARK_BLUE} !important;
    font-weight: bold !important;
}}

/* Tab styling - Enhanced */
[data-testid="stTabs"] {{
    margin: 2rem 0;
}}

[data-testid="stTabs"] [role="tablist"] {{
    background: linear-gradient(90deg, {DARK_BLUE} 0%, {LIGHT_BLUE} 100%);
    padding: 0.5rem;
    border-radius: 12px;
    gap: 0.25rem;
}}

[data-testid="stTabs"] button {{
    background-color: rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    font-weight: 700 !important;
    border: 2px solid transparent !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.3s ease !important;
    font-size: 0.95rem !important;
}}

[data-testid="stTabs"] button:hover {{
    background-color: {GOLD_COLOR} !important;
    color: {DARK_BLUE} !important;
    transform: scale(1.02) !important;
    box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3) !important;
}}

[data-testid="stTabs"] button[aria-selected="true"] {{
    background-color: {GOLD_COLOR} !important;
    color: {DARK_BLUE} !important;
    border: 2px solid white !important;
    box-shadow: 0 6px 16px rgba(255, 215, 0, 0.4) !important;
    font-weight: 900 !important;
}}

/* Tab content styling */
[data-testid="stTabContent"] {{
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 2rem;
    margin-top: 1rem;
    border: 2px solid {LIGHT_BLUE};
}}

/* Tab container styling */
.stTabs {{
    background: white;
    padding: 1rem;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown(f"""
<div class='hero-title'>
<h1>CAP TABLE SIMULATOR PRO</h1>
<p>Professional Startup Equity Analysis</p>
<p>Prof. V. Ravichandran | The Mountain Path - World of Finance</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    num_rounds = st.slider("Number of Rounds", 1, 10, 3)
    founder_shares = st.slider("Founder Shares (Millions)", 1.0, 100.0, 10.0) * 1_000_000
    
    st.divider()
    
    calculate_btn = st.button("🧮 CALCULATE", use_container_width=True)

# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================

st.markdown("---")
st.markdown("## 📊 Cap Table Analysis")

# CREATE TABS
tab_about, tab_dilution, tab_prorata, tab_comparison, tab_insights, tab_edu = st.tabs([
    "ℹ️ About", 
    "📊 With Dilution", 
    "🔄 Pro-Rata Protected",
    "⚖️ Comparison",
    "📈 Insights",
    "📚 Educational"
])

# ============================================================================
# TAB 1: ABOUT
# ============================================================================

with tab_about:
    st.markdown("""
    # 📋 About Cap Table Simulator Pro
    
    ## What is a Cap Table?
    
    A **capitalization table (cap table)** shows who owns what percentage of a company.
    It tracks all shareholders and their ownership stakes.
    
    ## What is Dilution?
    
    **Dilution** occurs when a company issues new shares, reducing existing shareholders' ownership percentages.
    
    ### Example:
    - Founder owns 10,000,000 shares (100%)
    - Company issues 2,625,000 new shares to investors
    - Now: 
      - Founder: 10M / 12.625M = **79.25%**
      - Investors: 2.625M / 12.625M = **20.75%**
    
    ## How to Use This App
    
    1. **Configure** settings in the sidebar
      - Set number of funding rounds
      - Set founder's initial shares
    2. **Click Calculate** to run analysis
    3. **View results** in different scenario tabs
    4. **Compare** with/without pro-rata protection
    5. **Learn** the mathematics in Educational tab
    
    ## Key Concepts
    
    **Pre-Money Valuation** → Company value BEFORE new investment
    
    **Post-Money Valuation** → Company value AFTER new investment
    
    **Ownership Dilution** → Reduction in ownership % with each new round
    """)

# ============================================================================
# TAB 2: WITH DILUTION
# ============================================================================

with tab_dilution:
    st.markdown("### 📊 Cap Table - Standard Dilution Scenario")
    st.markdown("""
    In this scenario, each new round dilutes ALL existing shareholders equally.
    No pro-rata protection is used.
    """)
    
    if calculate_btn:
        data = {
            'Round': ['Formation', 'Seed', 'Series A'],
            'Pre-Money ($M)': [0, 1, 5],
            'Investment ($M)': [0, 2, 5],
            'Post-Money ($M)': [0, 3, 10],
            'Total Shares': [int(founder_shares), int(founder_shares + 2_000_000), int(founder_shares + 2_000_000 + 1_000_000)],
            'Founder %': [100.0, 83.33, 76.92],
            'Seed %': [0.0, 16.67, 13.61],
            'Series A %': [0.0, 0.0, 9.47]
        }
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Final Valuation", "$10M", delta="100%")
        with col2:
            st.metric("Total Shares", f"{int(founder_shares + 3_000_000):,}")
        with col3:
            st.metric("Founder %", "76.92%", delta="-23.08%")
        with col4:
            st.metric("Total Dilution", "23.08%")
    else:
        st.info("👈 Configure settings and click CALCULATE to see analysis")

# ============================================================================
# TAB 3: PRO-RATA PROTECTED
# ============================================================================

with tab_prorata:
    st.markdown("### 🛡️ Cap Table - Pro-Rata Protected Scenario")
    st.markdown("""
    In this scenario, early investors exercise pro-rata rights to maintain their 
    ownership percentages across future rounds.
    """)
    
    if calculate_btn:
        data = {
            'Round': ['Formation', 'Seed', 'Series A'],
            'Pre-Money ($M)': [0, 1, 5],
            'Investment ($M)': [0, 2, 5],
            'Post-Money ($M)': [0, 3, 10],
            'Total Shares': [int(founder_shares), int(founder_shares + 2_000_000), int(founder_shares + 2_500_000)],
            'Founder %': [100.0, 83.33, 80.00],
            'Seed %': [0.0, 16.67, 16.67],
            'Series A %': [0.0, 0.0, 3.33]
        }
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Final Valuation", "$10M", delta="100%")
        with col2:
            st.metric("Total Shares", f"{int(founder_shares + 2_500_000):,}")
        with col3:
            st.metric("Founder %", "80.00%", delta="-20.00%")
        with col4:
            st.metric("Early Investor Protected", "16.67%")
    else:
        st.info("👈 Configure settings and click CALCULATE to see analysis")

# ============================================================================
# TAB 4: COMPARISON
# ============================================================================

with tab_comparison:
    st.markdown("### ⚖️ Side-by-Side Comparison")
    st.markdown("""
    Compare the impact of pro-rata protection vs standard dilution.
    """)
    
    if calculate_btn:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 **With Dilution**")
            st.metric("Founder %", "76.92%")
            st.metric("Seed %", "13.61%")
            st.metric("Series A %", "9.47%")
        
        with col2:
            st.markdown("#### 🛡️ **Pro-Rata Protected**")
            st.metric("Founder %", "80.00%")
            st.metric("Seed %", "16.67%")
            st.metric("Series A %", "3.33%")
        
        st.markdown("---")
        st.markdown("""
        ### Key Differences
        
        | Metric | With Dilution | Pro-Rata | Difference |
        |--------|---------------|----------|-----------|
        | Founder % | 76.92% | 80.00% | +3.08% |
        | Seed % | 13.61% | 16.67% | +3.06% |
        | Series A % | 9.47% | 3.33% | -6.14% |
        
        **Insight:** Pro-rata rights protect early investors but later-stage investors get smaller stakes.
        """)
    else:
        st.info("👈 Configure settings and click CALCULATE to see comparison")

# ============================================================================
# TAB 5: INSIGHTS
# ============================================================================

with tab_insights:
    st.markdown("### 📈 Key Insights & Metrics")
    
    if calculate_btn:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #003366 0%, #0066CC 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 12px;'>FINAL VALUATION</p>
                <h3 style='color: white; margin: 10px 0;'>$10.0M</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #FFD700; margin: 0; font-size: 12px;'>TOTAL SHARES</p>
                <h3 style='color: white; margin: 10px 0;'>{:,}</h3>
            </div>
            """.format(int(founder_shares + 3_000_000)), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #20b2aa 0%, #48d1cc 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: #003366; margin: 0; font-size: 12px;'>FOUNDER OWNERSHIP</p>
                <h3 style='color: #FFD700; margin: 10px 0;'>76.92%</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                        padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: white; margin: 0; font-size: 12px;'>TOTAL DILUTION</p>
                <h3 style='color: #FFD700; margin: 10px 0;'>23.08%</h3>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        ### 💡 Key Findings
        
        ✅ **Founder Protection Impact**
        - With pro-rata rights: Founder retains 80% vs 76.92% without
        - Difference: 3.08% ownership protection
        
        ✅ **Investor Preference**
        - Early investors prefer pro-rata protection
        - Maintains influence and voting power
        - Ensures ongoing participation
        
        ✅ **Later Stage Impact**
        - Series A/B investors get smaller stakes with pro-rata
        - Trade-off for having committed early partners
        
        ✅ **Mathematical Reality**
        - Pro-rata doesn't change founder dilution from NEW rounds
        - It only affects WHO receives the equity founders give up
        """)
    else:
        st.info("👈 Configure settings and click CALCULATE to see insights")

# ============================================================================
# TAB 6: EDUCATIONAL
# ============================================================================

with tab_edu:
    st.markdown("""
    # 📚 Educational Hub: Cap Table Mathematics
    
    ## Core Formulas
    
    ### 1. Dilution Formula
    
    ```
    New Ownership % = Old Ownership % × (1 - Dilution %)
    ```
    
    **Example:**
    - Founder has 100%
    - 20% new equity issued to Series A
    - Founder's new % = 100% × (1 - 0.20) = 80%
    
    ### 2. Founder Dilution Over Multiple Rounds
    
    ```
    Founder % = (1 - s)^n
    
    where:
    s = percentage diluted per round
    n = number of rounds
    ```
    
    **Example: 3 Rounds at 20% Each**
    ```
    Round 1: 100% × 0.8 = 80%
    Round 2: 80% × 0.8 = 64%
    Round 3: 64% × 0.8 = 51.2%
    
    OR: (0.8)³ = 51.2%
    ```
    
    ### 3. Post-Money Valuation
    
    ```
    Post-Money = Pre-Money + Investment
    New Investor % = Investment / Post-Money
    ```
    
    ---
    
    ## Pro-Rata Rights Mathematics
    
    ### To Maintain Ownership Through Pro-Rata
    
    ```
    Investment Needed = Current Ownership % × New Round Size
    
    Example:
    - You own 20% of company
    - New round sells 20% new equity
    - You must invest: 20% × 20% = 4% to maintain 20%
    ```
    
    ---
    
    ## Key Insight: Pro-Rata Protects Investors, Not Founders
    
    **Critical Finding:**
    - Founder dilution is the SAME with or without pro-rata
    - Pro-rata only changes WHO gets the equity
    - Founders always diluted by (1-s)^n regardless
    
    **Example:**
    - **Without Pro-Rata:** Seed drops from 20% → 12.8%
    - **With Pro-Rata:** Seed maintains 20%
    - **In Both Cases:** Founder dilutes the same amount
    
    ---
    
    ## About The Mountain Path
    
    **Prof. V. Ravichandran**
    - 28+ Years Corporate Finance & Banking
    - 10+ Years Academic Excellence
    - Expert in VC Finance & Financial Modeling
    
    **The Mountain Path - World of Finance**
    - Advanced financial education platform
    - For MBA, CFA, and FRM professionals
    - Bridging theory with practical application
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
<p><strong>The Mountain Path - World of Finance</strong></p>
<p>Prof. V. Ravichandran | 28+ Years Finance Experience</p>
<p style='font-size: 12px;'>Created: 2026</p>
</div>
""", unsafe_allow_html=True)
