import streamlit as st
from library.advisor import get_greenest_windows
from library.data_access import get_regional_readings

from library.RegionalModel import RegionalModel

st.title("Smart Advisor")

st.write(
    "The Smart Advisor predicts the greenest periods "
    "over the next 24 hours for each region."
)



# Get regional data

data = get_regional_readings()


# Train regional model

model = RegionalModel()

results = model.train(data)

# Predict next 24 hours

predictions = model.predict_next_24_hours(
    results
)


# -------------------------
# Find greenest periods
# -------------------------

greenest = get_greenest_windows(
    predictions,
    windows_per_region=3
)


# -------------------------
# Display
# -------------------------

st.subheader("Greenest periods")

st.dataframe(
    greenest,
    hide_index=True
)