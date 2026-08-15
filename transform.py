import sqlite3
import requests
from datetime import datetime, timezone

from fetch import Fetch


class Transform:
    def __init__(self):
        self.DB_PATH = "carbon_intensity.db"

    def transformNational(self):
        fetcher = Fetch()

        data, status_code = fetcher.fetch(
            "https://api.carbonintensity.org.uk/intensity"
        )
        fuel_data, fuel_status_code = fetcher.fetch(
            "https://api.carbonintensity.org.uk/generation"
        )
        if status_code and fuel_status_code != 200:
            print(f"National API request failed: {status_code, fuel_status_code}")
            return

        with sqlite3.connect(self.DB_PATH) as connection:
            cursor = connection.cursor()

            for reading in data:
                # Create the time-period record if it doesn't already exist
                self.insertPeriodID(cursor, reading)

                # Get the ID for this time period
                reading_id = self.getReadingID(cursor, reading)

                # Insert national reading
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO national_readings (
                        reading_id,
                        forecast_intensity,
                        actual_intensity,
                        intensity_index
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        reading_id,
                        reading["intensity"].get("forecast"),
                        reading["intensity"].get("actual"),
                        reading["intensity"].get("index")
                    )
                )
                self.transformNationalMix(cursor, reading_id, fuel_data["generationmix"])


    def transformRegional(self):
        fetcher = Fetch()

        data, status_code = fetcher.fetch(
            "https://api.carbonintensity.org.uk/regional"
        )

        if status_code != 200:
            print(f"Regional API request failed: {status_code}")
            return

        with sqlite3.connect(self.DB_PATH) as connection:
            cursor = connection.cursor()

            for period in data:

                # Create the time-period record
                self.insertPeriodID(cursor, period)

                reading_id = self.getReadingID(cursor, period)

                # Insert each region
                for region in period["regions"]:

                    # Insert regional reading
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO regional_readings (
                            reading_id,
                            region_id,
                            forecast_intensity,
                            actual_intensity,
                            intensity_index
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            reading_id,
                            region["regionid"],
                            region["intensity"].get("forecast"),
                            region["intensity"].get("actual"),
                            region["intensity"].get("index")
                        )
                    )
                    self.transformRegionalMix(cursor, reading_id, region["generationmix"],region["regionid"])

    def transformNationalMix(self,cursor, reading_id, fuel_data):
        for fuel in fuel_data:
            cursor.execute(
                """
                INSERT OR IGNORE INTO national_generation_mix (
                    reading_id,
                    fuel_type,
                    percentage
                )
                VALUES (?, ?, ?)
                """,
                (
                    reading_id,
                    fuel["fuel"],
                    fuel["perc"]
                )
            )

    def transformRegionalMix(self, cursor, reading_id, fuel_data, region_id):
        for fuel in fuel_data:
            cursor.execute(
                """
                INSERT OR IGNORE INTO regional_generation_mix (
                    reading_id,
                    region_id,
                    fuel_type,
                    percentage
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    reading_id,
                    region_id,
                    fuel["fuel"],
                    fuel["perc"]
                )
            )

    def insertPeriodID(self, cursor, reading):
        now = datetime.now(timezone.utc)
        minutes = (now.minute // 5) * 5

        fetched_at = now.replace(
            minute=minutes,
            second=0,
            microsecond=0
        ).isoformat()
        cursor.execute(
            """
            INSERT OR IGNORE INTO period_id (
                period_from,
                period_to,
                fetched_at
            )
            VALUES (?, ?, ?)
            """,
            (
                reading["from"],
                reading["to"],
                fetched_at
            )
        )

    def getReadingID(self, cursor, reading):
        cursor.execute(
            """
            SELECT id
            FROM period_id
            WHERE period_from = ?
            AND period_to = ?
            """,
            (
                reading["from"],
                reading["to"]
            )
        )

        return cursor.fetchone()[0]

transform = Transform()
transform.transformNational()
transform.transformRegional()