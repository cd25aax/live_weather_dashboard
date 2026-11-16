
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# ---------------- APP SETTINGS ----------------
st.set_page_config(
    page_title="Live Weather Monitoring Dashboard",
    page_icon="🌦️",
    layout="wide"
)


st.markdown("""
<style>

.weather-card {
    background: #202448;
    border-radius: 20px;
    padding: 25px;
}

/* PASTE YOUR NEW FORECAST CARD CSS HERE */

.forecast-card {
    background: linear-gradient(145deg, #202448, #151A36);
    border: 1px solid rgba(167, 139, 250, 0.20);
    border-radius: 18px;
    padding: 15px 10px;
    text-align: center;
}

.forecast-day {
    color: #C4B5FD;
    font-size: 12px;
}

.forecast-condition {
    color: #E2E8F0;
    font-size: 12px;
}

.forecast-high {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 700;
}

.forecast-low {
    color: #94A3B8;
    font-size: 12px;
}

.forecast-rain {
    color: #67E8F9;
    font-size: 12px;
}

.atmos-header {
    margin: 15px 0 25px;
}

.atmos-eyebrow {
    color: #A78BFA;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.atmos-header h1 {
    color: #F8FAFC;
    font-size: clamp(30px, 3vw, 46px);
    line-height: 1.2;
    margin: 0;
}

.atmos-header p {
    color: #94A3B8;
    margin-top: 12px;
}

.city-header {
    background: linear-gradient(120deg, #202448, #171B38);
    border: 1px solid rgba(167, 139, 250, 0.22);
    border-radius: 18px;
    padding: 18px 24px;
    margin: 22px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.city-label {
    color: #A78BFA;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.city-header h2 {
    color: #F8FAFC;
    font-size: 24px;
    margin: 8px 0 0;
}

.city-status {
    color: #86EFAC;
    background: rgba(34, 197, 94, 0.10);
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 12px;
}

/* Overall dashboard spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Main page background */
.stApp {
    background: #0B1023;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: #171B38;
    border-right: 1px solid rgba(167, 139, 250, 0.12);
}

/* Section headings */
h2, h3 {
    letter-spacing: -0.5px;
}

/* Chart panels */
div[data-testid="stPlotlyChart"] {
    background: #171B38;
    border: 1px solid rgba(167, 139, 250, 0.14);
    border-radius: 18px;
    padding: 12px;
    margin-bottom: 12px;
}

/* Sidebar select box */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    border-radius: 12px;
}

/* Subtle divider lines */
hr {
    border-color: rgba(167, 139, 250, 0.14);
}

/* -------- MOBILE RESPONSIVE STYLING -------- */

@media (max-width: 768px) {

    /* Reduce main page padding */
    .block-container {
        padding: 1rem 0.8rem 2rem;
    }

    /* Smaller dashboard title */
    .atmos-header h1 {
        font-size: 27px;
        line-height: 1.25;
    }

    /* Compact city information */
    .city-header {
        padding: 16px;
        gap: 10px;
    }

    .city-header h2 {
        font-size: 21px;
    }

    /* Smaller current weather cards */
    .weather-card {
        padding: 18px;
        min-height: 155px;
    }

    .weather-card-value {
        font-size: 26px;
    }

    /* Smaller daily forecast cards */
    .forecast-card {
        padding: 12px 8px;
        min-height: 160px;
    }

    .forecast-high {
        font-size: 21px;
    }

    /* Chart spacing */
    div[data-testid="stPlotlyChart"] {
        padding: 6px;
    }
}


</style>
""", unsafe_allow_html=True)



st.markdown("""
<div class="atmos-header">
    <div class="atmos-eyebrow">ATMOS WEATHER / OVERVIEW</div>
    <h1>Weather Intelligence Dashboard 🌦️</h1>
    <p>Current conditions, interactive forecasts and weather insights.</p>
</div>
""", unsafe_allow_html=True)


