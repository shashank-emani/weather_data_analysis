-- Table: public.crop_yield
--This table stores annual crop yield data. The combination of year is unique to prevent duplicate entries for the same year.

-- DROP TABLE IF EXISTS public.crop_yield;

CREATE TABLE IF NOT EXISTS public.crop_yield
(
    yield_id integer NOT NULL DEFAULT nextval('crop_yield_yield_id_seq'::regclass), -- Auto-incrementing crop yield record ID
    year integer NOT NULL, -- The year of the crop yield data
    crop_yield real NOT NULL, -- Crop yield value
    CONSTRAINT crop_yield_pkey PRIMARY KEY (yield_id),
    CONSTRAINT unique_year UNIQUE (year) -- Ensure only one record per year
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.crop_yield
    OWNER to postgres;