import streamlit as st
from library.advisor import get_greenest_windows
from library.data_access import get_regional_readings

st.title("Smart Advisor")

st.write(
    "The greenest periods over the next 24 hours based on "
    "forecast carbon intensity."
)

data = get_regional_readings()

greenest = get_greenest_windows(data)

st.dataframe(
    greenest,
    hide_index=True
)