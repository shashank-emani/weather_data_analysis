"""
This script performs data analysis on weather data and inserts
calculated yearly statistics into the `weather_stats` table in a PostgreSQL database.
It logs the start and end of the process, including any errors encountered.
"""

import logging
from datetime import datetime
import psycopg2

# Set up logging configuration
logging.basicConfig(filename='data_analysis.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')

# PostgreSQL connection details (replace DB and password with original ones)
conn = psycopg2.connect(
    host="localhost",           # PostgreSQL host
    database="weather",        # Name of the database
    user="postgres",             # PostgreSQL username
    password="****"       # PostgreSQL password
)
cursor = conn.cursor()

# Log the start of the analysis process
start_time = datetime.now()
logging.info('Data analysis process started.')

# SQL query for calculating the yearly statistics
analysis_query = '''
INSERT INTO weather_stats (station_id, year, avg_max_temp, avg_min_temp, total_precipitation)
SELECT
    wd.station_id,
    EXTRACT(YEAR FROM wd.weather_date) AS year,
    AVG(wd.max_temp) AS avg_max_temp,
    AVG(wd.min_temp) AS avg_min_temp,
    SUM(wd.precipitation) / 10 AS total_precipitation  -- Convert from mm to cm
FROM
    weather_data wd
WHERE
    wd.max_temp IS NOT NULL
    AND wd.min_temp IS NOT NULL
    AND wd.precipitation IS NOT NULL
GROUP BY
    wd.station_id, year
ON CONFLICT (station_id, year) DO NOTHING;
'''

# Execute the query and log the process
try:
    logging.info("Executing data analysis query.")
    cursor.execute(analysis_query)
    conn.commit()
    logging.info('Data analysis and insertion into weather_stats completed successfully.')
except Exception as e:
    logging.error(f"Error during data analysis: {e}")
    conn.rollback()

# Log the end of the analysis process
end_time = datetime.now()
logging.info(f'Total duration: {end_time - start_time}')

# Close the database connection
cursor.close()
conn.close()
