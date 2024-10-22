"""
Flask API for retrieving weather data and statistics.
The API supports pagination and allows filtering by station ID and date.
It retrieves data from a PostgreSQL database.
"""

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
import psycopg2

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app, version='1.0', title='Weather Data API',
          description='API for retrieving weather data and statistics.')

# PostgreSQL connection details
conn = psycopg2.connect(
    host="localhost",           # PostgreSQL host
    database="collabery",        # Database name
    user="postgres",             # PostgreSQL username
    password="$ury@003009"       # PostgreSQL password
)
cursor = conn.cursor()


@api.route('/api/weather')
@api.param('station_id', 'Filter by Station ID', required=False)
@api.param('date', 'Filter by Date (YYYY-MM-DD)', required=False)
@api.param('page', 'Page number for pagination', required=False, default=1)
@api.param('per_page', 'Number of results per page', required=False, default=10)
class Weather(Resource):
    """
    API resource for retrieving weather data with pagination and filters.
    Supports filtering by station_id and date.
    """

    def get(self):
        """
        Handles GET requests to fetch weather data based on filters and pagination.
        Returns paginated weather data as JSON or a message if no data is found.
        """
        station_id = request.args.get('station_id')
        date = request.args.get('date')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = "SELECT * FROM weather_data WHERE TRUE"
        params = []

        # Add filters for station_id and date
        if station_id:
            query += " AND station_id = %s"
            params.append(station_id)

        if date:
            query += " AND weather_date = %s"
            params.append(date)

        # Add pagination to the query
        offset = (page - 1) * per_page
        query += f" LIMIT {per_page} OFFSET {offset}"

        try:
            # Execute the query
            cursor.execute(query, tuple(params))
            weather_data = cursor.fetchall()

            # Get the column names from the cursor description
            column_names = [desc[0] for desc in cursor.description]

            # Convert the tuples into dictionaries
            weather_data_dict = [dict(zip(column_names, row)) for row in weather_data]

            # Check if no data was found
            if not weather_data_dict:
                return jsonify({'message': 'No data found for the given station_id or date.'})

            # Return paginated weather data as JSON
            return jsonify({
                'page': page,
                'per_page': per_page,
                'data': weather_data_dict
            })

        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({'message': 'An error occurred while fetching data from the database.'}), 500


@api.route('/api/weather/stats')
@api.param('station_id', 'Filter by Station ID', required=False)
@api.param('year', 'Filter by Year', required=False)
class WeatherStats(Resource):
    """
    API resource for retrieving weather statistics based on station_id and year.
    """

    def get(self):
        """
        Handles GET requests to fetch weather statistics based on station_id and year.
        Returns statistics as JSON or a message if no data is found.
        """
        station_id = request.args.get('station_id')
        year = request.args.get('year')

        query = "SELECT * FROM weather_stats WHERE TRUE"
        params = []

        # Add filters for station_id and year
        if station_id:
            query += " AND station_id = %s"
            params.append(station_id)

        if year:
            query += " AND year = %s"
            params.append(year)

        try:
            # Execute the query
            cursor.execute(query, tuple(params))
            stats_data = cursor.fetchall()

            # Get the column names from the cursor description
            column_names = [desc[0] for desc in cursor.description]

            # Convert the tuples into dictionaries
            stats_data_dict = [dict(zip(column_names, row)) for row in stats_data]

            # Check if no data was found
            if not stats_data_dict:
                return jsonify({'message': 'No data found for the given station_id or year.'})

            # Return the statistics data as JSON
            return jsonify(stats_data_dict)

        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({'message': 'An error occurred while fetching data from the database.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
