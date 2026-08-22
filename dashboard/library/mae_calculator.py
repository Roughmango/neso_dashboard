import pandas as pd
import numpy as np

from sklearn.metrics import mean_absolute_error, mean_squared_error

def calculate_yesterday_mae(data):
    data["period_from"] = pd.to_datetime(data["period_from"], utc=True)
    # drops readings that have a null intensity
    data = data.dropna(subset=["actual_intensity"])
    data.head()

    data["target"] = data["actual_intensity"]

    # Create a copy containing yesterday's readings
    yesterday = data[
        ["period_from", "actual_intensity"]
    ].copy()

    # Move yesterday's timestamps forward by one day
    # so they line up with today's timestamps
    yesterday["period_from"] = (
            yesterday["period_from"] + pd.Timedelta(days=1)
    )

    # Rename the intensity so we know it came from yesterday
    yesterday = yesterday.rename(
        columns={
            "actual_intensity": "yesterday_intensity"
        }
    )

    # Match today's timestamp with the exact same time yesterday
    data = data.merge(
        yesterday,
        on="period_from",
        how="left"
    )
    baseline = data.dropna(
        subset=["actual_intensity", "yesterday_intensity"]
    ).copy()

    baseline_mae = mean_absolute_error(
        baseline["actual_intensity"],
        baseline["yesterday_intensity"]
    )

    baseline_rmse = np.sqrt(
        mean_squared_error(
            baseline["actual_intensity"],
            baseline["yesterday_intensity"]
        )
    )
    return round(baseline_mae,3), float(round(baseline_rmse,3))

def calculate_forecast_accuracy(data):

    data = data.copy()

    valid = data.dropna(
        subset=["forecast_intensity", "actual_intensity"]
    )

    mae = mean_absolute_error(
        valid["actual_intensity"],
        valid["forecast_intensity"]
    )

    rmse = np.sqrt(
        mean_squared_error(
            valid["actual_intensity"],
            valid["forecast_intensity"]
        )
    )

    return round(mae,3), float(round(rmse,3))