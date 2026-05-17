import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="🌍 Weather AI Dashboard", layout="wide")

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    color: white;
}

/* Header */
.main-header {
    background: linear-gradient(90deg, #6d28d9, #2563eb);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: white;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌦 Weather Intelligence AI Dashboard</div>', unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/weather_40_cities.csv")

# ---------------- CITY DROPDOWN ----------------
cities = df[["city", "country"]].drop_duplicates()
cities["label"] = cities["city"] + " - " + cities["country"]

city_selected = st.selectbox("🌍 Select City", cities["label"])
city = city_selected.split(" - ")[0]

city_data = df[df["city"] == city].reset_index(drop=True)

# ---------------- WEATHER SCORE ----------------
def weather_score(temp, humidity, rain, wind, aqi):
    score = 100
    score -= rain * 0.4
    score -= humidity * 0.2
    score -= wind * 0.5

    if temp > 40:
        score -= 25
    if temp < 10:
        score -= 15
    if aqi > 150:
        score -= 20

    return max(0, min(100, score))

# ---------------- ACTIVITY ENGINE ----------------
def activity_engine(score):
    if score > 80:
        return "🏕 Camping | 🚴 Cycling | 🏃 Running | 🏞 Trekking | ⚽ Sports"
    elif score > 60:
        return "🚶 Walking | 🚴 Cycling | 🧘 Yoga | 🏸 Badminton"
    else:
        return "🏠 Indoor activities recommended"

# ---------------- 20 DAY FORECAST ----------------
def generate_20_day_forecast(base_temp):
    dates = [datetime.today() + timedelta(days=i) for i in range(20)]
    temps = base_temp + np.random.normal(0, 2, 20)
    rain = np.random.randint(0, 100, 20)

    return pd.DataFrame({
        "date": dates,
        "temp": temps,
        "rain": rain
    })

# ---------------- 🚨 ALERT SYSTEM (NEW) ----------------
def weather_alert(city_data):

    alerts = []

    for i in range(min(4, len(city_data))):

        row = city_data.iloc[i]

        temp = row["temperature"]
        rain = row["rain_chance"]
        wind = row["wind_speed"]
        aqi = row["aqi"]

        day = f"Day {i+1}"

        if rain > 70:
            alerts.append(f"🌧 {day}: Heavy rain expected")

        if temp > 40:
            alerts.append(f"🔥 {day}: Extreme heat warning")

        if temp < 10:
            alerts.append(f"❄ {day}: Very cold conditions")

        if wind > 35:
            alerts.append(f"💨 {day}: Strong winds expected")

        if aqi > 150:
            alerts.append(f"😷 {day}: Poor air quality")

    if len(alerts) == 0:
        alerts.append("✅ No major weather alerts for next 4 days")

    return alerts

# ---------------- CURRENT WEATHER ----------------
st.markdown("## 📊 Current Weather")

row = city_data.iloc[0]

temp = row["temperature"]
humidity = row["humidity"]
rain = row["rain_chance"]
wind = row["wind_speed"]
aqi = row["aqi"]

score = weather_score(temp, humidity, rain, wind, aqi)
activity = activity_engine(score)

# ---------------- METRICS ----------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🌡 Temp", f"{temp} °C")
col2.metric("💧 Humidity", f"{humidity} %")
col3.metric("🌧 Rain", f"{rain} %")
col4.metric("💨 Wind", f"{wind}")
col5.metric("🏭 AQI", f"{aqi}")

st.progress(int(score))

st.success(f"🌟 Weather Score: {score}/100")
st.info(f"🏕 Activity Suggestion: {activity}")

# ---------------- 🚨 ALERT SECTION ----------------
st.markdown("## 🚨 Weather Alerts")

alerts = weather_alert(city_data)

for alert in alerts:
    if "Heavy rain" in alert:
        st.error(alert)
    elif "Extreme heat" in alert:
        st.warning(alert)
    elif "Very cold" in alert:
        st.info(alert)
    elif "Strong winds" in alert:
        st.warning(alert)
    elif "Poor air quality" in alert:
        st.error(alert)
    else:
        st.success(alert)

# ---------------- 20 DAY GRAPH ----------------
# ---------------- 20 DAY GRAPH (THEME MATCHED) ----------------
st.markdown("## 📈 20-Day Weather Forecast")

forecast_df = generate_20_day_forecast(temp)

fig = go.Figure()

# 🌡 Temperature line (blue like your UI)
fig.add_trace(go.Scatter(
    x=forecast_df["date"],
    y=forecast_df["temp"],
    mode="lines+markers",
    name="Temperature (°C)",
    line=dict(color="#60a5fa", width=3),  # light blue
    marker=dict(size=6, color="#60a5fa")
))

# 🌧 Rain bars (purple like your image)
fig.add_trace(go.Bar(
    x=forecast_df["date"],
    y=forecast_df["rain"],
    name="Rain Chance (%)",
    marker=dict(color="#7c3aed", opacity=0.7)  # purple
))

# 🎨 DARK THEME STYLING (IMPORTANT)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0f172a",   # dark navy background
    plot_bgcolor="#0f172a",
    font=dict(color="white"),
    height=450,
    title="20-Day Temperature & Rain Forecast",

    xaxis=dict(
        showgrid=False,
        color="white"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.1)",
        color="white"
    ),

    legend=dict(
        font=dict(color="white")
    )
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- CITY COMPARISON ----------------
st.markdown("## 🌍 All Cities Weather Comparison")

city_summary = df.groupby("city").agg({
    "temperature": "mean",
    "rain_chance": "mean",
    "aqi": "mean"
}).reset_index()

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=city_summary["city"],
    y=city_summary["temperature"],
    name="Avg Temp"
))

fig2.add_trace(go.Bar(
    x=city_summary["city"],
    y=city_summary["rain_chance"],
    name="Avg Rain"
))

fig2.update_layout(
    barmode="group",
    template="plotly_dark",
    height=500,
    title="City-wise Weather Comparison (40 Cities)"
)

st.plotly_chart(fig2, use_container_width=True)