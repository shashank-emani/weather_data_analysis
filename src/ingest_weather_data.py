"""
This script ingests weather data from multiple files, processes them, and
inserts the data into a PostgreSQL database. It logs each step of the process
and handles any errors that occur during the data insertion.
"""

import os
import psycopg2
import logging
from datetime import datetime

# Set up logging configuration
logging.basicConfig(filename='data_ingestion.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')

# Log the start of the process
start_time = datetime.now()
logging.info('Data ingestion process started.')

# PostgreSQL connection details (password with original ones)
conn = psycopg2.connect(
    host="localhost",
    database="collabery",
    user="postgres",
    password="****"
)
cursor = conn.cursor()


def insert_station(station_code):
    """
    Inserts the station_code into the 'stations' table if it does not already exist.
    Uses ON CONFLICT DO NOTHING to avoid duplicate station entries.

    Args:
        station_code (str): The station code extracted from the file name.
    """
    cursor.execute('''
        INSERT INTO stations (station_code)
        VALUES (%s)
        ON CONFLICT (station_code) DO NOTHING
    ''', (station_code,))
    conn.commit()


def get_station_id(station_code):
    """
    Retrieves the station_id for the given station_code from the 'stations' table.

    Args:
        station_code (str): The station code for which to retrieve the ID.

    Returns:
        int: The station_id corresponding to the station_code.
    """
    cursor.execute('SELECT station_id FROM stations WHERE station_code = %s', (station_code,))
    return cursor.fetchone()[0]


def insert_weather_data(station_id, date, max_temp, min_temp, precipitation):
    """
    Inserts weather data into the 'weather_data' table.

    Args:
        station_id (int): The ID of the weather station.
        date (str): The date of the weather record.
        max_temp (float): The maximum temperature for the day.
        min_temp (float): The minimum temperature for the day.
        precipitation (float): The precipitation level for the day.

    Returns:
        int: Returns 1 if a row was inserted successfully, otherwise 0.
    """
    try:
        cursor.execute('''
            INSERT INTO weather_data (station_id, weather_date, max_temp, min_temp, precipitation)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (station_id, weather_date, max_temp, min_temp, precipitation) DO NOTHING
        ''', (station_id, date, max_temp, min_temp, precipitation))
        conn.commit()
        return 1  # Successful insert
    except Exception as e:
        logging.error(f"Error inserting data for station_id {station_id}: {e}")
        return 0  # No new row inserted


# Initialize a total record count
total_records_inserted = 0

# Path to the directory containing weather data files
wx_data_directory = '/Users/shashankemani/Desktop/code-challenge-template/wx_data'

# Loop through each weather file in the directory
for file_name in os.listdir(wx_data_directory):
    logging.info(f'Processing file: {file_name}')
    station_code = os.path.splitext(file_name)[0]  # Get station code from file name

    # Insert the station if it doesn't exist
    insert_station(station_code)
    station_id = get_station_id(station_code)  # Get station_id for weather data

    file_records_inserted = 0  # Track records for each file
    with open(f'{wx_data_directory}/{file_name}', 'r') as file:
        for line in file:
            # Split the line by tabs manually
            row = line.strip().split('\t')
            date, max_temp, min_temp, precipitation = row

            # Handle missing values (-9999)
            if max_temp == '-9999':
                max_temp = None
            else:
                max_temp = float(max_temp) / 10  # Convert from tenths of degrees Celsius to degrees Celsius

            if min_temp == '-9999':
                min_temp = None
            else:
                min_temp = float(min_temp) / 10  # Convert from tenths of degrees Celsius to degrees Celsius

            if precipitation == '-9999':
                precipitation = None
            else:
                precipitation = float(precipitation) / 10  # Convert from tenths of mm to mm

            # Insert weather data
            inserted = insert_weather_data(station_id, date, max_temp, min_temp, precipitation)
            file_records_inserted += inserted

    # Log the number of records inserted for this file
    logging.info(f'File {file_name}: {file_records_inserted} new records inserted.')
    total_records_inserted += file_records_inserted

# Log the total number of records inserted
logging.info(f'Total records inserted: {total_records_inserted}')

# Log the end of the process
end_time = datetime.now()
logging.info('Data ingestion process completed.')
logging.info(f'Total duration: {end_time - start_time}')

# Close the connection
cursor.close()
conn.close()