with st.expander("ℹ️ About This Dashboard", expanded=False):
    st.markdown("""
    ### 🌍 Dashboard Overview

    Welcome to the **Live Weather Monitoring Dashboard**!

    This interactive application provides weather forecasts
    and insights for selected UK cities using the Open-Meteo API.

    **Features include:**
    - 🌡️ Current temperature, humidity and wind speed
    - 📈 Interactive 24-hour weather graphs
    - 📅 Seven-day weather forecast
    - 🌧️ Rain probability analysis
    - 📊 Weekly weather insights
    - 📥 Downloadable CSV datasets
    - 🔄 Manual and automatic refresh

    **Data Source:** Open-Meteo Weather API
    """)



# ---------------- CITY SELECTION ----------------
cities = {
    "London": (51.5074, -0.1278),
    "Manchester": (53.4808, -2.2426),
    "Birmingham": (52.4862, -1.8904),
    "Liverpool": (53.4084, -2.9916),
    "Edinburgh": (55.9533, -3.1883),
    "Leeds": (53.8008, -1.5491),
    "Hatfield": (51.7634, -0.2242),
    "Luton": (51.8787, -0.4200),
    "Bristol": (51.4545, -2.5879),
}


st.sidebar.markdown("## 🌦️ ATMOS WEATHER")
st.sidebar.caption("Your personal weather intelligence dashboard")
st.sidebar.divider()

selected_city = st.sidebar.selectbox(
    "📍 Select a City",
    list(cities.keys())
)


latitude, longitude = cities[selected_city]


st.markdown(
    f"""
    <div class="city-header">
        <div>
            <span class="city-label">CURRENT LOCATION</span>
            <h2>📍 Weather in {selected_city}</h2>
        </div>
        <span class="city-status">● Forecast available</span>
    </div>
    """,
    unsafe_allow_html=True
)



# Manual refresh button

# Manual refresh button in sidebar
if st.sidebar.button("🔄 Refresh Weather Data"):
    st.rerun()


st.sidebar.caption("⏱️ Forecast refreshes every 15 minutes")
st.sidebar.caption("🌍 Data provided by Open-Meteo")

st.sidebar.divider()

st.sidebar.markdown("**📊 Dashboard Features**")
st.sidebar.caption("• Current weather conditions")
st.sidebar.caption("• Interactive hourly forecasts")
st.sidebar.caption("• Seven-day weather outlook")
st.sidebar.caption("• Weather insights and CSV exports")

st.sidebar.divider()
st.sidebar.caption("Atmos Weather · Version 2")



# ---------------- API SETTINGS ----------------
API_URL = "https://api.open-meteo.com/v1/forecast"


params = {
    "latitude": latitude,
    "longitude": longitude,

    # Current weather information
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m"
    ],

    # Hourly weather forecast
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m"
    ],

    # Seven-day weather forecast
    "daily": [
        "weather_code",
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_probability_max",
        "sunrise",
        "sunset"
    ],

    "forecast_days": 7,
    "timezone": "Europe/London"
}


# ---------------- COLOUR FUNCTIONS ----------------

# Temperature colour function
def temperature_color(value):
    if value < 5:
        return "#3685E8"  # Very Cold
    if value < 15:
        return "#22B8D0"  # Cold
    if value < 25:
        return "#2BAB66"  # Mild
    if value < 30:
        return "#F2A42A"  # Warm
    return "#E4544D"      # Hot


# Humidity colour function
def humidity_color(value):
    if value < 30:
        return "#E9A23B"  # Very Dry
    if value < 40:
        return "#E9CE65"  # Dry
    if value <= 60:
        return "#2BAB66"  # Moderate
    if value <= 80:
        return "#22B8D0"  # Humid
    return "#3685E8"      # Very Humid


# Wind speed colour function
def wind_color(value):
    if value < 10:
        return "#2BAB66"  # Calm / Light
    if value < 20:
        return "#22B8D0"  # Breezy
    if value < 40:
        return "#F2A42A"  # Windy
    if value < 60:
        return "#E67E22"  # Strong
    return "#E4544D"      # Very Strong


