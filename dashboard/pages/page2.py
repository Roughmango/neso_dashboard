import streamlit as st
from library.mae_calculator import *
from library.data_access import get_national_readings

st.title("Forecast Accuracy")
st.write(
    "How accurately does the carbon-intensity forecast predict actual intensity overall?"
)
data = get_national_readings()
st.write(calculate_forecast_accuracy(data))
st.write(
    "How accurately does the carbon-intensity forecast predict actual intensity based on the comparison of yesterday to today?"
)
st.write(calculate_yesterday_mae(data))
