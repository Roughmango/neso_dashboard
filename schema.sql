CREATE TABLE period_id (
    id INTEGER PRIMARY KEY,
    period_from TEXT NOT NULL,
    period_to TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    UNIQUE(period_from, period_to, fetched_at)
);
CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL
);
CREATE TABLE national_readings (
    id INTEGER PRIMARY KEY,
    reading_id INTEGER NOT NULL,
    forecast_intensity INTEGER,
    actual_intensity INTEGER,
    intensity_index TEXT,

    FOREIGN KEY (reading_id) REFERENCES period_id(id),
    UNIQUE(reading_id)
);

CREATE TABLE regional_readings (
    id INTEGER PRIMARY KEY,
    reading_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    forecast_intensity INTEGER,
    actual_intensity INTEGER,
    intensity_index TEXT,

    FOREIGN KEY (reading_id) REFERENCES period_id(id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id),
    UNIQUE(reading_id, region_id)
);

CREATE TABLE national_generation_mix (
    id INTEGER PRIMARY KEY,
    reading_id INTEGER NOT NULL,
    fuel_type TEXT NOT NULL,
    percentage REAL,

    FOREIGN KEY (reading_id) REFERENCES period_id(id),
    UNIQUE(reading_id, fuel_type, percentage)
);

CREATE TABLE regional_generation_mix (
    id INTEGER PRIMARY KEY,
    reading_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    fuel_type TEXT NOT NULL,
    percentage REAL,

    FOREIGN KEY (reading_id) REFERENCES period_id(id),
    UNIQUE(reading_id, region_id, fuel_type, percentage)
);

INSERT INTO regions (region_id, region_name)
VALUES
    (1, 'North Scotland'),
    (2, 'South Scotland'),
    (3, 'North West England'),
    (4, 'North East England'),
    (5, 'Yorkshire'),
    (6, 'North Wales & Merseyside'),
    (7, 'South Wales'),
    (8, 'West Midlands'),
    (9, 'East Midlands'),
    (10, 'East England'),
    (11, 'South West England'),
    (12, 'South England'),
    (13, 'London'),
    (14, 'South East England'),
    (15, 'England'),
    (16, 'Scotland'),
    (17, 'Wales'),
    (18, 'GB');