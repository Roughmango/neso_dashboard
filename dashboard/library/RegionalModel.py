from xgboost import XGBRegressor
import pandas as pd


class RegionalModel:

    def __init__(self):
        self.model = None

        self.features = [

            "hour",
            "minute",
            "day_of_week",
            "is_weekend",
            "time_of_day",

            "lag_1",
            "lag_2",
            "lag_3",
            "lag_4",
            "lag_48",

            "rolling_3",
            "rolling_6"
        ]

    def train(self, data):

        data = data.copy()
        data["period_from"] = pd.to_datetime(
            data["period_from"],
            utc=True
        )

        # Make sure each region is in chronological order

        data = self.getFeatures(data)


        # -------------------------
        # Train/test split
        # -------------------------

        split = int(len(data) * 0.8)

        train = data.iloc[:split]
        test = data.iloc[split:]

        X_train = train[self.features]
        y_train = train["forecast_intensity"]

        X_test = test[self.features]
        y_test = test["forecast_intensity"]

        # -------------------------
        # Model
        # -------------------------

        self.model = XGBRegressor(
            n_estimators=800,
            max_depth=5,
            learning_rate=0.03,
            subsample=0.7,
            colsample_bytree=0.7,
            objective="reg:absoluteerror",
            random_state=42
        )


        self.model.fit(
            X_train,
            y_train
        )

        predictions = self.model.predict(X_test)

        results = test[
            [
                "region_name",
                "period_from",
            ]
        ].copy()

        results["prediction"] = predictions.round(0)

        return results

    def predict_next_24_hours(self, data):

        if self.model is None:
            raise ValueError(
                "Model has not been trained. "
                "Call train() first."
            )

        data = data.copy()

        data["period_from"] = pd.to_datetime(
            data["period_from"],
            utc=True
        )

        data = data.sort_values(
            ["region_name", "period_from"]
        )

        predictions = []

        # Predict each region separately
        for region, region_data in data.groupby("region_name"):

            region_data = region_data.copy()

            region_data = region_data.sort_values(
                "period_from"
            )

            history = list(
                region_data["prediction"]
                .dropna()
                .values[-48:]
            )

            if len(history) < 48:
                continue

            # Last known row
            last_row = region_data.iloc[-1]

            # Start 30 minutes after the latest reading
            next_time = (
                last_row["period_from"]
                + pd.Timedelta(minutes=30)
            )

            # Generate 48 half-hour predictions
            for _ in range(48):

                row = {}

                # Time features

                row["hour"] = next_time.hour
                row["minute"] = next_time.minute
                row["day_of_week"] = next_time.dayofweek
                row["is_weekend"] = int(
                    next_time.dayofweek >= 5
                )

                row["time_of_day"] = (
                    next_time.hour * 2
                    + next_time.minute // 30
                )

                # Historical / predicted lags

                row["lag_1"] = history[-1]
                row["lag_2"] = history[-2]
                row["lag_3"] = history[-3]
                row["lag_4"] = history[-4]

                # Same time yesterday
                row["lag_48"] = history[-48]

                # Rolling averages

                row["rolling_3"] = (
                    sum(history[-3:]) / 3
                )

                row["rolling_6"] = (
                    sum(history[-6:]) / 6
                )

                # API forecast

                # Find the API forecast for this
                # future timestamp.
                matching = region_data[
                    region_data["period_from"] == next_time
                ]

                if len(matching) > 0:
                    row["forecast_intensity"] = (
                        matching.iloc[0]["forecast_intensity"]
                    )
                else:
                    # If no API forecast exists,
                    # we cannot use this feature.
                    row["forecast_intensity"] = (
                        history[-1]
                    )

                # Make prediction


                X = pd.DataFrame(
                    [row],
                    columns=self.features
                )

                prediction = self.model.predict(X)[0]

                predictions.append({
                    "region_name": region,
                    "period_from": next_time,
                    "prediction": prediction.round(0).astype(int)
                })

                # Add prediction to history.
                # This allows the next prediction to use it as lag_1.
                history.append(prediction)

                # Keep only the last 48 values
                history = history[-48:]

                next_time += pd.Timedelta(
                    minutes=30
                )

        return pd.DataFrame(predictions)

    def getFeatures(self, data):

        data = data.copy()

        data["actual_intensity"] = pd.to_numeric(
            data["forecast_intensity"],
            errors="coerce"
        )
        # Calculate lags separately for each region.

        data["hour"] = data["period_from"].dt.hour
        data["minute"] = data["period_from"].dt.minute

        data["day_of_week"] = (
            data["period_from"].dt.dayofweek
        )

        data["is_weekend"] = (
            data["day_of_week"] >= 5
        ).astype(int)

        data["time_of_day"] = (
            data["hour"] * 2
            + data["minute"] // 30
        )

        # Historical intensity
        data["lag_1"] = (
            data.groupby("region_name")["actual_intensity"]
            .shift(1)
        )

        data["lag_2"] = (
            data.groupby("region_name")["actual_intensity"]
            .shift(2)
        )

        data["lag_3"] = (
            data.groupby("region_name")["actual_intensity"]
            .shift(3)
        )

        data["lag_4"] = (
            data.groupby("region_name")["actual_intensity"]
            .shift(4)
        )

        data["lag_48"] = (
            data.groupby("region_name")["actual_intensity"]
            .shift(48)
        )

        # Rolling averages
        data["rolling_3"] = (
            data.groupby("region_name")["actual_intensity"]
            .transform(
                lambda x:
                x.shift(1).rolling(3).mean()
            )
        )

        data["rolling_6"] = (
            data.groupby("region_name")["actual_intensity"]
            .transform(
                lambda x:
                x.shift(1).rolling(6).mean()
            )
        )

        return data