# ---------------- GRAPH FUNCTION ----------------
def make_chart(
    df,
    column,
    title,
    unit,
    color_function,
    decimals=1
):
    # Assign colours based on values
    point_colors = df[column].apply(
        color_function
    ).tolist()

    # Create the line graph
    fig = px.line(
        df,
        x="Time",
        y=column,
        title=title
    )

    # Display values every 2 hours
    labels = [
        f"{value:.{decimals}f}{unit}"
        if index % 2 == 0 else ""
        for index, value in enumerate(df[column])
    ]

    fig.update_traces(
        mode="lines+markers+text",

        line=dict(
            color="#94A3B8",
            width=2
        ),

        marker=dict(
            size=9,
            color=point_colors
        ),

        text=labels,
        textposition="top center",
        textfont=dict(size=10),

        hovertemplate=(
            "Time: %{x|%d %b, %H:%M}"
            f"<br>{column}: %{{y:.1f}}{unit}"
            "<extra></extra>"
        )
    )

    
    fig.update_layout(
        height=450,
        paper_bgcolor="#171B38",
        plot_bgcolor="#171B38",
        font=dict(
            color="#E2E8F0",
            family="Arial"
        ),
        title=dict(
            font=dict(size=18, color="#F8FAFC")
        ),
        xaxis=dict(
            title="Time (UK local time)",
            showgrid=False,
            tickfont=dict(color="#A5B4CF")
        ),
        yaxis=dict(
            title=f"{column} ({unit})",
            gridcolor="rgba(148, 163, 184, 0.12)",
            zeroline=False,
            tickfont=dict(color="#A5B4CF")
        ),
        hovermode="closest",
        margin=dict(l=45, r=30, t=65, b=45)
    )


    fig.update_xaxes(
        tickformat="%H:%M",
        dtick=3 * 60 * 60 * 1000
    )

    return fig


# ---------------- AUTOMATIC REFRESH ----------------
# Automatically refresh every 15 minutes
# while the Streamlit session is active.

