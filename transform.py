import requests
from datetime import datetime, timezone
from database import get_connection


class Transform:
    """
    This class is used to collect data from the api and then transform it so that it can be added to the database
    in the correct area
    """
    def __init__(self):
        self.DB_PATH = "carbon_intensity.db"

    def transformNational(self):
        """
        This function is used to transform all data that is related to the national readings, so that it can be added
        to the database in the correct table
        :return:
        """
        # gets the initial data response of its carbon value
        response = requests.get("https://api.carbonintensity.org.uk/intensity")
        data, status_code = response.json()["data"], response.status_code
        # gets the initial data response of the make up of the carbon generation and the fuel used
        data_response = requests.get("https://api.carbonintensity.org.uk/generation")
        fuel_data, fuel_status_code = data_response.json()["data"], data_response.status_code
        # checks that both requests have not encountered an error
        if status_code and fuel_status_code != 200:
            print(f"National API request failed: {status_code, fuel_status_code}")
            return
        # connects to the database
        with get_connection() as connection:
            cursor = connection.cursor()

            for reading in data:
                # Create the time-period record if it doesn't already exist
                self.insertPeriodID(cursor, reading)

                # Get the ID for this time period
                reading_id = self.getReadingID(cursor, reading)

                # Insert national reading
                cursor.execute(
                    """
                    INSERT INTO national_readings (
                        reading_id,
                        forecast_intensity,
                        actual_intensity,
                        intensity_index
                    )
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
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
        """
            This function is used to transform all data that is related to the regional readings, so that it can be added
            to the database in the correct table
        :return:
        """
        #gets the regional data
        response = requests.get("https://api.carbonintensity.org.uk/regional")
        data, status_code = response.json()["data"], response.status_code
        # ensures a error was not encountered getting the api data
        if status_code != 200:
            print(f"Regional API request failed: {status_code}")
            return
        #sets up the connection with the database
        with get_connection() as connection:
            cursor = connection.cursor()
            # goes over every region in the data
            for period in data:

                # Create the time-period record
                self.insertPeriodID(cursor, period)
                # gets the id for the time period
                reading_id = self.getReadingID(cursor, period)

                # Insert each region
                for region in period["regions"]:

                    # Insert regional reading
                    cursor.execute(
                        """
                        INSERT INTO regional_readings (
                            reading_id,
                            region_id,
                            forecast_intensity,
                            actual_intensity,
                            intensity_index
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
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
        """
        This function is used to transform all data that is related to the national mix of fuel so that it can be input
        into its correct table
        :param cursor: the connection with the database
        :param reading_id: the id of its time period
        :param fuel_data: the fuel data it is adding
        :return:
        """
        for fuel in fuel_data:
            # for each type of fuel adds it to the database for that national reading
            cursor.execute(
                """
                INSERT INTO national_generation_mix (
                    reading_id,
                    fuel_type,
                    percentage
                )
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (
                    reading_id,
                    fuel["fuel"],
                    fuel["perc"]
                )
            )

    def transformRegionalMix(self, cursor, reading_id, fuel_data, region_id):
        """
                This function is used to transform all data that is related to the regional mix of fuel so that it can be input
                into its correct table
                :param cursor: the connection with the database
                :param reading_id: the id of its time period
                :param fuel_data: the fuel data it is adding
                :param region_id: the id of the region this data belongs to
                :return:
                """
        for fuel in fuel_data:
            # goes other every type of fuel and adds it to the database
            cursor.execute(
                """
                INSERT INTO regional_generation_mix (
                    reading_id,
                    region_id,
                    fuel_type,
                    percentage
                )
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (
                    reading_id,
                    region_id,
                    fuel["fuel"],
                    fuel["perc"]
                )
            )

    def insertPeriodID(self, cursor, reading):
        """
        This function is used to insert the period ID into the database, the period id is the id used for each
        time period that is being recorded
        :param cursor: the connection with the database
        :param reading: the time period
        :return:
        """
        #records when the data was fetched at
        # this rounds it to the nearest 5 minute
        now = datetime.now(timezone.utc)
        minutes = (now.minute // 5) * 5

        fetched_at = now.replace(
            minute=minutes,
            second=0,
            microsecond=0
        ).isoformat()
        cursor.execute(
            """
            INSERT INTO period_id (
                period_from,
                period_to,
                fetched_at
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (period_from, period_to, fetched_at) DO NOTHING
            """,
            (
                reading["from"],
                reading["to"],
                fetched_at
            )
        )

    def getReadingID(self, cursor, reading):
        """
        This function is used to get the reading id from the database
        :param cursor: the connection with the database
        :param reading: the data it is reading from
        :return:
        """
        cursor.execute(
            """
            SELECT id
            FROM period_id
            WHERE period_from = %s
            AND period_to = %s
            """,
            (
                reading["from"],
                reading["to"]
            )
        )

        return cursor.fetchone()[0]
