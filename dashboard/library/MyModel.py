from xgboost import XGBRegressor
import pandas as pd
class MyModel:
    def model(self, data):
        data = data.copy()

        data = self.getFuelTable(data)

        data = self.getFeatures(data)

        # Target
        data["target"] = data["actual_intensity"]


        # Features

        features = [
            "forecast_intensity",

            "hour",
            "minute",
            "day_of_week",
            "is_weekend",
            "time_of_day",

            "intensity_change",

            "lag_1",
            "forecast_vs_lag",
            "lag_2",
            "lag_3",
            "lag_4",
            "lag_48",
            "error_lag_1",
            "error_lag_2",
            "error_lag_3",
            "error_lag_48",

            "rolling_3",
            "rolling_6",
            "error_rolling_3",
            "error_rolling_6",
            "error_rolling_48",


            "renewable",
            "fossil",
            "low_carbon"
        ]

        # Remove rows with missing values
        model_data = data.dropna(
            subset=features + ["target"]
        ).copy()
        # i noticed there are instances in the data where the predicted data is wildly off the acutal value, so we do not want to train it on those values
        # this makes it so that if there is a difference of 50 or more between the actual and predicted then it does not train it on that
        model_data = model_data[
            (
                    model_data["forecast_intensity"]
                    - model_data["actual_intensity"]
            ).abs() < 50
            ].copy()

        # Train/test split


        split = int(len(model_data) * 0.8)

        train = model_data.iloc[:split]
        test = model_data.iloc[split:]

        X_train = train[features]
        y_train = train["target"]

        X_test = test[features]
        y_test = test["target"]

        # Model


        model = XGBRegressor(
            n_estimators=800,
            max_depth=5,
            learning_rate=0.03,
            subsample=0.7,
            colsample_bytree=0.7,
            objective="reg:absoluteerror",
            random_state=42
        )

        model.fit(
            X_train,
            y_train)
        importance = pd.Series(
            model.feature_importances_,
            index=features
        ).sort_values(ascending=False)

        print(importance)
        predictions = model.predict(X_test)
        results = pd.DataFrame({
            "actual_intensity": y_test.values,
            "forecast_intensity": predictions.round(0),
            "api_prediction": test["forecast_intensity"].values,
            "period_from": test["period_from"].values
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
        data["forecast_vs_lag"] = (
                data["forecast_intensity"]
                - data["lag_1"]
        )
        data["lag_2"] = data["actual_intensity"].shift(2)
        data["lag_3"] = data["actual_intensity"].shift(3)
        data["lag_4"] = data["actual_intensity"].shift(4)
        # Same time yesterday
        data["lag_48"] = data["actual_intensity"].shift(48)

        data["intensity_change"] = (
                data["actual_intensity"].shift(1)
                - data["actual_intensity"].shift(2)
        )

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
        #fuel types has to be shifted as although when training actual and fuel percentages is known,
        # in actuality when predicting for a time in the future the fuel percentage is not known
        data["renewable"] = (
                data["biomass"].shift(1)
                + data["hydro"].shift(1)
                + data["solar"].shift(1)
                + data["wind"].shift(1)
        )

        data["fossil"] = (
                data["coal"].shift(1)
                + data["gas"].shift(1)
        )

        data["low_carbon"] = (
                data["nuclear"].shift(1)
                + data["hydro"].shift(1)
                + data["solar"].shift(1)
                + data["wind"].shift(1)
                + data["biomass"].shift(1)
        )

        data["forecast_error"] = (
                data["actual_intensity"]
                - data["forecast_intensity"]
        )

        data["error_lag_1"] = data["forecast_error"].shift(1)
        data["error_lag_2"] = data["forecast_error"].shift(2)
        data["error_lag_3"] = data["forecast_error"].shift(3)
        data["error_lag_48"] = data["forecast_error"].shift(48)

        data["error_rolling_3"] = (
            data["forecast_error"]
            .shift(1)
            .rolling(3)
            .mean()
        )

        data["error_rolling_6"] = (
            data["forecast_error"]
            .shift(1)
            .rolling(6)
            .mean()
        )

        data["error_rolling_48"] = (
            data["forecast_error"]
            .shift(1)
            .rolling(48)
            .mean()
        )

        return data