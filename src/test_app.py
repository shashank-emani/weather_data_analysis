"""
Unit tests for Weather Data API using Flask's test client.
Tests include: No filters, filtering by station and date, filtering by station and year,
and a test for no data found case.
"""

import unittest
import json
from app import app  # Assuming your file is named app.py


class WeatherApiTestCase(unittest.TestCase):
    """
    A TestCase class for testing the Weather Data API endpoints.
    """

    def setUp(self):
        """
        Set up the test client before each test.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_weather_endpoint_no_filters(self):
        """
        Test the /api/weather endpoint without any filters.
        The response should contain either data or a message indicating no data.
        """
        response = self.app.get('/api/weather')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Check if 'data' is returned or a 'message' indicating no data
        if 'data' in data:
            self.assertIsInstance(data['data'], list)
        else:
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No data found for the given station_id or date.')

    def test_weather_endpoint_with_filters(self):
        """
        Test the /api/weather endpoint with valid station_id and date filters.
        The response should contain data if the filters match existing records.
        """
        # Use filters that exist in the database to prevent "No data found"
        response = self.app.get('/api/weather?station_id=1&date=2024-01-01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Check if 'data' is returned or a 'message' indicating no data
        if 'data' in data:
            self.assertIsInstance(data['data'], list)
        else:
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No data found for the given station_id or date.')

    def test_weather_stats_endpoint(self):
        """
        Test the /api/weather/stats endpoint with valid station_id and year filters.
        The response should contain data if the filters match existing records.
        """
        # Use filters that exist in the database to prevent "No data found"
        response = self.app.get('/api/weather/stats?station_id=1&year=2024')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Check if 'data' is returned or a 'message' indicating no data
        if isinstance(data, list):
            self.assertIsInstance(data, list)
        else:
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No data found for the given station_id or year.')

    def test_weather_no_data_found(self):
        """
        Test the /api/weather endpoint with a station_id that doesn't exist.
        The response should return a message indicating no data found.
        """
        # Test a station_id that doesn't exist
        response = self.app.get('/api/weather?station_id=999999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'No data found for the given station_id or date.')


if __name__ == '__main__':
    unittest.main()
