
# Weather Data Analysis & API Project

## Project Overview
This project processes weather data from multiple stations, analyzes it, and provides an API for retrieving the ingested data and calculated statistics. The project involves:
- **Data ingestion** from raw text files.
- **Transformation/Analysis** to calculate weather statistics.
- **API deployment** to provide access to the ingested and analyzed data.
- **Optional cloud deployment** using AWS or open-source infrastructure.

## Project Structure
```
.
├── app.py                      # Flask API for weather data and stats
├── ingest_weather_data.py       # Script for ingesting weather data into the database
├── analyze_weather_data.py      # Script for calculating yearly weather statistics
├── test_app.py                  # Unit tests for the API
├── Dockerfile                   # Docker configuration for containerization (if applicable)
├── requirements.txt             # Python dependencies
├── data_ingestion.log           # Log file for data ingestion
├── data_analysis.log            # Log file for data analysis
├── README.md                    # Project documentation
└── wx_data/                     # Directory containing weather station data files
```

## Key Components
1. **Data Ingestion**:
   - The script `ingest_weather_data.py` reads weather data from raw text files and inserts it into a PostgreSQL database.
   - Missing or invalid data (e.g., temperatures of `-9999`) is handled during ingestion.

2. **Data Transformation and Analysis**:
   - The script `analyze_weather_data.py` calculates yearly weather statistics such as:
     - Average maximum temperature.
     - Average minimum temperature.
     - Total precipitation (converted to centimeters).
   - These statistics are stored in the database for quick retrieval.

3. **API Deployment**:
   - `app.py` is a Flask-based API providing the following endpoints:
     - `/api/weather`: Retrieves paginated weather data, filtered by station and date.
     - `/api/weather/stats`: Retrieves yearly weather statistics, filtered by station and year.

## Tools and Technologies
- **Python**: Core programming language used for ingestion, transformation, and API development.
- **PostgreSQL**: Database for storing the ingested weather data and calculated statistics.
- **Flask**: Web framework for creating the API.
- **Psycopg2**: PostgreSQL database adapter for Python.
- **Logging**: Logs are generated for both data ingestion and analysis for monitoring and troubleshooting.

## API Endpoints
1. **Weather Data**:
   - **GET `/api/weather`**
     - Parameters:
       - `station_id` (optional): Filter by station ID.
       - `date` (optional): Filter by date (format: YYYY-MM-DD).
       - `page` (optional): Page number for pagination (default: 1).
       - `per_page` (optional): Number of results per page (default: 10).

2. **Weather Statistics**:
   - **GET `/api/weather/stats`**
     - Parameters:
       - `station_id` (optional): Filter by station ID.
       - `year` (optional): Filter by year.

## Setup Instructions
### 1. Prerequisites
- **Python 3.x** installed on your machine.
- **PostgreSQL** installed and running.
- **pip** for installing dependencies.

### 2. Install Dependencies
Run the following command to install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Database Setup
1. Create a PostgreSQL database called `collabery`.
2. Run the following SQL scripts to create the necessary tables:
```sql
CREATE TABLE stations (
    station_id SERIAL PRIMARY KEY,
    station_code VARCHAR(50) UNIQUE
);

CREATE TABLE weather_data (
    weather_id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES stations(station_id),
    weather_date DATE,
    max_temp FLOAT,
    min_temp FLOAT,
    precipitation FLOAT,
    UNIQUE (station_id, weather_date)
);

CREATE TABLE weather_stats (
    station_id INTEGER REFERENCES stations(station_id),
    year INTEGER,
    avg_max_temp FLOAT,
    avg_min_temp FLOAT,
    total_precipitation FLOAT,
    PRIMARY KEY (station_id, year)
);
```

### 4. Ingest Weather Data
To ingest weather data from the `wx_data` folder into the PostgreSQL database, run:
```bash
python ingest_weather_data.py
```

### 5. Analyze Weather Data
To calculate yearly weather statistics and store them in the database, run:
```bash
python analyze_weather_data.py
```

### 6. Run the API
Start the Flask API by running:
```bash
python app.py
```
The API will be available at `http://127.0.0.1:5000`.

### 7. Run Unit Tests
To run the unit tests, execute:
```bash
python -m unittest test_app.py
```

## Cloud Deployment (Optional)
For deployment in the cloud, use the following AWS services:
- **Elastic Beanstalk** or **Lambda + API Gateway** for API deployment.
- **Amazon RDS** for hosting the PostgreSQL database.
- **AWS Lambda** for automating data ingestion and analysis with **CloudWatch Events** for scheduling.

For open-source alternatives, consider using **Docker** and **Kubernetes** for deployment, with **PostgreSQL** hosted on a VPS (e.g., **DigitalOcean**, **Linode**).

## Contact
If you have any questions or need further clarification, feel free to reach out.
