-- Table: public.stations
--This table stores the weather station information, where each station has a unique code (e.g., USC00110072).
-- DROP TABLE IF EXISTS public.stations;

CREATE TABLE IF NOT EXISTS public.stations
(
    station_id integer NOT NULL DEFAULT nextval('stations_station_id_seq'::regclass), -- Auto-incrementing station ID
    station_code character varying(20) COLLATE pg_catalog."default" NOT NULL, -- Unique station identifier (e.g., 'USC00110072')
    CONSTRAINT stations_pkey PRIMARY KEY (station_id),
    CONSTRAINT stations_station_code_key UNIQUE (station_code)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.stations
    OWNER to postgres;