@st.fragment(run_every="15m")
def show_weather_dashboard():

    try:
        # Fetch weather information
        response = requests.get(
            API_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        # ---------------- LAST UPDATED ----------------
        fetched_at = datetime.now(
            ZoneInfo("Europe/London")
        )

        st.caption(
            f"Last fetched: "
            f"{fetched_at:%d %B %Y, %H:%M:%S %Z}"
        )

        st.caption(
            f"Selected location: {selected_city} "
            f"({latitude}, {longitude})"
        )

        # ---------------- CURRENT WEATHER ----------------
        current = data["current"]

        st.caption(
            f"Weather data time: {current['time']} "
            "(UK local time)"
        )

       
        # -------- MODERN CURRENT WEATHER CARDS --------
        st.subheader("🌤️ Current Weather")

        
        col1, col2, col3 = st.columns(
            3,
            gap="medium",
            border=False
        )


        with col1:
            st.markdown(
                f"""
                <div class="weather-card">
                    <div class="weather-card-icon">🌡️</div>
                    <div class="weather-card-label">Temperature</div>
                    <div class="weather-card-value">
                        {current['temperature_2m']}°C
                    </div>
                    <div class="weather-card-caption">
                        Current temperature
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="weather-card">
                    <div class="weather-card-icon">💧</div>
                    <div class="weather-card-label">Humidity</div>
                    <div class="weather-card-value">
                        {current['relative_humidity_2m']}%
                    </div>
                    <div class="weather-card-caption">
                        Relative humidity
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="weather-card">
                    <div class="weather-card-icon">💨</div>
                    <div class="weather-card-label">Wind Speed</div>
                    <div class="weather-card-value">
                        {current['wind_speed_10m']} km/h
                    </div>
                    <div class="weather-card-caption">
                        Current wind speed
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # ---------------- HOURLY DATA ----------------
        hourly = data["hourly"]

        # Convert API data into a Pandas DataFrame
        df = pd.DataFrame({
            "Time": pd.to_datetime(hourly["time"]),
            "Temperature": hourly["temperature_2m"],
            "Humidity": hourly["relative_humidity_2m"],
            "Wind Speed": hourly["wind_speed_10m"]
        })

        # Select the next 24 hours
        now = pd.Timestamp.now(
            tz="Europe/London"
        ).tz_localize(None)

        df = df[
            df["Time"] >= now.floor("h")
        ].head(24).copy()

        if df.empty:
            st.warning(
                "No upcoming hourly forecast data was returned."
            )
            return

        st.caption(
            f"Forecast period: "
            f"{df['Time'].min():%d %b %Y %H:%M} "
            f"to {df['Time'].max():%d %b %Y %H:%M} "
            "(UK local time)"
        )

        # ---------------- TEMPERATURE GRAPH ----------------
        st.subheader(
            "🌡️ Next 24 Hours Temperature Forecast"
        )

        fig_temp = make_chart(
            df,
            "Temperature",
            "Hourly Temperature Changes",
            "°C",
            temperature_color
        )

      

        st.markdown("""
        **🌡️ Temperature Colour Guide**

        🔵 Very Cold: Below 5°C

        🩵 Cold: 5–14.9°C

        🟢 Mild: 15–24.9°C

        🟠 Warm: 25–29.9°C

        🔴 Hot: 30°C and above
        """)

        # ---------------- HUMIDITY GRAPH ----------------
        st.subheader(
            "💧 Next 24 Hours Humidity Forecast"
        )

        fig_humidity = make_chart(
            df,
            "Humidity",
            "Hourly Humidity Changes",
            "%",
            humidity_color,
            decimals=0
        )

        # Zoom into humidity range
        lower = max(
            0,
            float(df["Humidity"].min()) - 5
        )

        upper = min(
            100,
            float(df["Humidity"].max()) + 5
        )

        if upper <= lower:
            lower, upper = 0, 100

        fig_humidity.update_yaxes(
            range=[lower, upper]
        )

        

        st.markdown("""
        **💧 Humidity Colour Guide**

        🟠 Very Dry: Below 30%

        🟡 Dry: 30–39%

        🟢 Moderate: 40–60%

        🔵 Humid: Above 60–80%

        🔷 Very Humid: Above 80%
        """)

        st.caption(
            "Humidity graph is zoomed to the forecast "
            "range; its vertical axis may not start at zero."
        )

        # ---------------- WIND SPEED GRAPH ----------------
        st.subheader(
            "💨 Next 24 Hours Wind Speed Forecast"
        )

        fig_wind = make_chart(
            df,
            "Wind Speed",
            "Hourly Wind Speed Changes",
            " km/h",
            wind_color
        )

        # -------- WEATHER GRAPH TABS --------
        st.subheader("📈 Interactive Weather Forecast")

        
        tab1, tab2, tab3 = st.tabs([
            "🌡️ Temperature",
            "💧 Humidity",
            "💨 Wind Speed"
        ])

        with tab1:
            st.plotly_chart(fig_temp, width="stretch")

            st.markdown("""
            **🌡️ Temperature Colour Guide**

            🔵 Very Cold: Below 5°C

            🩵 Cold: 5–14.9°C

            🟢 Mild: 15–24.9°C

            🟠 Warm: 25–29.9°C

            🔴 Hot: 30°C and above
            """)

        with tab2:
            st.plotly_chart(fig_humidity, width="stretch")

            st.markdown("""
            **💧 Humidity Colour Guide**

            🟠 Very Dry: Below 30%

            🟡 Dry: 30–39%

            🟢 Moderate: 40–60%

            🔵 Humid: Above 60–80%

            🔷 Very Humid: Above 80%
            """)

            st.caption(
                "Humidity graph is zoomed to the forecast "
                "range; its vertical axis may not start at zero."
            )

        with tab3:
            st.plotly_chart(fig_wind, width="stretch")

            st.markdown("""
            **💨 Wind Speed Colour Guide**

            🟢 Calm / Light: Below 10 km/h

            🔵 Breezy: 10–19.9 km/h

            🟡 Windy: 20–39.9 km/h

            🟠 Strong: 40–59.9 km/h

            🔴 Very Strong: 60 km/h and above
            """)

            st.caption(
                "Colour ranges are visual categories, "
                "not official weather warning thresholds."
            )



       

        st.markdown("""
        **💨 Wind Speed Colour Guide**

        🟢 Calm / Light: Below 10 km/h

        🔵 Breezy: 10–19.9 km/h

        🟡 Windy: 20–39.9 km/h

        🟠 Strong: 40–59.9 km/h

        🔴 Very Strong: 60 km/h and above
        """)

        st.caption(
            "Colour ranges are visual categories, "
            "not official weather warning thresholds."
        )

        # -------- SEVEN-DAY FORECAST --------
        st.header("📅 Seven-Day Weather Forecast")

        # Retrieve daily forecast from API
        daily = data["daily"]

        # Create daily DataFrame
        daily_df = pd.DataFrame({
            "Date": pd.to_datetime(daily["time"]),
            "Min Temp": daily["temperature_2m_min"],
            "Max Temp": daily["temperature_2m_max"],
            "Rain Chance": daily["precipitation_probability_max"],
            "Weather Code": daily["weather_code"],
            "Sunrise": daily["sunrise"],
            "Sunset": daily["sunset"]
        })

        # Convert weather codes into descriptions
        def weather_description(code):
            if code == 0:
                return "☀️ Clear"
            elif code in [1, 2]:
                return "🌤️ Partly Cloudy"
            elif code == 3:
                return "☁️ Overcast"
            elif code in [45, 48]:
                return "🌫️ Fog"
            elif code in [51, 53, 55, 56, 57]:
                return "🌦️ Drizzle"
            elif code in [61, 63, 65, 66, 67]:
                return "🌧️ Rain"
            elif code in [71, 73, 75, 77]:
                return "❄️ Snow"
            elif code in [80, 81, 82]:
                return "🌧️ Showers"
            elif code in [85, 86]:
                return "🌨️ Snow Showers"
            elif code in [95, 96, 99]:
                return "⛈️ Thunderstorm"
            return "🌡️ Other"

        daily_df["Condition"] = daily_df["Weather Code"].apply(
            weather_description
        )

        daily_df["Day"] = daily_df["Date"].dt.strftime("%a %d %b")

        
        
        # -------- RESPONSIVE SEVEN-DAY WEATHER CARDS --------

        # Create groups of up to 3 forecast cards
        for start in range(0, len(daily_df), 3):

            forecast_group = daily_df.iloc[start:start + 3]

           
            columns = st.columns(
                3,
                gap="medium"
            )


            for column, (_, row) in zip(
                columns,
                forecast_group.iterrows()
            ):
                condition = str(row["Condition"])
                day = str(row["Day"])
                max_temp = float(row["Max Temp"])
                min_temp = float(row["Min Temp"])
                rain = float(row["Rain Chance"])

                with column:
                    st.markdown(
                        f"""
                        <div class="forecast-card">
                            <div class="forecast-day">{day}</div>
                            <div class="forecast-condition">{condition}</div>
                            <div class="forecast-high">{max_temp:.0f}°C</div>
                            <div class="forecast-low">Low {min_temp:.0f}°C</div>
                            <div class="forecast-rain">💧 {rain:.0f}% rain</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )




        # Display seven-day table
        st.dataframe(
            daily_df[[
                "Day",
                "Condition",
                "Min Temp",
                "Max Temp",
                "Rain Chance",
                "Sunrise",
                "Sunset"
            ]],
            hide_index=True
        )

        # Create weekly temperature chart
        st.subheader("Weekly Temperature Outlook")

        fig_week = px.line(
            daily_df,
            x="Day",
            y=["Min Temp", "Max Temp"],
            markers=True,
            title="Daily Minimum and Maximum Temperatures"
        )

        fig_week.update_layout(
            xaxis_title="Day",
            yaxis_title="Temperature (°C)",
            height=450
        )

        st.plotly_chart(fig_week, width="stretch")


        # -------- SEVEN-DAY RAIN PROBABILITY --------
        st.subheader("🌧️ Seven-Day Rain Probability")

        fig_rain = px.bar(
            daily_df,
            x="Day",
            y="Rain Chance",
            title="Daily Maximum Probability of Precipitation",
            labels={
                "Day": "Day",
                "Rain Chance": "Rain Probability (%)"
            },
            text="Rain Chance",
            color="Rain Chance",
            color_continuous_scale="Blues",
            range_color=[0, 100]
        )

        fig_rain.update_traces(
            texttemplate="%{text:.0f}%",
            textposition="outside"
        )

        fig_rain.update_layout(
            height=450,
            yaxis=dict(range=[0, 105]),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig_rain, width="stretch")


        # -------- WEEKLY WEATHER INSIGHTS --------
        st.header("📊 Weekly Weather Insights")

        # Find the warmest day using maximum temperature
        warmest_day = daily_df.loc[
            daily_df["Max Temp"].idxmax()
        ]

        # Find the coldest day using minimum temperature
        coldest_day = daily_df.loc[
            daily_df["Min Temp"].idxmin()
        ]

        # Find the day with the highest rain probability
        rainiest_day = daily_df.loc[
            daily_df["Rain Chance"].idxmax()
        ]

        # Create three summary cards
        insight1, insight2, insight3 = st.columns(3)

        with insight1:
            st.metric(
                label=f"☀️ Warmest Day: {warmest_day['Day']}",
                value=f"{warmest_day['Max Temp']:.1f} °C"
            )

        with insight2:
            st.metric(
                label=f"❄️ Coldest Day: {coldest_day['Day']}",
                value=f"{coldest_day['Min Temp']:.1f} °C"
            )

        with insight3:
            st.metric(
                label=f"🌧️ Highest Rain Chance: {rainiest_day['Day']}",
                value=f"{rainiest_day['Rain Chance']:.0f}%"
            )


        # -------- SEVEN-DAY CSV DOWNLOAD --------
        st.subheader("📥 Download Seven-Day Forecast")

        # Copy daily forecast data
        weekly_export = daily_df[[
            "Day",
            "Condition",
            "Min Temp",
            "Max Temp",
            "Rain Chance",
            "Sunrise",
            "Sunset"
        ]].copy()

        # Convert the data into CSV format
        weekly_csv = weekly_export.to_csv(
            index=False
        ).encode("utf-8-sig")

        # Create the download button
        st.download_button(
            label="📥 Download Seven-Day Weather CSV",
            data=weekly_csv,
            file_name=f"{selected_city}_7_day_forecast.csv",
            mime="text/csv",
            key="weekly_csv_download"
        )






        # ---------------- WEATHER STATISTICS ----------------
        st.header("📊 24-Hour Weather Analysis")

        stat1, stat2, stat3 = st.columns(3)

        # Temperature statistics
        with stat1:
            st.subheader("🌡️ Temperature")

            st.metric(
                "Minimum",
                f"{df['Temperature'].min():.1f} °C"
            )

            st.metric(
                "Maximum",
                f"{df['Temperature'].max():.1f} °C"
            )

            st.metric(
                "Average",
                f"{df['Temperature'].mean():.1f} °C"
            )

        # Humidity statistics
        with stat2:
            st.subheader("💧 Humidity")

            st.metric(
                "Minimum",
                f"{df['Humidity'].min():.0f}%"
            )

            st.metric(
                "Maximum",
                f"{df['Humidity'].max():.0f}%"
            )

            st.metric(
                "Average",
                f"{df['Humidity'].mean():.1f}%"
            )

        # Wind speed statistics
        with stat3:
            st.subheader("💨 Wind Speed")

            st.metric(
                "Minimum",
                f"{df['Wind Speed'].min():.1f} km/h"
            )

            st.metric(
                "Maximum",
                f"{df['Wind Speed'].max():.1f} km/h"
            )

            st.metric(
                "Average",
                f"{df['Wind Speed'].mean():.1f} km/h"
            )

        # ---------------- DATA TABLE ----------------
        st.subheader("Hourly Weather Data")

        st.dataframe(
            df,
            hide_index=True
        )

        # ---------------- CSV DOWNLOAD ----------------
        st.subheader("📥 Download Weather Data")

        # Create a copy for export
        export_df = df.copy()

        # Format date and time
        export_df["Time"] = export_df["Time"].dt.strftime(
            "%Y-%m-%d %H:%M"
        )

        # Convert DataFrame to CSV
        csv_data = export_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        # Create download button
        st.download_button(
            label="Download 24-Hour Weather Forecast (CSV)",
            data=csv_data,
            file_name=f"{selected_city}_weather_forecast.csv",
            mime="text/csv"
        )

        # ---------------- API ATTRIBUTION ----------------
        st.caption(
            "Source: Open-Meteo (open-meteo.com). "
            "Forecasts are estimates, "
            "not on-site observations."
        )

    # ---------------- ERROR HANDLING ----------------
    except requests.RequestException as error:
        st.error(
            f"Could not contact the weather API: {error}"
        )

    except (KeyError, ValueError, TypeError) as error:
        st.error(
            f"Could not process the weather data: {error}"
        )


# ---------------- RUN DASHBOARD ----------------
# Call the function once, outside its definition
show_weather_dashboard()
