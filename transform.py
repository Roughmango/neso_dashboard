import sqlite3
import requests
from datetime import datetime, timezone

from fetch import Fetch


class Transform:
    def __init__(self):
        self.API_URL = "https://api.carbonintensity.org.uk/intensity"
        self.DB_PATH = "carbon_intensity.db"

    def transform(self):
        fetcher = Fetch()
        data, status_code = fetcher.fetch(self.API_URL)
        if status_code==200:
            fetched_at = datetime.now(timezone.utc).isoformat()
            # Connect to SQLite database
            connection = sqlite3.connect(self.DB_PATH)
            cursor = connection.cursor()
            for reading in data:
                cursor.execute(
                    """
                    INSERT INTO national_readings (
                        period_from,
                        period_to,
                        forecast_intensity,
                        actual_intensity,
                        intensity_index,
                        fetched_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        reading["from"],
                        reading["to"],
                        reading["intensity"]["forecast"],
                        reading["intensity"]["actual"],
                        reading["intensity"]["index"],
                        fetched_at
                    )
                )

            connection.commit()
            connection.close()

transform = Transform()
transform.transform()