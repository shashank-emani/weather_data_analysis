-- Table: public.weather_stats
--This table stores annual weather statistics (average maximum and minimum temperatures, and total precipitation) for each station. 
--The combination of station_id and year is unique to ensure there is only one entry per station per year.


-- DROP TABLE IF EXISTS public.weather_stats;

CREATE TABLE IF NOT EXISTS public.weather_stats
(
    stats_id SERIAL PRIMARY KEY,            -- Auto-incrementing stats record ID
    station_id INTEGER NOT NULL,            -- Foreign key to stations table
    year INTEGER NOT NULL,                  -- The year for the statistics
    avg_max_temp REAL,                      -- Average maximum temperature for the year
    avg_min_temp REAL,                      -- Average minimum temperature for the year
    total_precipitation REAL,               -- Total precipitation for the year (in centimeters)
    CONSTRAINT weather_stats_pkey PRIMARY KEY (stats_id),
    CONSTRAINT unique_station_year UNIQUE (station_id, year), -- Ensure only one record per station per year
    CONSTRAINT fk_station_stats FOREIGN KEY (station_id)
        REFERENCES public.stations (station_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.weather_stats
    OWNER to postgres;