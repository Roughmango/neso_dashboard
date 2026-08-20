import plotly.express as px


def regional_intensity_chart(data):

    fig = px.bar(
        data,
        x="forecast_intensity",
        y="region_name",
        orientation="h",
        title="Carbon Intensity by Region"
    )

    return fig

def national_mix_chart(data):
    fig = px.bar(
        data,
        x="percentage",
        y="fuel_type",
        orientation="h",
        title="National Generation mix"
    )

    return fig