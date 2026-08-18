import os
import psycopg


def get_connection():
    # returns the connection to the database
    database_url = os.environ["DATABASE_URL"]

    return psycopg.connect(database_url)