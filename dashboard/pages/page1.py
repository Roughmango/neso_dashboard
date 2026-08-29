import streamlit as st

from library.data_access import get_latest_national_reading

from library.data_access import get_latest_regional_readings
from library.charts import regional_intensity_chart
st.title("Live Carbon Intensity")

st.header("National intensity")
# This section is for latest national readings
data = get_latest_national_reading()

if data.empty:
    st.warning("No carbon intensity data available.")
else:

    reading = data.iloc[0]
    st.write(
        f"Period: {reading['period_from']} → "
        f"{reading['period_to']}"
    )

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

# this section is for the regional data
regional = get_latest_regional_readings()
st.header("Regional Intensity")
st.write(
        f"Period: {reading['period_from']} → "
        f"{reading['period_to']}"
    )
if regional.empty:
    st.warning("No regional carbon intensity data available.")
else:
    for _, regional_reading in regional.iterrows():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                    <div style="font-size: 14px;">
                        <b>Region name</b><br>
                        {regional_reading["region_name"]}
                    </div>
                    """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                    <div style="font-size: 14px;">
                        <b>Forecast</b><br>
                        {regional_reading["forecast_intensity"]}gCO₂/kWh
                    </div>
                    """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                        <div style="font-size: 14px;">
                            <b>Index</b><br>
                            {regional_reading["intensity_index"]}
                        </div>
                        """,
                unsafe_allow_html=True
            )

    fig = regional_intensity_chart(regional)

    st.plotly_chart(
        fig,
        width="stretch"
    )