import pandas as pd


def get_greenest_windows(data, windows_per_region=3):

    data = data.copy()

    # Make sure timestamps are datetime
    data["period_from"] = pd.to_datetime(
        data["period_from"],
        utc=True
    )

    # Get the current time
    now = pd.Timestamp.now(tz="UTC")

    # Only look at the next 24 hours
    next_24_hours = data[
        (data["period_from"] >= now) &
        (data["period_from"] <= now + pd.Timedelta(hours=24))
    ].copy()

    # Sort lowest carbon intensity first within each region
    next_24_hours = next_24_hours.sort_values(
        ["region_id", "forecast_intensity"]
    )

    # Take the greenest periods for each region
    greenest = (
        next_24_hours
        .groupby("region_id")
        .head(windows_per_region)
        .copy()
    )

    # Format the timestamp for display
    greenest["time"] = greenest["period_from"].dt.strftime(
        "%H:%M"
    )

    # Rename for the dashboard
    greenest = greenest.rename(
        columns={
            "forecast_intensity": "Forecast intensity"
        }
    )

    return greenest[
        [
            "region_id",
            "time",
            "Forecast intensity"
        ]
    ]