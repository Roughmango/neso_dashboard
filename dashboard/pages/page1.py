import streamlit as st

from library.data_access import get_latest_national_reading

from library.data_access import get_latest_regional_readings
from library.charts import regional_intensity_chart
st.title("Live Carbon Intensity")

data = get_latest_national_reading()

if data.empty:
    st.warning("No carbon intensity data available.")
else:

    reading = data.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Forecast",
            f"{reading['forecast_intensity']} gCO₂/kWh"
        )

    with col2:
        st.metric(
            "Actual",
            f"{reading['actual_intensity']} gCO₂/kWh"
        )

    with col3:
        st.metric(
            "Index",
            reading["intensity_index"]
        )

    st.write(
        f"Period: {reading['period_from']} → "
        f"{reading['period_to']}"
    )

    regional = get_latest_regional_readings()

    st.subheader("Regional intensity")

    st.dataframe(
        regional,
        use_container_width=True
    )

    fig = regional_intensity_chart(regional)

    st.plotly_chart(
        fig,
        use_container_width=True
    )