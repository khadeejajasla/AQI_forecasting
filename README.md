# Air Quality Index forecasting

Forecasting Air Quality Index (AQI) across major Indian cities using time series models, with an interactive dashboard for exploring trends and future predictions.

🔗 **Live Demo:** https://aqi-forecasting-india.streamlit.app/

---

## 📌 Objective

To analyze historical air quality data across Indian cities and build a forecasting model that predicts future AQI levels, identifies high-risk pollution periods, and supports data-driven policy recommendations.

---

## 📊 Dataset

- **Source:** CPCB (Central Pollution Control Board) air quality records
- **Coverage:** 26 Indian cities, daily readings from 2015 to 2020
- **Features used:** PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, and AQI

---

## 🧹 Data Cleaning

- Handled missing pollutant values using per-city linear interpolation, preserving genuine seasonal spikes
- Removed sensor-error outliers (negative values, impossible highs) without deleting entire rows, to keep the daily timeline intact
- Rebuilt AQI categories (Good, Satisfactory, Moderate, Poor, Very Poor, Severe) after cleaning

---

## 🔍 Exploratory Data Analysis

- City-wise AQI comparison across all 26 cities
- Seasonal trend analysis (month-wise and year-wise)
- Pollutant correlation analysis
- Visible drop in AQI during the 2020 lockdown period

---

## 📈 Forecasting Models

| Model | Purpose |
|---|---|
| **ARIMA** | Baseline statistical time series model |
| **Facebook Prophet** | Final model, chosen for strength in modeling yearly seasonality |

**Model Comparison (Delhi):**

| Metric | ARIMA | Prophet |
|---|---|---|
| MAE | 90.36 | 64.21 |
| RMSE | 114.07 | 82.10 |
| MAPE | 53.21% | 43.94% |

Prophet outperformed ARIMA significantly, since ARIMA failed to capture the sharp winter and Diwali-season pollution spikes, while Prophet's built-in seasonality modeling tracked them closely.

---

## 💡 Key Insights

- Delhi showed the most severe air quality among the cities studied in depth, with winter AQI regularly crossing 400–700
- All cities show a consistent winter spike (November–January), driven by temperature inversion and festival-related emissions
- The model independently flagged early November (Diwali season) as the highest-risk period, purely from historical seasonality patterns
- Bengaluru showed the most stable and cleanest air quality among the cities analyzed

---

## 📋 Recommendations

- Stricter vehicle emission controls during winter months
- Festival-based emission advisories ahead of predicted peak-pollution days
- Expansion of green zones in high-AQI cities
- City-specific pollution monitoring instead of a uniform national policy

---

## 🖥️ Dashboard Features

An interactive Streamlit dashboard was built on top of the analysis, extending forecasts to 20 cities:
- Historical AQI trend viewer
- 12-month AQI forecast with confidence intervals
- Trend and seasonality breakdown
- Predicted peak pollution days with recommendations

---

## ⚙️ Tech Stack

Python, Pandas, NumPy, Matplotlib, Seaborn, Statsmodels (ARIMA), Facebook Prophet, Streamlit
