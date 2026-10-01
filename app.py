import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

st.set_page_config(page_title="AQI Forecasting", page_icon="🌫️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stMetric { background-color: #1C2630; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { font-size: 22px; }
    h1, h2, h3 { color: #2E8B57; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🌫️ Air Quality Index Forecasting</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Forecasting pollution trends across major Indian cities using Facebook Prophet</p>", unsafe_allow_html=True)
st.divider()

df = pd.read_csv('city_day_cleaned.csv')
df['Date'] = pd.to_datetime(df['Date'])

st.sidebar.image("https://img.icons8.com/emoji/96/fog.png", width=80)
st.sidebar.header("Dashboard Controls")
city = st.sidebar.selectbox("🏙️ Select a city", [
    'Delhi', 'Mumbai', 'Kolkata', 'Bengaluru',
    'Chennai', 'Hyderabad', 'Ahmedabad', 'Lucknow',
    'Jaipur', 'Patna', 'Amritsar', 'Chandigarh',
    'Guwahati', 'Coimbatore', 'Visakhapatnam', 'Bhopal', 'Gurugram',
    'Thiruvananthapuram', 'Kochi', 'Jorapokhar'])
months = st.sidebar.slider("📅 Forecast period (months)", 3, 12, 12)
st.sidebar.markdown("---")
st.sidebar.caption("Data source: CPCB, 2015–2020")

city_df = df[df['City'] == city].set_index('Date')['AQI'].asfreq('D').interpolate()

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Average AQI", f"{city_df.mean():.0f}")
col2.metric("🔺 Highest Recorded", f"{city_df.max():.0f}")
col3.metric("🔻 Lowest Recorded", f"{city_df.min():.0f}")

def aqi_category(x):
    if x <= 50: return "Good 🟢"
    if x <= 100: return "Satisfactory 🟡"
    if x <= 200: return "Moderate 🟠"
    if x <= 300: return "Poor 🔴"
    if x <= 400: return "Very Poor 🟣"
    return "Severe ⚫"

col4.metric("🩺 Current Category", aqi_category(city_df.mean()))

st.divider()

tab1, tab2, tab3 = st.tabs(["📈 Historical Trend", "🔮 Forecast", "⚠️ Risk Days"])

with tab1:
    st.subheader(f"Historical AQI — {city}")
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    ax1.plot(city_df.index, city_df.values, color='#2E8B57')
    ax1.set_facecolor("#0E1117")
    fig1.patch.set_facecolor("#0E1117")
    ax1.tick_params(colors='white')
    ax1.set_xlabel("Date", color='white')
    ax1.set_ylabel("AQI", color='white')
    st.pyplot(fig1)

prophet_df = city_df.reset_index()
prophet_df.columns = ['ds', 'y']

with st.spinner("Training forecast model..."):
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=months * 30)
    forecast = model.predict(future)

with tab2:
    st.subheader(f"{months}-Month Forecast — {city}")
    fig2 = model.plot(forecast)
    st.pyplot(fig2)

    st.subheader("Trend & Seasonality Breakdown")
    fig3 = model.plot_components(forecast)
    st.pyplot(fig3)

with tab3:
    st.subheader("Predicted Peak Pollution Days")
    future_only = forecast[forecast['ds'] > prophet_df['ds'].max()]
    worst_days = future_only.sort_values('yhat', ascending=False).head(5)[['ds', 'yhat']]
    worst_days.columns = ['Date', 'Predicted AQI']
    worst_days['Date'] = worst_days['Date'].dt.strftime('%d %b %Y')
    worst_days['Predicted AQI'] = worst_days['Predicted AQI'].round(1)
    st.table(worst_days)
    st.info("💡 Recommendation: Issue public advisories and emission restrictions ahead of these predicted peak days.")

st.divider()
st.caption("Built with Streamlit & Prophet | CPCB Air Quality Dataset (2015–2020)")