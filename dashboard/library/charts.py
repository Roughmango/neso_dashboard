import plotly.express as px
import plotly.graph_objects as go

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

def regional_mix_chart(data, region):
    fig = px.bar(
        data,
        x="percentage",
        y="fuel_type",
        orientation="h",
        title=f"{region} Generation mix"
    )
    return fig

def actual_vs_predicted(my_predicted):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=my_predicted["period_from"],
            y=my_predicted["actual_intensity"],
            mode="lines",
            name="Actual"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=my_predicted["period_from"],
            y=my_predicted["api_prediction"],
            mode="lines",
            name="API Forecast"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=my_predicted["period_from"],
            y=my_predicted["forecast_intensity"],
            mode="lines",
            name="My Model"
        )
    )

    fig.update_layout(
        title="Actual vs Predicted Carbon Intensity",
        xaxis_title="Time",
        yaxis_title="Carbon Intensity (gCO₂/kWh)",
        hovermode="x unified"
    )

    return fig