import sqlite3

connection = sqlite3.connect("carbon_intensity.db")

with open("schema.sql", "r") as file:
    schema = file.read()

connection.executescript(schema)
connection.commit()
connection.close()