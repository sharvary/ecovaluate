"""
ESG-Integrated DCF Valuation Model
==================================
A Streamlit application that combines Environmental, Social, and Governance (ESG) metrics 
with traditional financial analysis to create an integrated DCF valuation model.

Features:
- Landing page with video background
- Comprehensive ESG and financial input form
- ESG-adjusted DCF calculation with research-based coefficients
- Interactive visualizations and detailed valuation output

Author: Enowa, Nellie, Sharvary & Andrew
Date: 2025
"""

import streamlit as st

# =============================================================================
# PAGE CONFIGURATION & PROFESSIONAL COLOR PALETTE
# =============================================================================

st.set_page_config(
    page_title="EcoValuate Pro",
    page_icon="assets/electric-car-icon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Color Palette
COLORS = {
    'primary': '#2E86AB',      # Professional blue
    'secondary': '#A23B72',    # Burgundy accent
    'tertiary': '#F18F01',     # Orange accent
    'light': '#C5E4FD',        # Light blue
    'dark': '#0B132B',         # Dark blue
    'neutral': '#8B9DC3',      # Muted blue-gray
    'success': '#2eb82e',      # Keep green for positive metrics
    'danger': '#ff6b6b',       # Keep red for negative metrics
    'text_light': '#ffffff',
    'text_muted': 'rgba(255,255,255,0.7)'
}
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'
if 'esg_data' not in st.session_state:
    st.session_state.esg_data = {}
if 'show_dcf' not in st.session_state:
    st.session_state.show_dcf = False

# =============================================================================
# STYLING AND CSS
# =============================================================================

def load_custom_css():
    """Load custom CSS for consistent styling across all pages"""
    st.markdown("""
    <style>
        /* Main page background */
        .main {
            background-color: #f0f7f4;
        }
        
        /* Page container styling */
        .page-container {
            background: linear-gradient(120deg, #f7ffe0 0%, #e6f4d7 100%);
            padding: 3rem 2rem 2.5rem 2rem;
            border-radius: 18px;
            color: #2d3a1a;
            margin: 2rem auto;
            max-width: 700px;
            box-shadow: 0 8px 32px 0 rgba(60, 80, 60, 0.10), 0 1.5px 6px 0 rgba(60, 80, 60, 0.08);
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }
        
        /* Typography */
        .page-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.7rem;
            color: #3b5e2b;
            letter-spacing: 0.5px;
            text-align: center;
        }
        
        .page-subtitle {
            font-size: 1.18rem;
            margin-bottom: 2.2rem;
            color: #7a8f3e;
            text-align: center;
            line-height: 1.6;
            font-weight: 400;
        }
        
        .section-title {
            color: #4e6e2a;
            font-size: 1.35rem;
            margin-top: 1.7rem;
            margin-bottom: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.2px;
        }
        
        /* Professional Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #2E86AB 0%, #0B132B 100%);
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 1rem 2rem;
            border-radius: 8px;
            border: none;
            box-shadow: 0 4px 12px rgba(46, 134, 171, 0.3);
            transition: all 0.3s ease;
            width: 100%;
            max-width: 300px;
            margin: 2rem auto;
            display: block;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(46, 134, 171, 0.4);
            background: linear-gradient(135deg, #3B9BC8 0%, #1A1F3A 100%);
        }
    </style>
    """, unsafe_allow_html=True)

def load_esg_input_css():
    """Load specific CSS for the ESG inputs page with dark theme"""
    st.markdown("""
    <style>
        /* Set dark background for the app */
        .stApp {
            background: linear-gradient(120deg, #14171c 0%, #22272e 100%) !important;
            min-height: 100vh;
        }
        /* Set main page container to 75vw width for better screen utilization */
        .stApp .main .block-container,
        .main .block-container,
        div.block-container {
            background: none !important;
            box-shadow: none !important;
            border: none !important;
            padding: 2rem 0 !important;
            margin-left: auto !important;
            margin-right: auto !important;
            width: 75vw !important;
            min-width: 800px !important;
            max-width: 2800px !important;
        }
        
        /* Additional override for Streamlit's container */
        .block-container.st-emotion-cache-1y4p8pa {
            width: 75vw !important;
            max-width: 2800px !important;
        }
        
        /* Force width on all potential container classes */
        [data-testid="block-container"] {
            width: 75vw !important;
            max-width: 2800px !important;
            margin: 0 auto !important;
        }
        
        /* Override any Streamlit default container styling */
        .main > div:first-child {
            width: 75vw !important;
            max-width: 2800px !important;
            margin: 0 auto !important;
        }
        /* Form block styling - now fits within main container */
        .stForm {
            width: 100% !important;
            margin-left: auto;
            margin-right: auto;
            background: linear-gradient(120deg, rgba(10,12,18,0.92) 0%, rgba(22,24,32,0.88) 100%);
            border-radius: 20px;
            padding: 2.7rem 2.7rem 2.1rem 2.7rem !important;
            box-shadow: 0 2px 24px 0 rgba(0,0,0,0.17), 0 0 0 1.2px rgba(255,255,255,0.08) inset;
            border: 1.7px solid rgba(0,0,0,0.85);
            backdrop-filter: blur(24px) saturate(160%);
            -webkit-backdrop-filter: blur(24px) saturate(160%);
            transition: box-shadow 0.3s;
        }
        /* Add elegant side padding to sliders */
        .stSlider, .stSlider > div {
            padding-left: 1.3rem !important;
            padding-right: 1.3rem !important;
        }
        .stSlider .css-1yycg8u, .stSlider .st-cw {
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }
        /* Professional slider styling */
        .stSlider .rc-slider-handle {
            background: rgba(255,255,255,0.9) !important;
            border: 2.2px solid #2E86AB !important;
            box-shadow: 0 2px 8px 0 rgba(46, 134, 171, 0.3);
        }
        .stSlider .rc-slider-track {
            background: linear-gradient(90deg, #2E86AB 0%, #A23B72 100%) !important;
            height: 6px !important;
            border-radius: 3px !important;
        }
        .stSlider .rc-slider-rail {
            background: rgba(139, 157, 195, 0.2) !important;
            height: 6px !important;
            border-radius: 3px !important;
        }

        .esg-title {
            font-size: 2.8rem;
            font-weight: 800;
            text-align: center;
            margin-top: 5vh;
            margin-bottom: 0.5rem;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #fff;
            letter-spacing: 0.5px;
            line-height: 1.1;
        }
        .esg-sub {
            color: #fff;
            text-align: center;
            margin-bottom: 2.5rem;
            font-size: 1.25rem;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-weight: 400;
            opacity: 0.95;
        }
        .esg-col-title {
            text-align: left;
            font-weight: 700;
            color: #333;
            margin-bottom: 1.2rem;
            margin-top: 2.2rem;
            font-size: 2rem;
            font-family: 'Segoe UI', Arial, sans-serif;
            letter-spacing: 0.5px;
        }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# DCF CALCULATION FUNCTIONS
# =============================================================================

def calculate_esg_adjustments(esg_data):
    """
    Calculate ESG-based adjustments to financial margins using research coefficients.
    
    Args:
        esg_data (dict): Dictionary containing current and target ESG metrics
        
    Returns:
        tuple: (gpm_shift, ebit_shift) - Gross Profit Margin and EBIT adjustments
    """
    # Research-based ESG coefficients from empirical analysis
    ghg_coef = -6.15        # %GPM per MtCO2e reduction
    water_coef = -3.09      # %GPM per m³ reduction  
    diversity_coef = 1.43   # %EBIT per % female employee increase
    swr_coef = -0.11        # %EBIT per % sustainable waste ratio increase
    
    # Calculate deltas between targets and current values
    delta_ghg = esg_data['ghg_target'] - esg_data['ghg_0']
    delta_water = esg_data['water_target'] - esg_data['water_0']
    delta_div = esg_data['diversity_target'] - esg_data['diversity_0']
    delta_swr = esg_data['swr_target'] - esg_data['swr_0']
    
    # Calculate margin shifts based on ESG improvements
    gpm_shift = ghg_coef * delta_ghg + water_coef * delta_water
    ebit_shift = diversity_coef * delta_div + swr_coef * delta_swr
    
    return gpm_shift, ebit_shift

def calculate_dcf_projection(inputs, esg_adjustments):
    """
    Calculate the 5-year DCF projection with ESG adjustments.
    
    Args:
        inputs (dict): Financial input parameters
        esg_adjustments (tuple): ESG-based margin adjustments
        
    Returns:
        pandas.DataFrame: DCF projection with all cash flow components
    """
    gpm_shift, ebit_shift = esg_adjustments
    years = 5
    data = []
    
    # Initialize projection variables
    revenue_projected = inputs['revenue']
    nwc_last = inputs['revenue'] * inputs['nwc_pct']
    base_gross_margin = ((inputs['revenue'] - inputs['cogs_inputs'][0]) / inputs['revenue']) * 100
    
    for year in range(1, years + 1):
        # Project revenue with growth
        revenue_projected *= (1 + inputs['growth_rate'] / 100)
        
        # Apply progressive ESG adjustments (linear progression over 5 years)
        esg_progress = year / years
        gpm_adjusted = base_gross_margin + gpm_shift * esg_progress
        
        # Calculate adjusted COGS and gross profit
        cogs_projected = revenue_projected * (1 - gpm_adjusted / 100)
        gross_profit = revenue_projected - cogs_projected
        
        # Calculate operating expenses as percentage of revenue
        sga_expense = revenue_projected * (inputs['sga'] / 100)
        rd_expense = revenue_projected * (inputs['rd'] / 100)
        opex_expense = revenue_projected * (inputs['opex'] / 100)
        
        # Calculate base EBIT (before ESG adjustments)
        ebit_base = gross_profit - sga_expense - rd_expense - opex_expense
        
        # Apply EBIT improvement as basis points to revenue (proper financial approach)
        ebit_adjustment = revenue_projected * (ebit_shift * esg_progress / 100)
        ebit_projected = ebit_base + ebit_adjustment
        
        # Calculate EBIAT (Earnings Before Interest After Tax)
        ebiat = ebit_projected * (1 - inputs['tax_rate'] / 100)
        
        # Calculate cash flow components
        depreciation_projected = revenue_projected * (inputs['dep_pct'] / 100)
        capex_projected = revenue_projected * (inputs['capex_pct'] / 100)
        
        # Net Working Capital change calculation
        nwc = revenue_projected * inputs['nwc_pct']
        delta_nwc = nwc - nwc_last
        nwc_last = nwc
        
        # Free Cash Flow calculation
        fcf = ebiat + depreciation_projected - capex_projected - delta_nwc
        
        # Discounting
        discount_factor = 1 / ((1 + inputs['wacc'] / 100) ** year)
        discounted_fcf = fcf * discount_factor
        
        # Append year data
        data.append([
            f"Year {year}", revenue_projected, cogs_projected, ebit_projected, ebiat,
            depreciation_projected, capex_projected, delta_nwc, fcf, 
            discount_factor, discounted_fcf
        ])
    
    # Create DataFrame
    columns = [
        "Year", "Revenue", "COGS", "EBIT", "EBIAT", "Depreciation",
        "CapEx", "Change in NWC", "FCF", "Discount Factor", "Discounted FCF"
    ]
    
    return pd.DataFrame(data, columns=columns)

def calculate_valuation(df, inputs):
    """
    Calculate enterprise value, equity value, and price per share.
    
    Args:
        df (pandas.DataFrame): DCF projection DataFrame
        inputs (dict): Financial input parameters
        
    Returns:
        dict: Valuation metrics including TV, EV, equity value, and price per share
    """
    # Terminal Value calculation (Gordon Growth Model)
    terminal_fcf = df.iloc[-1]["FCF"]
    terminal_growth = inputs['growth_rate'] / 100  # Use same growth rate for terminal
    terminal_value = terminal_fcf * (1 + terminal_growth) / (inputs['wacc'] / 100 - terminal_growth)
    
    # Present value of terminal value
    years = len(df)
    present_value_tv = terminal_value / ((1 + inputs['wacc'] / 100) ** years)
    
    # Enterprise Value = Sum of discounted FCFs + Present value of TV
    enterprise_value = df["Discounted FCF"].sum() + present_value_tv
    
    # Equity Value = Enterprise Value - Net Debt
    equity_value = enterprise_value - inputs['net_debt']
    
    # Price per share
    price_per_share = equity_value / inputs['shares_outstanding']
    
    return {
        'terminal_value': terminal_value,
        'present_value_tv': present_value_tv,
        'enterprise_value': enterprise_value,
        'equity_value': equity_value,
        'price_per_share': price_per_share,
        'total_pv_fcf': df["Discounted FCF"].sum()
    }

# =============================================================================
# ENHANCED VISUALIZATION FUNCTIONS
# =============================================================================



def create_margin_impact_analysis(df, esg_adjustments, financial_inputs):
    """
    Create a multi-line chart comparing ESG vs Non-ESG margin trajectories over time.
    """
    gmp_shift, ebit_shift = esg_adjustments
    years = [1, 2, 3, 4, 5]  # Numeric years for better line chart
    
    # Calculate non-ESG baseline margins
    baseline_df = calculate_dcf_projection(financial_inputs, (0, 0))  # No ESG adjustments
    baseline_gross_margins = [(baseline_df.iloc[i]["Revenue"] - baseline_df.iloc[i]["COGS"]) / baseline_df.iloc[i]["Revenue"] * 100 for i in range(5)]
    baseline_operating_margins = [baseline_df.iloc[i]["EBIT"] / baseline_df.iloc[i]["Revenue"] * 100 for i in range(5)]
    
    # Extract ESG-enhanced margins from df
    esg_gross_margins = [(df.iloc[i]["Revenue"] - df.iloc[i]["COGS"]) / df.iloc[i]["Revenue"] * 100 for i in range(5)]
    esg_operating_margins = [df.iloc[i]["EBIT"] / df.iloc[i]["Revenue"] * 100 for i in range(5)]
    
    fig = go.Figure()
    
    # Non-ESG Gross Margin line (same color as ESG, consistent styling)
    fig.add_trace(go.Scatter(
        x=years,
        y=baseline_gross_margins,
        mode='lines+markers',
        name='Gross Margin (Baseline)',
        line=dict(color=COLORS['primary'], width=3, dash='dash'),
        marker=dict(size=8, color=COLORS['primary'], symbol='circle-open'),
        hovertemplate='<b>Year %{x}</b><br>Baseline Gross Margin: %{y:.1f}%<extra></extra>'
    ))
    
    # ESG Gross Margin line (primary color)
    fig.add_trace(go.Scatter(
        x=years,
        y=esg_gross_margins,
        mode='lines+markers',
        name='Gross Margin (ESG-Enhanced)',
        line=dict(color=COLORS['primary'], width=4),
        marker=dict(size=10, color=COLORS['primary'], symbol='circle'),
        text=[f'{val:.1f}%' for val in esg_gross_margins],
        textposition='top center',
        hovertemplate='<b>Year %{x}</b><br>ESG Gross Margin: %{y:.1f}%<extra></extra>'
    ))
    
    # Non-ESG Operating Margin line (same color as ESG, consistent styling)
    fig.add_trace(go.Scatter(
        x=years,
        y=baseline_operating_margins,
        mode='lines+markers',
        name='Operating Margin (Baseline)',
        line=dict(color=COLORS['secondary'], width=3, dash='dash'),
        marker=dict(size=8, color=COLORS['secondary'], symbol='square-open'),
        hovertemplate='<b>Year %{x}</b><br>Baseline Operating Margin: %{y:.1f}%<extra></extra>'
    ))
    
    # ESG Operating Margin line (secondary color)
    fig.add_trace(go.Scatter(
        x=years,
        y=esg_operating_margins,
        mode='lines+markers',
        name='Operating Margin (ESG-Enhanced)',
        line=dict(color=COLORS['secondary'], width=4),
        marker=dict(size=10, color=COLORS['secondary'], symbol='square'),
        text=[f'{val:.1f}%' for val in esg_operating_margins],
        textposition='top center',
        hovertemplate='<b>Year %{x}</b><br>ESG Operating Margin: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        # title=dict(
        #     text="ESG vs Baseline: Margin Improvement Comparison",
        #     font=dict(size=20, color='white'),
        #     x=0.5
        # ),
        xaxis=dict(
            title=dict(text="Year", font=dict(size=14, color='white')),
            tickfont=dict(size=12, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickmode='linear',
            tick0=1,
            dtick=1
        ),
        yaxis=dict(
            title=dict(text="Margin (%)", font=dict(size=14, color='white')),
            tickfont=dict(size=12, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            font=dict(color='white', size=11),
            bgcolor='rgba(0,0,0,0.3)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1,
            x=0.02,
            y=0.98
        ),
        height=500
    )
    
    return fig

def create_scenario_comparison(inputs, esg_adjustments):
    """
    Create a 2x2 subplot comparison showing individual valuation metrics with different scales.
    """
    # Calculate baseline scenario (without ESG)
    baseline_df = calculate_dcf_projection(inputs, (0, 0))  # No ESG adjustments
    baseline_valuation = calculate_valuation(baseline_df, inputs)
    
    # Calculate ESG scenario
    esg_df = calculate_dcf_projection(inputs, esg_adjustments)
    esg_valuation = calculate_valuation(esg_df, inputs)
    
    # Create 2x2 subplots with better spacing
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Enterprise Value ($M)", 
            "Equity Value ($M)", 
            "Price per Share ($)", 
            "Total PV of FCF ($M)"
        ),
        vertical_spacing=0.25,
        horizontal_spacing=0.15
    )
    
    # Data for each metric
    metrics_data = [
        ('Enterprise Value', baseline_valuation['enterprise_value'], esg_valuation['enterprise_value'], 1, 1),
        ('Equity Value', baseline_valuation['equity_value'], esg_valuation['equity_value'], 1, 2),
        ('Price per Share', baseline_valuation['price_per_share'], esg_valuation['price_per_share'], 2, 1),
        ('Total PV of FCF', baseline_valuation['total_pv_fcf'], esg_valuation['total_pv_fcf'], 2, 2)
    ]
    
    for i, (metric_name, baseline_val, esg_val, row, col) in enumerate(metrics_data):
        # Add bars for each scenario with professional colors
        fig.add_trace(
            go.Bar(
                name='Without ESG' if i == 0 else '',
                x=['Baseline', 'ESG-Enhanced'],
                y=[baseline_val, esg_val],
                marker=dict(color=[COLORS['neutral'], COLORS['primary']]),
                text=[
                    f'${baseline_val:,.2f}' if 'Price' in metric_name else f'${baseline_val:,.0f}',
                    f'${esg_val:,.2f}' if 'Price' in metric_name else f'${esg_val:,.0f}'
                ],
                textposition='outside',
                textfont=dict(size=10, color='white'),
                showlegend=False,  # Remove legend completely
                hovertemplate=f'<b>{metric_name}</b><br>%{{x}}: %{{y:$,.0f}}<extra></extra>' if 'Price' not in metric_name else f'<b>{metric_name}</b><br>%{{x}}: %{{y:$,.2f}}<extra></extra>'
            ),
            row=row, col=col
        )
        
        # Add connecting line to highlight the difference
        fig.add_trace(
            go.Scatter(
                x=['Baseline', 'ESG-Enhanced'],
                y=[baseline_val, esg_val],
                mode='lines+markers',
                line=dict(
                    color=COLORS['tertiary'],  # Professional accent color
                    width=3,
                    dash='dot'
                ),
                marker=dict(
                    color=COLORS['tertiary'],
                    size=8,
                    symbol='circle'
                ),
                showlegend=False,
                hoverinfo='skip',  # Don't show hover for the connecting line
                name=''
            ),
            row=row, col=col
        )
        
        # Calculate and add percentage increase annotation
        if baseline_val != 0:  # Avoid division by zero
            pct_increase = ((esg_val - baseline_val) / baseline_val) * 100
            
            # Position annotation in the middle of the line
            mid_x = 0.5  # Middle between the two x positions
            mid_y = (baseline_val + esg_val) / 2
            
            fig.add_annotation(
                x=mid_x,
                y=mid_y,
                text=f"+{pct_increase:.1f}%",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=COLORS['tertiary'],
                font=dict(
                    color=COLORS['tertiary'],
                    size=12,
                    family='Arial Black'
                ),
                bgcolor='rgba(0,0,0,0.7)',
                bordercolor=COLORS['tertiary'],
                borderwidth=1,
                borderpad=4,
                row=row, col=col
            )
    
    # Update layout
    fig.update_layout(
        # title=dict(
        #     text="ESG Integration Impact: Detailed Valuation Comparison",
        #     font=dict(size=18, color='white'),
        #     x=0.5,
        #     y=0.95
        # ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        margin=dict(t=100, b=60, l=60, r=60),
        showlegend=False  # Completely remove legend
    )
    
    # Update all axes with better formatting and more y-axis margin
    fig.update_xaxes(
        tickfont=dict(color='white', size=9),
        title_font=dict(color='white', size=10)
    )
    
    # Add individual y-axis ranges with proper margins for each subplot
    for i, (metric_name, baseline_val, esg_val, row, col) in enumerate(metrics_data):
        y_min = min(baseline_val, esg_val)
        y_max = max(baseline_val, esg_val)
        y_range = y_max - y_min
        margin_factor = 0.50  # 30% margin above and below
        
        fig.update_yaxes(
            range=[y_min - (y_range * margin_factor), y_max + (y_range * margin_factor)],
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            row=row, col=col
        )
    
    # Update subplot titles with better styling
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(color='white', size=12, family='Arial')
        annotation['y'] = annotation['y'] + 0.02  # Move titles up slightly
    
    return fig, baseline_valuation, esg_valuation

def create_esg_impact_waterfall(baseline_val, esg_val, esg_data):
    """
    Create a waterfall chart showing individual ESG contributions to valuation uplift.
    """
    # Calculate individual ESG impacts based on actual coefficient contributions
    total_uplift = esg_val['enterprise_value'] - baseline_val['enterprise_value']
    
    # Calculate actual improvements for each ESG metric
    ghg_improvement = esg_data['ghg_target'] - esg_data['ghg_0']  # Negative = reduction
    water_improvement = esg_data['water_target'] - esg_data['water_0']  # Negative = reduction  
    diversity_improvement = esg_data['diversity_target'] - esg_data['diversity_0']  # Positive = increase
    waste_improvement = esg_data['swr_target'] - esg_data['swr_0']  # Positive = increase
    
    # Research coefficients (from your model)
    ghg_coef = -6.15      # %GPM per MtCO2e reduction
    water_coef = -3.09    # %GPM per m³ reduction  
    diversity_coef = 1.43 # %EBIT per % female employee increase
    waste_coef = -0.11    # %EBIT per % sustainable waste ratio increase
    
    # Calculate approximate individual contributions
    # These are proportional estimates based on coefficient magnitudes
    total_coef_impact = abs(ghg_coef * ghg_improvement) + abs(water_coef * water_improvement) + abs(diversity_coef * diversity_improvement) + abs(waste_coef * waste_improvement)
    
    ghg_impact = total_uplift * (abs(ghg_coef * ghg_improvement) / total_coef_impact) if total_coef_impact > 0 else 0
    water_impact = total_uplift * (abs(water_coef * water_improvement) / total_coef_impact) if total_coef_impact > 0 else 0
    diversity_impact = total_uplift * (abs(diversity_coef * diversity_improvement) / total_coef_impact) if total_coef_impact > 0 else 0
    waste_impact = total_uplift * (abs(waste_coef * waste_improvement) / total_coef_impact) if total_coef_impact > 0 else 0
    
    categories = ['Baseline EV', 'GHG Reduction', 'Water Efficiency', 'Diversity', 'Waste Management', 'ESG-Enhanced EV']
    values = [baseline_val['enterprise_value'], ghg_impact, water_impact, diversity_impact, waste_impact, 0]
    
    fig = go.Figure(go.Waterfall(
        name="ESG Value Creation",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=categories,
        textposition="outside",
        text=[f"${val:,.0f}M" for val in [baseline_val['enterprise_value']] + [ghg_impact, water_impact, diversity_impact, waste_impact] + [esg_val['enterprise_value']]],
        y=[baseline_val['enterprise_value'], ghg_impact, water_impact, diversity_impact, waste_impact, esg_val['enterprise_value']],
        connector={"line":{"color":"rgba(255,255,255,0.3)"}},
        increasing={"marker":{"color":COLORS['success']}},
        decreasing={"marker":{"color":COLORS['danger']}},
        totals={"marker":{"color":COLORS['primary']}}
    ))
    
    fig.update_layout(
        # title=dict(
        #     text="ESG Value Creation Waterfall Analysis",
        #     font=dict(size=20, color='white'),
        #     x=0.5
        # ),
        xaxis=dict(
            tickfont=dict(size=10, color='white'),
            title_font=dict(color='white')
        ),
        yaxis=dict(
            title=dict(text="Enterprise Value ($M)", font=dict(size=14, color='white')),
            tickfont=dict(size=12, color='white'),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    return fig, {
        'ghg_impact': ghg_impact,
        'water_impact': water_impact, 
        'diversity_impact': diversity_impact,
        'waste_impact': waste_impact,
        'ghg_improvement': ghg_improvement,
        'water_improvement': water_improvement,
        'diversity_improvement': diversity_improvement,
        'waste_improvement': waste_improvement
    }

# =============================================================================
# OUTPUT DISPLAY FUNCTIONS
# =============================================================================

def display_dcf_results(df, valuation_metrics, esg_data, financial_inputs, esg_adjustments):
    """
    Display the DCF results including tables, metrics, and enhanced visualizations.
    
    Args:
        df (pandas.DataFrame): DCF projection DataFrame
        valuation_metrics (dict): Calculated valuation metrics
        esg_data (dict): ESG metrics data
        financial_inputs (dict): Financial input parameters
        esg_adjustments (tuple): ESG-based margin adjustments
    """
    # =============================================================================
    # ESG IMPACT DASHBOARD
    # =============================================================================
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(46, 134, 171, 0.15) 0%, rgba(162, 59, 114, 0.1) 100%); 
                border-radius: 15px; padding: 2rem; margin: 2rem 0; 
                border: 1px solid rgba(46, 134, 171, 0.3);">
        <h2 style="color: {COLORS['primary']}; text-align: center; margin-bottom: 1rem; font-size: 2rem;">
            🌱 ESG IMPACT DASHBOARD
        </h2>
        <p style="color: white; text-align: center; font-size: 1.1rem; opacity: 0.9;">
            Visualizing the financial impact of sustainability initiatives
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ESG-driven Margin Analysis
    st.subheader("📊 ESG-Driven Margin Improvements")
    
    # Add calculation explanation
    gmp_shift, ebit_shift = esg_adjustments
    
    st.info(f"""
    💡 **How This Works:**
    
    • **Research-Based Model:** ESG improvements affect margins through operational efficiency and cost savings
    
    • **Gross Margin Impact:** {gmp_shift:+.2f}% improvement from reduced resource costs (GHG: -6.15% per MtCO2e, Water: -3.09% per m³)
    
    • **Operating Margin Impact:** {ebit_shift:+.2f}% improvement from enhanced workforce productivity and waste efficiency
    
    • **Progressive Implementation:** ESG benefits are realized gradually over the 5-year period
    """)
    
    margin_impact_fig = create_margin_impact_analysis(df, esg_adjustments, financial_inputs)
    st.plotly_chart(margin_impact_fig, use_container_width=True)
    
    # Scenario Comparison
    st.subheader("🔄 Scenario Analysis: ESG Impact on Valuation")
    
    st.info("""
    📊 **Methodology:**
    
    We run two identical DCF models: one with ESG improvements applied, and one baseline scenario without ESG enhancements. 
    The difference shows the financial value created purely through sustainable business practices.
    """)
    
    scenario_fig, baseline_val, esg_val = create_scenario_comparison(financial_inputs, esg_adjustments)
    st.plotly_chart(scenario_fig, use_container_width=True)
    
    # ESG Value Creation Summary
    total_value_uplift = esg_val['enterprise_value'] - baseline_val['enterprise_value']
    uplift_percentage = (total_value_uplift / baseline_val['enterprise_value']) * 100
    
    # Compact metrics display using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(46, 134, 171, 0.1) 0%, rgba(162, 59, 114, 0.08) 100%); 
                    border-radius: 8px; padding: 0.8rem; margin: 0.5rem 0; 
                    border: 1px solid rgba(46, 134, 171, 0.2); text-align: center;">
            <h4 style="color: {COLORS['primary']}; margin: 0 0 0.5rem 0; font-size: 1.1rem;">💡 ESG Value Creation Impact</h4>
            <div style="display: flex; justify-content: space-around;">
                <div>
                    <span style="color: white; font-size: 0.9rem;">Total Uplift:</span>
                    <h3 style="color: {COLORS['success']}; margin: 0.2rem 0; font-size: 1.4rem;">${total_value_uplift:,.0f}M</h3>
                </div>
                <div>
                    <span style="color: white; font-size: 0.9rem;">Increase:</span>
                    <h3 style="color: {COLORS['success']}; margin: 0.2rem 0; font-size: 1.4rem;">{uplift_percentage:.1f}%</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Waterfall Chart
    st.subheader("🌊 ESG Value Creation Breakdown")
    
    waterfall_fig, breakdown_data = create_esg_impact_waterfall(baseline_val, esg_val, esg_data)
    
    # Add detailed calculation explanation
    with st.expander("🔬 **Calculation Methodology** - Click to expand"):
        st.write(f"""
        **Individual ESG Contributions are calculated using research-based coefficients:**
        
        • **GHG Reduction:** {breakdown_data['ghg_improvement']:+.2f} MtCO2e × (-6.15% GPM coefficient) = ${breakdown_data['ghg_impact']:,.0f}M value
        
        • **Water Efficiency:** {breakdown_data['water_improvement']:+.2f} m³/vehicle × (-3.09% GPM coefficient) = ${breakdown_data['water_impact']:,.0f}M value
        
        • **Workforce Diversity:** {breakdown_data['diversity_improvement']:+.2f}% female employees × (1.43% EBIT coefficient) = ${breakdown_data['diversity_impact']:,.0f}M value
        
        • **Waste Management:** {breakdown_data['waste_improvement']:+.2f}% sustainable ratio × (-0.11% EBIT coefficient) = ${breakdown_data['waste_impact']:,.0f}M value
        
        *Values are proportionally allocated based on each ESG factor's relative contribution to total margin improvements.*
        """)
    
    st.plotly_chart(waterfall_fig, use_container_width=True)
    
    # Key Insights Summary
    st.success(f"""
    🎯 **Key Takeaways for Presentation**
    
    ✅ **ESG Integration Creates Measurable Value:** ${total_value_uplift:,.0f}M ({uplift_percentage:.1f}%) enterprise value increase through sustainable practices
    
    📈 **Research-Backed Model:** Uses empirically-derived coefficients linking ESG improvements to financial performance
    
    🎯 **Supports Tesla Case Study:** Demonstrates how carbon reduction and operational efficiency translate to shareholder value, similar to Tesla's $2.76B carbon credit revenue
    
    💼 **Business Case:** The model quantifies the ROSI (Return on Sustainability Investment) framework, proving that ESG initiatives are not just costs but value drivers
    """)
    
    # =============================================================================
    # TRADITIONAL DCF RESULTS
    # =============================================================================
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%); 
                border-radius: 15px; padding: 2rem; margin: 2rem 0; 
                border: 1px solid rgba(255, 255, 255, 0.1);">
        <h2 style="color: {COLORS['text_light']}; text-align: center; margin-bottom: 1rem; font-size: 2rem;">
            📊 Detailed Financial Analysis
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Format DataFrame for display
    df_display = df.copy()
    
    # Main DCF Table
    st.subheader("📊 Projected Free Cash Flows")
    st.dataframe(
        df_display.style.format({
            col: "{:,.2f}" for col in df_display.select_dtypes(include=[np.number]).columns
        })
    )
    
    # Financial Metrics Table
    st.subheader("📋 Key Financial Metrics (by Year)")
    df_metrics = df.copy()
    df_metrics["Gross Profit"] = df_metrics["Revenue"] - df_metrics["COGS"]
    df_metrics["Gross Margin (%)"] = (df_metrics["Gross Profit"] / df_metrics["Revenue"]) * 100
    df_metrics["Operating Margin (%)"] = (df_metrics["EBIT"] / df_metrics["Revenue"]) * 100
    
    st.dataframe(
        df_metrics[["Year", "Gross Margin (%)", "Operating Margin (%)"]].style.format({
            "Gross Margin (%)": "{:.2f}",
            "Operating Margin (%)": "{:.2f}"
        })
    )
    
    # Valuation Summary
    st.subheader("💰 Final Valuation Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Terminal Value (TV):** ${valuation_metrics['terminal_value']:,.2f}M")
        st.markdown(f"**Present Value of TV:** ${valuation_metrics['present_value_tv']:,.2f}M")
        st.markdown(f"**Enterprise Value (EV):** ${valuation_metrics['enterprise_value']:,.2f}M")
    
    with col2:
        st.markdown(f"**Equity Value:** ${valuation_metrics['equity_value']:,.2f}M")
        st.markdown(f"**Price per Share:** ${valuation_metrics['price_per_share']:,.2f}")
        st.markdown(f"**Total PV of FCF:** ${valuation_metrics['total_pv_fcf']:,.2f}M")
    
    # Free Cash Flow Visualization
    st.subheader("📊 Free Cash Flow Projection")
    
    # Create interactive Plotly chart
    fig = go.Figure()
    
    # Add bar chart with consistent color gradient (lighter to darker)
    # Create blue gradient from lighter to darker
    blue_gradient = ['#C5E4FD', '#7AC3E8', '#2E86AB', '#1F5F7A', '#0B132B']
    
    fig.add_trace(go.Bar(
        x=df["Year"],
        y=df["FCF"],
        name="Free Cash Flow",
        marker=dict(
            color=blue_gradient[:len(df)]
        ),
        text=[f'${value:,.0f}M' for value in df["FCF"]],
        textposition='outside',
        textfont=dict(size=12, color='white'),
        hovertemplate='<b>%{x}</b><br>' +
                      'Free Cash Flow: $%{y:,.0f}M<br>' +
                      '<extra></extra>'
    ))
    
    # Update layout for beautiful styling
    fig.update_layout(
        xaxis=dict(
            title=dict(text="Year", font=dict(size=14, color='white')),
            tickfont=dict(size=12, color='white'),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text="Free Cash Flow ($M)", font=dict(size=14, color='white')),
            tickfont=dict(size=12, color='white'),
            showgrid=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=500,
        margin=dict(t=80, b=60, l=60, r=60)
    )
    
    # Display the interactive chart
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# NAVIGATION FUNCTION
# =============================================================================

def navigate_to(page):
    """Navigate to a specific page and trigger rerun"""
    st.session_state.current_page = page
    st.rerun()

# =============================================================================
# PAGE CONTENT
# =============================================================================

# Load base CSS
load_custom_css()

# Landing Page
if st.session_state.current_page == 'landing':
    # Global CSS for no scrolling and full screen
    st.markdown("""
    <style>
    .stApp {
        background: none !important;
        overflow: hidden !important;
        height: 100vh !important;
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: none !important;
        width: 100vw !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* Hide Streamlit elements */
    .stAppDeployButton, .stDecoration, #MainMenu, footer, header {
        display: none !important;
    }
    
    .bg-video {
        position: fixed;
        top: 0; 
        left: 0; 
        width: 100vw; 
        height: 100vh;
        object-fit: cover;
        z-index: -1;
        pointer-events: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add the background video
    st.markdown("""
    <video autoplay loop muted playsinline class="bg-video">
        <source src="https://ik.imagekit.io/9e66zllzf/1394254-uhd_4096_2160_24fps%20(1).mp4?updatedAt=1747778644604" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)
    
    # Create the landing page content using Streamlit components
    
    # Brand title
    st.markdown("""
    <h1 style="
        font-size: 4rem;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 4px 20px rgba(0,0,0,0.8), 0 2px 8px rgba(0,0,0,0.6);
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    ">EcoValuate Pro</h1>
    """, unsafe_allow_html=True)
    
    # Tagline
    st.markdown("""
    <p style="
        font-size: 1.2rem;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 300;
        color: #ffffff;
        text-shadow: 0 2px 12px rgba(0,0,0,0.7);
        margin-bottom: 2rem;
        max-width: 600px;
        line-height: 1.6;
        letter-spacing: 0.3px;
    ">The next generation ESG-integrated DCF valuation platform.<br>Transform sustainability metrics into quantifiable financial impact.</p>
    """, unsafe_allow_html=True)
    
    # Feature cards using columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 1.2rem 1rem;
            text-align: center;
            margin: 1rem 0;
        ">
            <h3 style="
                font-size: 1.1rem;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 0.6rem;
                text-shadow: 0 1px 4px rgba(0,0,0,0.5);
            ">ESG Integration</h3>
            <p style="
                font-size: 0.85rem;
                color: #ffffff;
                opacity: 0.9;
                line-height: 1.4;
                text-shadow: 0 1px 3px rgba(0,0,0,0.4);
            ">Seamlessly incorporate Environmental, Social, and Governance metrics into traditional financial models</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 1.2rem 1rem;
            text-align: center;
            margin: 1rem 0;
        ">
            <h3 style="
                font-size: 1.1rem;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 0.6rem;
                text-shadow: 0 1px 4px rgba(0,0,0,0.5);
            ">Advanced Analytics</h3>
            <p style="
                font-size: 0.85rem;
                color: #ffffff;
                opacity: 0.9;
                line-height: 1.4;
                text-shadow: 0 1px 3px rgba(0,0,0,0.4);
            ">Research-backed coefficients and sophisticated algorithms for accurate ESG-adjusted valuations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 1.2rem 1rem;
            text-align: center;
            margin: 1rem 0;
        ">
            <h3 style="
                font-size: 1.1rem;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 0.6rem;
                text-shadow: 0 1px 4px rgba(0,0,0,0.5);
            ">Real-Time Results</h3>
            <p style="
                font-size: 0.85rem;
                color: #ffffff;
                opacity: 0.9;
                line-height: 1.4;
                text-shadow: 0 1px 3px rgba(0,0,0,0.4);
            ">Interactive dashboards with instant calculations and beautiful visualizations of your projections</p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    
    # Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # Style the button
        st.markdown("""
        <style>
        div[data-testid="column"] > div > div > div > div > div > button {
            background: linear-gradient(135deg, #2E86AB 0%, #0B132B 100%) !important;
            color: white !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            padding: 1rem 2.5rem !important;
            border: none !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 25px rgba(46, 134, 171, 0.4), 0 4px 12px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.4s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            width: 100% !important;
            min-width: 250px !important;
        }
        
        div[data-testid="column"] > div > div > div > div > div > button:hover {
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: 0 12px 35px rgba(46, 134, 171, 0.6), 0 6px 20px rgba(0, 0, 0, 0.4) !important;
            background: linear-gradient(135deg, #3B9BC8 0%, #1A1F3A 100%) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Begin Analysis", key="start_analysis_btn"):
            navigate_to('esg_inputs')
    
    
    st.markdown("</div>", unsafe_allow_html=True)

# ESG Inputs and Analysis Page
elif st.session_state.current_page == 'esg_inputs':
    # Load ESG-specific CSS
    load_esg_input_css()
    
    # Page header
    st.markdown("""
        <div style="height: 5vh"></div>
        <h1 class="esg-title">EcoValuate Pro</h1>
        <div class="esg-sub">Enter all required <b>Financial</b>, <b>Operational</b>, and <b>ESG</b> metrics below.</div>
    """, unsafe_allow_html=True)

    # Main input form
    with st.form("main_input_form"):
        # Revenue Inputs
        st.markdown('<h2 class="esg-col-title">Revenue Inputs</h2>', unsafe_allow_html=True)
        revenue = st.number_input("Total Revenue ($M)", value=10000.0, step=1000.0, key="revenue")

        # Expense Inputs
        st.markdown('<h2 class="esg-col-title">Expense Inputs</h2>', unsafe_allow_html=True)
        st.markdown("<b>COGS per Year ($M)</b>", unsafe_allow_html=True)
        cogs_cols = st.columns(5)
        cogs_inputs = [
            cogs_cols[i].number_input(f"Year {i+1}", value=5000.0 + i * 100.0, min_value=0.0, key=f"cogs_{i}") 
            for i in range(5)
        ]
        
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        with exp_col1:
            sga = st.number_input("SG&A (% of Revenue)", value=6.0, key="sga")
        with exp_col2:
            rd = st.number_input("R&D Expense (% of Revenue)", value=4.0, key="rd")
        with exp_col3:
            opex = st.number_input("Other Operating Expense (% of Revenue)", value=2.0, key="opex")

        # CapEx & Depreciation
        st.markdown('<h2 class="esg-col-title">CapEx & Depreciation</h2>', unsafe_allow_html=True)
        col4, col5 = st.columns(2)
        with col4:
            dep_pct = st.slider("Depreciation (% of Revenue)", min_value=0.0, max_value=20.0, value=3.6, key="dep_pct")
        with col5:
            capex_pct = st.slider("CapEx (% of Revenue)", min_value=0.0, max_value=20.0, value=4.0, key="capex_pct")

        # Working Capital & Growth
        st.markdown('<h2 class="esg-col-title">Working Capital & Growth</h2>', unsafe_allow_html=True)
        col6, col7 = st.columns(2)
        with col6:
            nwc_pct = st.slider("NWC as % of Revenue", 0.0, 0.5, 0.10, key="nwc_pct")
        with col7:
            growth_rate = st.slider("Annual Revenue Growth (%)", 0, 20, 5, key="growth_rate")

        # WACC Inputs
        st.markdown('<h2 class="esg-col-title">WACC Inputs</h2>', unsafe_allow_html=True)
        col8, col9, col10 = st.columns(3)
        with col8:
            re = st.number_input("Cost of Equity (%)", value=10.0, key="re")
            tax_rate = st.number_input("Tax Rate (%)", value=24.0, key="tax_rate")
        with col9:
            rd_cost = st.number_input("Cost of Debt (%)", value=5.2, key="rd_cost")
            ev_pct = st.slider("Equity % of Capital", 0, 100, 75, key="ev_pct")
        with col10:
            dv_pct = st.slider("Debt % of Capital", 0, 100, 25, key="dv_pct")
            wacc = (ev_pct/100) * re + (dv_pct/100) * rd_cost * (1 - tax_rate/100)
            st.markdown(f"**Calculated WACC: {wacc:.2f}%**")

        # Equity Value Inputs
        st.markdown('<h2 class="esg-col-title">Equity Value Inputs</h2>', unsafe_allow_html=True)
        col11, col12 = st.columns(2)
        with col11:
            net_debt = st.number_input("Net Debt ($M)", value=2000.0, key="net_debt")
        with col12:
            shares_outstanding = st.number_input("Shares Outstanding (M)", value=400.0, key="shares_outstanding")

        # ESG Metrics
        st.markdown('<h2 class="esg-col-title">ESG Metrics</h2>', unsafe_allow_html=True)
        col13, col14 = st.columns(2)
        
        with col13:
            st.markdown('<b>Current ESG Metrics (Year 0)</b>', unsafe_allow_html=True)
            # Sub-columns for current metrics
            col13_1, col13_2 = st.columns(2)
            with col13_1:
                ghg_0 = st.slider("GHG Emissions (MtCO2e)", 0.0, 10.0, 3.5, key="ghg_0")
                diversity_0 = st.slider("Female Employees (%)", 0.0, 50.0, 20.0, key="diversity_0")
            with col13_2:
                water_0 = st.slider("Water Use per Vehicle (m³)", 0.0, 10.0, 3.5, key="water_0")
                swr_0 = st.slider("Sustainable Waste Ratio (%)", 50.0, 100.0, 90.0, key="swr_0")
        
        with col14:
            st.markdown('<b>Target ESG Metrics (Year 5)</b>', unsafe_allow_html=True)
            # Sub-columns for target metrics
            col14_1, col14_2 = st.columns(2)
            with col14_1:
                ghg_target = st.slider("Target GHG (MtCO2e)", 0.0, 10.0, 2.5, key="ghg_target")
                diversity_target = st.slider("Target Female %", 0.0, 50.0, 25.0, key="diversity_target")
            with col14_2:
                water_target = st.slider("Target Water Use (m³)", 0.0, 10.0, 2.5, key="water_target")
                swr_target = st.slider("Target SWR (%)", 50.0, 100.0, 95.0, key="swr_target")

        # Submit button
        submitted = st.form_submit_button("🚀 Run Model")

    # Store data in session state
    st.session_state.esg_data = {
        'ghg_0': ghg_0, 'water_0': water_0, 'diversity_0': diversity_0, 'swr_0': swr_0,
        'ghg_target': ghg_target, 'water_target': water_target,
        'diversity_target': diversity_target, 'swr_target': swr_target
    }

    # Process results when form is submitted
    if submitted:
        st.session_state.show_dcf = True

    if st.session_state.show_dcf:
        # Prepare input parameters
        financial_inputs = {
            'revenue': revenue,
            'cogs_inputs': cogs_inputs,
            'sga': sga,
            'rd': rd,
            'opex': opex,
            'dep_pct': dep_pct,
            'capex_pct': capex_pct,
            'nwc_pct': nwc_pct,
            'growth_rate': growth_rate,
            'wacc': wacc,
            'tax_rate': tax_rate,
            'net_debt': net_debt,
            'shares_outstanding': shares_outstanding
        }
        
        # Calculate ESG adjustments
        esg_adjustments = calculate_esg_adjustments(st.session_state.esg_data)
        
        # Generate DCF projection
        dcf_df = calculate_dcf_projection(financial_inputs, esg_adjustments)
        
        # Calculate valuation metrics
        valuation_results = calculate_valuation(dcf_df, financial_inputs)
        
        # Display results
        display_dcf_results(dcf_df, valuation_results, st.session_state.esg_data, financial_inputs, esg_adjustments)


