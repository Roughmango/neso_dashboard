CREATE TABLE national_readings (
    id INTEGER PRIMARY KEY,
    period_from TEXT NOT NULL,
    period_to TEXT NOT NULL,
    forecast_intensity INTEGER,
    actual_intensity INTEGER,
    intensity_index TEXT,
    fetched_at TEXT NOT NULL,
    UNIQUE(period_from, fetched_at)
);

CREATE TABLE regional_readings (
    id INTEGER PRIMARY KEY,
    region_id INTEGER,
    region_name TEXT,
    period_from TEXT NOT NULL,
    period_to TEXT NOT NULL,
    forecast_intensity INTEGER,
    actual_intensity INTEGER,
    intensity_index TEXT,
    fetched_at TEXT NOT NULL,
    UNIQUE(region_id, period_from, fetched_at)
);

CREATE TABLE generation_mix (
    id INTEGER PRIMARY KEY,
    period_from TEXT NOT NULL,
    fuel_type TEXT NOT NULL,
    percentage REAL,
    fetched_at TEXT NOT NULL
);