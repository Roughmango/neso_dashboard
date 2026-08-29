import pandas as pd


def get_greenest_windows(predictions, windows_per_region=3):
    predictions = predictions.copy()
    predictions = predictions.sort_values(
        ["region_name", "prediction"]
    )

    greenest = (
        predictions
        .groupby("region_name")
        .head(windows_per_region)
        .copy()
    )

    greenest["time"] = (
        greenest["period_from"]
        .dt.strftime("%H:%M")
    )
    greenest = greenest.sort_values(
        by="prediction",
        ascending=True
    )
    return greenest[
        ["region_name", "time", "prediction"]
    ]