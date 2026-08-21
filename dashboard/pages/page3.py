import streamlit as st
from botocore import regions
from library.data_access import get_national_generation, get_regional_generation, get_region_name
from library.charts import national_mix_chart, regional_mix_chart
st.title("Generation mix")


data = get_national_generation()
reading = data.iloc[0]
st.write(
        f"Period: {reading['period_from']} → "
        f"{reading['period_to']}"
    )
latest = data[data["period_from"] == data["period_from"].max()]
fig = national_mix_chart(latest)
st.plotly_chart(fig, use_container_width=True)

columns = st.columns(3)

for i, region in enumerate(range(1, 98)):
    regional_data = get_regional_generation(region)

    latest = regional_data[
        regional_data["period_from"] == regional_data["period_from"].max()
    ]

    fig = regional_mix_chart(
        latest,
        get_region_name(region)
    )

    with columns[i % 3]:
        st.plotly_chart(fig, use_container_width=True)