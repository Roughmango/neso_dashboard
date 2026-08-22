import streamlit as st
from library.mae_calculator import *
from library.data_access import get_national_readings
from library.MyModel import *


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

model = MyModel()
predictions = model.model(data)
st.write("Predictions:")
st.write(predictions.head())
st.write(calculate_forecast_accuracy(predictions))
