# EcoValuate Pro - ESG-Integrated DCF Valuation Model

A sophisticated Streamlit application that combines Environmental, Social, and Governance (ESG) metrics with traditional financial analysis to create an integrated DCF valuation model, demonstrating how sustainability initiatives translate into measurable shareholder value.

## 🌱 Overview

EcoValuate Pro bridges the gap between ESG performance and financial valuation by applying research-based coefficients that quantify how environmental and social improvements directly impact financial margins and, ultimately, enterprise value.

### Key Features
- **Research-Backed ESG Integration**: Uses empirically-derived coefficients linking ESG improvements to financial performance
- **Progressive Implementation Modeling**: ESG benefits are realized gradually over a 5-year projection period
- **Interactive Visualizations**: Real-time charts showing margin improvements, valuation comparisons, and value creation breakdowns
- **Professional Financial Analysis**: Complete DCF model with terminal value calculation and equity valuation

## 📊 Input Parameters

### Financial Inputs
- **Revenue**: Total company revenue ($M)
- **COGS**: Cost of Goods Sold (calculated as % of revenue after ESG adjustments)
- **Operating Expenses**: SG&A, R&D, and Other OpEx (% of revenue)
- **Capital Structure**: CapEx, Depreciation, Net Working Capital (% of revenue)
- **WACC Components**: Cost of Equity, Cost of Debt, Tax Rate, Capital Structure ratios
- **Valuation Inputs**: Net Debt, Shares Outstanding

### ESG Metrics (Current vs. Target Year 5)
- **Environmental**: GHG Emissions (MtCO2e), Water Use per Vehicle (m³)
- **Social**: Female Employee Percentage (%)
- **Governance**: Sustainable Waste Ratio (%)

## 🔬 Research-Based ESG Coefficients

Our model applies the following empirically-derived coefficients from sustainability research:

| ESG Factor | Impact | Coefficient | Description |
|------------|--------|-------------|-------------|
| **GHG Emissions** | Gross Margin | **-6.15%** per MtCO2e reduction | Resource efficiency savings from carbon reduction |
| **Water Efficiency** | Gross Margin | **-3.09%** per m³ reduction | Operational cost savings from water optimization |
| **Workforce Diversity** | EBIT Margin | **+1.43%** per % female employee increase | Productivity gains from diverse workforce |
| **Waste Management** | EBIT Margin | **-0.11%** per % sustainable ratio increase | Efficiency improvements from waste optimization |

*Note: Negative coefficients for environmental factors represent cost reductions (margin improvements) from resource efficiency gains.*

## 📈 Visualization Components

### 1. ESG-Driven Margin Analysis
**Calculation**: Compares baseline margins vs. ESG-enhanced margins over 5 years
- **Baseline Scenario**: DCF projection with no ESG improvements
- **ESG Scenario**: Progressive margin improvements using research coefficients
- **Formula**: `Adjusted Margin = Base Margin + (ESG Coefficient × Improvement × Progress Factor)`
- **Impact**: Shows how sustainability initiatives directly improve operational efficiency

### 2. Scenario Comparison Dashboard
**Calculation**: Side-by-side comparison of key valuation metrics
- **Enterprise Value**: Sum of discounted FCF + Present Value of Terminal Value
- **Equity Value**: Enterprise Value - Net Debt
- **Price per Share**: Equity Value ÷ Shares Outstanding
- **Methodology**: Identical DCF models with and without ESG adjustments
- **Impact**: Quantifies total value creation from ESG integration ($M and %)

### 3. ESG Value Creation Waterfall
**Calculation**: Individual contribution of each ESG factor to total value uplift
- **Proportional Allocation**: Based on each factor's relative coefficient impact
- **Formula**: `Factor Impact = Total Uplift × (|Coefficient × Improvement| / Total Coefficient Impact)`
- **Components**: GHG reduction, water efficiency, workforce diversity, waste management
- **Impact**: Shows which ESG initiatives drive the most financial value

### 4. Free Cash Flow Projection
**Calculation**: Traditional DCF with ESG-adjusted margins
- **FCF Formula**: EBIAT + Depreciation - CapEx - ΔNWC
- **ESG Integration**: Applied progressively over 5-year period
- **Terminal Value**: Gordon Growth Model with conservative terminal growth rate
- **Impact**: Demonstrates sustainable cash flow generation from ESG improvements

## 🎯 Business Impact & Use Cases

### Investment Decision Support
- **ROSI Framework**: Quantifies Return on Sustainability Investment
- **Value Driver Analysis**: Identifies which ESG initiatives create most value
- **Risk Assessment**: Models financial impact of ESG performance gaps

### Presentation & Reporting
- **Tesla Case Study Support**: Demonstrates how carbon credits translate to enterprise value
- **Stakeholder Communication**: Visual proof that ESG investments drive shareholder returns
- **Strategic Planning**: Data-driven ESG target setting based on financial impact

## 🛠️ Technical Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or Download the Repository**
   ```bash
   # If using git
   git clone <repository-url>
   cd esg-dcf-model
   
   # Or download and extract the files to your desired directory
   ```

2. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv esg_venv
   
   # Activate virtual environment
   # On Windows:
   esg_venv\Scripts\activate
   
   # On macOS/Linux:
   source esg_venv/bin/activate
   ```

3. **Install Required Dependencies**
   ```bash
   # Install all required packages
   pip install streamlit pandas numpy plotly
   
   # Alternative: If you have a requirements.txt file
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   # Start the Streamlit application
   streamlit run "ESG model v2.py"
   
   # The app will automatically open in your browser at:
   # http://localhost:8501
   ```

### Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualizations


## 🚀 Usage Instructions

1. **Launch Application**: Run the Streamlit command and open the provided URL
2. **Landing Page**: Click "🚀 Begin Analysis" to proceed to input form
3. **Input Financial Data**: Enter company revenue, expenses, and capital structure
4. **Set ESG Metrics**: Input current ESG performance and 5-year targets
5. **Run Model**: Click "🚀 Run Model" to generate projections
6. **Analyze Results**: Review ESG impact dashboard and detailed financial analysis

## 📊 Output Interpretation

### ESG Impact Dashboard
- **Margin Improvement**: Progressive enhancement in gross and operating margins
- **Value Creation**: Total enterprise value uplift from ESG integration
- **Factor Breakdown**: Individual contribution of each ESG improvement

### Financial Analysis
- **DCF Projection**: 5-year free cash flow forecast with ESG adjustments
- **Valuation Summary**: Enterprise value, equity value, and price per share
- **Performance Metrics**: Gross margin and operating margin by year

## 🔧 Troubleshooting

### Common Issues
- **Port Already in Use**: If localhost:8501 is busy, Streamlit will suggest an alternative port
- **Import Errors**: Ensure all dependencies are installed in the active virtual environment
- **Display Issues**: Try refreshing the browser or clearing cache

### Support
For technical issues or questions about the ESG methodology, please refer to the documentation or contact the development team.

---

**Built for**: Financial analysts, sustainability teams, and investment professionals seeking to quantify the financial impact of ESG initiatives.

**Version**: 2025.1 | **Framework**: Streamlit | **Language**: Python 