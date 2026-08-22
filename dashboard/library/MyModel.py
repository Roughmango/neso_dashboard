from xgboost import XGBRegressor
import pandas as pd
class MyModel:
    def model(self, data):
        data = data.copy()
        data = self.getFuelTable(data)
        data["hour"] = data["period_from"].dt.hour
        data["minute"] = data["period_from"].dt.minute
        data["day_of_week"] = data["period_from"].dt.dayofweek
        data["is_weekend"] = (data["day_of_week"] >= 5).astype(int)
        data["time_of_day"] = (
            data["hour"] * 2
            + (data["minute"] // 30)
        )
        data["target"] = data["actual_intensity"]

        features = [
            "forecast_intensity",
            "hour",
            "minute",
            "day_of_week",
            "is_weekend",
            "time_of_day",
            "biomass",
            "coal",
            "imports",
            "gas",
            "nuclear",
            "other",
            "hydro",
            "solar",
            "wind"
        ]

        # remove rows where there is not enough historical information

        model_data = data.dropna(
            subset=features + ["target"]
        ).copy()

        split = int(len(model_data) * 0.8)

        train = model_data.iloc[:split]
        test = model_data.iloc[split:]

        X_train = train[features]
        y_train = train["target"]

        X_test = test[features]
        y_test = test["target"]


        model = XGBRegressor(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            objective="reg:squarederror",
            random_state=42
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(X_test)
        results = pd.DataFrame({
            "actual_intensity": y_test.values,
            "forecast_intensity": predictions
        })


        return results.head()


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