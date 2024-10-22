-- Table: public.weather_data
--This table stores daily weather data. Each weather record is linked to a station using the station_id foreign key. 
--The combination of station_id, weather_date, max_temp, min_temp, and precipitation is unique to avoid duplicates.

-- DROP TABLE IF EXISTS public.weather_data;

CREATE TABLE IF NOT EXISTS public.weather_data
(
    weather_id SERIAL PRIMARY KEY,          -- Auto-incrementing weather record ID
    station_id INTEGER NOT NULL,            -- Foreign key to stations table
    weather_date DATE NOT NULL,             -- The date of the weather record
    max_temp REAL,                          -- Maximum temperature (in tenths of degrees Celsius)
    min_temp REAL,                          -- Minimum temperature (in tenths of degrees Celsius)
    precipitation REAL,                     -- Precipitation (in tenths of millimeters)
    CONSTRAINT weather_data_pkey PRIMARY KEY (weather_id),
    CONSTRAINT unique_weather_data UNIQUE (station_id, weather_date, max_temp, min_temp, precipitation), -- Enforce uniqueness
    CONSTRAINT fk_station FOREIGN KEY (station_id)
        REFERENCES public.stations (station_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.weather_data
    OWNER to postgres;