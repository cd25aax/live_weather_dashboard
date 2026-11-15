# 🌦️ Live Weather Monitoring Dashboard


## 🌐 Live Dashboard

Try the deployed application here:

[Open Live Weather Dashboard](https://live-weather-monitoring-dashboard.streamlit.app)


An interactive weather monitoring and forecasting dashboard built with **Python, Streamlit, Pandas and Plotly**.

## Project Overview

This project uses the Open-Meteo API to retrieve current model-based weather conditions and forecasts for selected UK cities.

The dashboard provides interactive weather visualisations, seven-day forecasts, weather insights and downloadable CSV datasets.

## Features

- Current temperature, relative humidity and wind speed
- Interactive 24-hour weather graphs
- Seven-day weather forecast
- Daily weather overview cards
- Weekly maximum and minimum temperature chart
- Seven-day rain probability chart
- Weekly weather insights
- Hourly and seven-day CSV downloads
- City selection and manual refresh
- Automatic data refresh every 15 minutes while the application is active
- Dark-themed interface

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly Express
- Requests
- Open-Meteo Weather API

## How to Run

1. Download or clone the project.
2. Open the project folder in a terminal.
3. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Start the dashboard:

```bash
python -m streamlit run app.py
```

5. Open `http://localhost:8501` in your browser.

## Data Source

Weather data is provided by [Open-Meteo](https://open-meteo.com/).

Current conditions and forecasts are model-based estimates rather than direct on-site observations. Actual weather may differ from predicted values.

## Project Purpose

This project demonstrates practical skills in API integration, data processing, data visualisation, exploratory weather analysis and interactive dashboard development.

## Future Improvements

- Weather alerts
- Historical weather comparison
- Location-based forecasts
- Cloud deployment