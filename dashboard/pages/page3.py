import streamlit as st
from library.data_access import get_national_generation
from library.charts import national_mix_chart
st.title("Generation mix")


data = get_national_generation()
latest = data[data["period_from"] == data["period_from"].max()]
fig = national_mix_chart(latest)
st.plotly_chart(fig, use_container_width=True)