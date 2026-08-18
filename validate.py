from database import get_connection
class Validate:
    def validateNational(self):
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT COUNT(*)
                        FROM national_readings
                        WHERE actual_intensity IS NULL;
                    """)
            missing_intensity = cursor.fetchone()[0]
            if missing_intensity > 0:
                print(
                    f"INFO: {missing_intensity} national readings "
                    f"have no actual intensity yet."
                )
            cursor.execute("""
                        SELECT reading_id, COUNT(*)
                        FROM national_readings
                        GROUP BY reading_id
                        HAVING COUNT(*) > 1;
                    """)

            duplicates = cursor.fetchall()

            if duplicates:
                print("WARNING: Duplicate national readings found:")
                for reading_id, count in duplicates:
                    print(f"  Reading {reading_id}: {count} rows")
            else:
                print("No duplicate national readings found.")

        connection.close()

    def validateRegional(self):
        connection = get_connection()
        with connection.cursor() as cursor:
            # Check that each period has 17 regions
            cursor.execute("""
                        SELECT reading_id, COUNT(DISTINCT region_id)
                        FROM regional_readings
                        GROUP BY reading_id
                        HAVING COUNT(DISTINCT region_id) != 18;
                    """)

            incomplete_periods = cursor.fetchall()

            if incomplete_periods:
                print("WARNING: Some periods do not contain 18 regions:")

                for reading_id, region_count in incomplete_periods:
                    print(
                        f"  Reading {reading_id}: "
                        f"{region_count} regions"
                    )
            else:
                print("Every regional period contains 18 regions.")

            # Check for duplicate regional readings
            cursor.execute("""
                        SELECT reading_id, region_id, COUNT(*)
                        FROM regional_readings
                        GROUP BY reading_id, region_id
                        HAVING COUNT(*) > 1;
                    """)

            duplicates = cursor.fetchall()

            if duplicates:
                print("Duplicate regional readings found:")

                for reading_id, region_id, count in duplicates:
                    print(
                        f"  Reading {reading_id}, "
                        f"Region {region_id}: {count} rows"
                    )
            else:
                print("No duplicate regional readings found.")

        connection.close()

    def validatePeriods(self):
        connection = get_connection()

        with connection.cursor() as cursor:

            # Look for periods where the end is before the start
            cursor.execute("""
                SELECT id, period_from, period_to
                FROM period_id
                WHERE period_from >= period_to;
            """)

            invalid_periods = cursor.fetchall()

            if invalid_periods:
                print("Invalid time periods found:")

                for row in invalid_periods:
                    print(f"  {row}")
            else:
                print("No invalid time periods found.")

        connection.close()

    def validate(self):
        print("Running data validation...")

        self.validateNational()
        self.validateRegional()
        self.validatePeriods()

        print("Data validation complete.")

validate = Validate()
validate.validate()