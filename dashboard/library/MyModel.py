from xgboost import XGBRegressor
import pandas as pd
class MyModel:
    def model(self, data):
        data = data.copy()
        data = self.getFuelTable(data)
        data = self.getFeatures(data)

        # Target
        data["target"] = data["actual_intensity"]

        # -------------------------
        # Features
        # -------------------------

        features = [
            "forecast_intensity",
            "forecast_error",

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
            "rolling_6",
            "renewable",
            "fossil",
            "low_carbon"
        ]

        # Remove rows with missing values
        model_data = data.dropna(
            subset=features + ["target"]
        ).copy()

        # -------------------------
        # Train/test split
        # -------------------------

        split = int(len(model_data) * 0.8)

        train = model_data.iloc[:split]
        test = model_data.iloc[split:]

        X_train = train[features]
        y_train = train["target"]

        X_test = test[features]
        y_test = test["target"]

        # -------------------------
        # Model
        # -------------------------

        model = XGBRegressor(
            n_estimators=500,
            max_depth=5,
            learning_rate=0.03,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            random_state=42
        )

        model.fit(
            X_train,
            y_train)

        predictions = model.predict(X_test)
        results = pd.DataFrame({
            "actual_intensity": y_test.values,
            "forecast_intensity": predictions
        })


        return results


    def getFuelTable(self, data):
        generation_mix = data.pivot_table(
            index="reading_id",
            columns="fuel_type",
            values="percentage",
            aggfunc="first"
        ).reset_index()

        readings = data[
            [
                "reading_id",
                "period_from",
                "period_to",
                "forecast_intensity",
                "actual_intensity"
            ]
        ].drop_duplicates()
        finalData = readings.merge(
            generation_mix,
            on="reading_id",
            how="left"
        )
        return finalData

    def getFeatures(self, data):
        data["hour"] = data["period_from"].dt.hour
        data["minute"] = data["period_from"].dt.minute
        data["day_of_week"] = data["period_from"].dt.dayofweek
        data["is_weekend"] = (data["day_of_week"] >= 5).astype(int)
        data["time_of_day"] = (
                data["hour"] * 2
                + (data["minute"] // 30)
        )
        data["target"] = data["actual_intensity"]

        data["lag_1"] = data["actual_intensity"].shift(1)
        data["lag_2"] = data["actual_intensity"].shift(2)
        data["lag_3"] = data["actual_intensity"].shift(3)
        data["lag_4"] = data["actual_intensity"].shift(4)

        # Same time yesterday
        data["lag_48"] = data["actual_intensity"].shift(48)

        # Rolling averages
        data["rolling_3"] = (
            data["actual_intensity"]
            .shift(1)
            .rolling(3)
            .mean()
        )

        data["rolling_6"] = (
            data["actual_intensity"]
            .shift(1)
            .rolling(6)
            .mean()
        )

        data["renewable"] = (
                data["biomass"]
                + data["hydro"]
                + data["solar"]
                + data["wind"]
        )

        data["fossil"] = (
                data["coal"]
                + data["gas"]
        )

        data["low_carbon"] = (
                data["nuclear"]
                + data["hydro"]
                + data["solar"]
                + data["wind"]
                + data["biomass"]
        )

        data["forecast_error"] = (
                data["actual_intensity"]
                - data["forecast_intensity"]
        )
        return data