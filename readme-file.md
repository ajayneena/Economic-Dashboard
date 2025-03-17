# Global Economic Dashboard

A Streamlit-based dashboard for visualizing economic data, risk assessments, and outlooks for countries worldwide.

## Features

- Country and region selection
- Multiple economic indicators visualization
- Risk assessment scoring
- Economic outlook generation
- Interactive charts and metrics
- Simulated forecast data

## Setup Instructions for Non-Technical Users

### Step 1: Set Up GitHub Account

1. Go to [GitHub](https://github.com/) and sign up for a free account
2. Verify your email address

### Step 2: Create a New Repository

1. Click the "+" icon in the top right corner of GitHub and select "New repository"
2. Name your repository (e.g., "economic-dashboard")
3. Make it public
4. Click "Create repository"

### Step 3: Upload the Dashboard Files

1. Click "uploading an existing file" on the repository page
2. Drag and drop or select the `app.py` file (the main dashboard code)
3. Click "Commit changes"

### Step 4: Create Requirements File

1. Click "Add file" > "Create new file"
2. Name the file `requirements.txt`
3. Add the following content:

```
streamlit
pandas
numpy
requests
plotly
```

4. Click "Commit new file"

### Step 5: Set Up Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign up for a free account using your GitHub account
2. Click "New app"
3. Select your repository, branch (main), and file path (app.py)
4. Click "Deploy"

Your dashboard will now be deployed with a public URL that you can access and share!

## Customizing Your Dashboard

### Adding More Indicators

1. To add more indicators, find their codes from the [World Bank Indicators](https://data.worldbank.org/indicator) page
2. Add them to the `get_indicators()` function in the code

### Connecting Real API Data

The dashboard currently uses:
- Real World Bank API connections
- Simulated IMF data

To connect to the real IMF API:
1. Register for an API key at [IMF Data API](https://www.imf.org/en/Data)
2. Replace the `get_imf_data()` function with actual API calls

### Improving the Risk Model

The current risk model is simplified. To improve it:
1. Add more indicators to the risk calculation
2. Adjust weights based on economic research
3. Consider adding machine learning models for more precise risk assessment

## Troubleshooting

### Dashboard Not Loading
- Check that all requirements are properly listed in requirements.txt
- Verify that your app.py file contains valid Python code
- Look at the build logs in Streamlit Cloud for specific errors

### Data Not Appearing
- Verify the country codes and indicator IDs
- Check your internet connection (the app needs to access external APIs)
- Try selecting different indicators or countries

## Getting AI Assistance

If you need help modifying or extending the dashboard:

1. Ask Claude or ChatGPT for specific code changes
2. Describe the feature you want to add
3. If you get an error, share the exact error message with the AI assistant
4. For visualization changes, describe what you want to see and ask for the specific code to create it

## No-Cost Alternatives for Data Sources

- **World Bank**: Free API, no registration required
- **FRED (Federal Reserve)**: Free API, requires API key registration
- **UN Data**: Free downloadable datasets
- **OEC (Observatory of Economic Complexity)**: Free API with some limitations
- **Our World in Data**: Free CSV downloads

## Cost Management Tips

- Keep your Streamlit app on the free tier
- Cache API responses to avoid hitting rate limits
- Schedule data updates instead of real-time fetching
- Use the free tiers of all data APIs

## Next Steps

- Add user authentication if you need private dashboards
- Create comparison views between multiple countries
- Add downloadable reports in PDF format
- Create custom indices based on multiple indicators
