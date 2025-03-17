import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import time

# Set page configuration
st.set_page_config(
    page_title="Global Economic Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
    }
    .risk-high {
        color: #D32F2F;
        font-weight: bold;
    }
    .risk-medium {
        color: #FFA000;
        font-weight: bold;
    }
    .risk-low {
        color: #388E3C;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Cache function to improve performance
@st.cache_data(ttl=3600)
def get_countries():
    """Get list of countries from World Bank API"""
    try:
        response = requests.get("http://api.worldbank.org/v2/country?format=json&per_page=300")
        data = response.json()
        countries = []
        
        # Skip first element (metadata)
        for country in data[1]:
            # Filter out aggregates and regions
            if country['region']['value'] != "Aggregates":
                countries.append({
                    'id': country['id'],
                    'name': country['name'],
                    'region': country['region']['value']
                })
        
        return pd.DataFrame(countries)
    except Exception as e:
        st.error(f"Error fetching countries: {e}")
        # Return a simple dataframe with a few countries
        return pd.DataFrame([
            {'id': 'USA', 'name': 'United States', 'region': 'North America'},
            {'id': 'GBR', 'name': 'United Kingdom', 'region': 'Europe & Central Asia'},
            {'id': 'JPN', 'name': 'Japan', 'region': 'East Asia & Pacific'},
            {'id': 'DEU', 'name': 'Germany', 'region': 'Europe & Central Asia'},
            {'id': 'IND', 'name': 'India', 'region': 'South Asia'}
        ])

@st.cache_data(ttl=3600)
def get_indicators():
    """Return commonly used economic indicators"""
    indicators = [
        {"id": "NY.GDP.MKTP.CD", "name": "GDP (current US$)"},
        {"id": "NY.GDP.MKTP.KD.ZG", "name": "GDP growth (annual %)"},
        {"id": "FP.CPI.TOTL.ZG", "name": "Inflation, consumer prices (annual %)"}
    ]
    return pd.DataFrame(indicators)

# Generate sample data instead of using API
def get_sample_data(indicator, start_year, end_year):
    """Generate sample data for demonstration"""
    years = list(range(start_year, end_year + 1))
    
    # Different patterns for different indicators
    if "GDP" in indicator and "growth" in indicator:
        # GDP growth around 2-4%
        values = [np.random.normal(3, 1) for _ in years]
    elif "Inflation" in indicator:
        # Inflation around 2-3%
        values = [np.random.normal(2.5, 0.8) for _ in years]
    else:
        # GDP in trillions with growth
        base = 1.0 if "GDP" in indicator else 200.0
        values = [base * (1 + 0.03) ** i for i, _ in enumerate(years)]
    
    # Add some trends and make it smoother
    for i in range(1, len(values)):
        values[i] = 0.7 * values[i-1] + 0.3 * values[i]
    
    return pd.DataFrame({
        'year': years,
        'value': values
    })

def calculate_risk_score(indicators_data):
    """Calculate a simple risk score from 0-10"""
    # Just for demonstration, return a random score between 2 and 8
    return np.random.uniform(2, 8)

def risk_analysis(score):
    """Convert risk score to assessment and color"""
    if score >= 7:
        return "High Risk", "risk-high"
    elif score >= 4:
        return "Medium Risk", "risk-medium"
    else:
        return "Low Risk", "risk-low"

def generate_outlook(score):
    """Generate a simple economic outlook based on risk score"""
    if score >= 7:
        return "Economic conditions face significant headwinds. Policy intervention may be needed to stabilize growth and inflation."
    elif score >= 4:
        return "Economic conditions show mixed signals with moderate risks. Careful monitoring recommended."
    else:
        return "Economic conditions appear favorable with positive outlook for sustained growth and stability."

def run_dashboard():
    """Main dashboard function"""
    # Header
    st.markdown("<h1 class='main-header'>Global Economic Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for filters
    st.sidebar.header("Filters")
    
    # Load countries data
    countries_df = get_countries()
    
    # Region filter
    regions = ["All Regions"] + sorted(countries_df['region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Select Region", regions)
    
    # Filter countries by region
    if selected_region != "All Regions":
        filtered_countries = countries_df[countries_df['region'] == selected_region]
    else:
        filtered_countries = countries_df
    
    # Country selection
    selected_country_name = st.sidebar.selectbox(
        "Select Country",
        options=sorted(filtered_countries['name'].tolist()),
        index=0
    )
    
    # Get country code
    selected_country_data = filtered_countries[filtered_countries['name'] == selected_country_name]
    selected_country_code = selected_country_data.iloc[0]['id'] if not selected_country_data.empty else None
    
    # Date range
    start_year = st.sidebar.slider("Start Year", 2010, 2022, 2015)
    end_year = st.sidebar.slider("End Year", start_year+1, 2023, 2023)
    
    # Indicator selection
    indicators_df = get_indicators()
    selected_indicators = st.sidebar.multiselect(
        "Select Indicators",
        options=indicators_df['name'].tolist(),
        default=indicators_df['name'].tolist()[:2]  # Default to first 2 indicators
    )
    
    st.markdown("<h2 class='sub-header'>Economic Data</h2>", unsafe_allow_html=True)
    
    if not selected_country_code or not selected_indicators:
        st.warning("Please select a country and at least one indicator.")
        return
    
    # Show a loading spinner while fetching data
    with st.spinner(f"Loading data for {selected_country_name}..."):
        # Container for indicator data
        indicators_data = {}
        
        # Generate sample data for each selected indicator
        for indicator in selected_indicators:
            sample_data = get_sample_data(indicator, start_year, end_year)
            indicators_data[indicator] = sample_data
            
        # Simulate loading time
        time.sleep(0.5)
        
    # Calculate risk score
    risk_score = calculate_risk_score(indicators_data)
    risk_label, risk_class = risk_analysis(risk_score)
    
    # Layout with 3 columns
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Column 1: Key metrics
    with col1:
        st.markdown("<h3>Key Metrics</h3>", unsafe_allow_html=True)
        
        # Display latest values for selected indicators
        for indicator in selected_indicators:
            data = indicators_data[indicator]
            latest_value = data.iloc[-1]['value']
            
            if "growth" in indicator.lower() or "inflation" in indicator.lower():
                st.metric(indicator, f"{latest_value:.2f}%")
            elif "gdp" in indicator.lower():
                st.metric(indicator, f"${latest_value/1e12:.2f} Trillion")
            else:
                st.metric(indicator, f"{latest_value:.2f}")
    
    # Column 2: Risk Assessment
    with col2:
        st.markdown("<h3>Risk Assessment</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4>Overall Risk: <span class='{risk_class}'>{risk_label}</span></h4>", unsafe_allow_html=True)
        
        # Risk score display
        st.progress(risk_score / 10)
        st.write(f"Risk Score: {risk_score:.2f}/10")
    
    # Column 3: Outlook
    with col3:
        st.markdown("<h3>Economic Outlook</h3>", unsafe_allow_html=True)
        outlook = generate_outlook(risk_score)
        st.write(outlook)
    
    # Main charts section
    st.markdown("---")
    st.markdown("<h2 class='sub-header'>Economic Indicators</h2>", unsafe_allow_html=True)
    
    # Create charts for each selected indicator
    for indicator in selected_indicators:
        indicator_data = indicators_data[indicator]
        
        st.subheader(indicator)
        
        # Plot line chart
        fig = px.line(
            indicator_data, 
            x='year', 
            y='value',
            markers=True,
            title=f"{indicator} ({start_year}-{end_year})"
        )
        fig.update_layout(xaxis_title="Year", yaxis_title="Value")
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.caption("Note: This is a simplified demonstration using simulated data")
    st.caption("Last updated: " + pd.Timestamp.now().strftime("%Y-%m-%d"))

# Run the application
if __name__ == "__main__":
    run_dashboard()
