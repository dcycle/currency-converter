"""
test_fetch_currency_conversion_rates.py

A script to test fetch_currency_conversion_rates.py.

Usage:
    python test_fetch_currency_conversion_rates.py

"""
import unittest
from unittest.mock import patch, MagicMock
# import sys
from io import StringIO
# pylint: disable=E0401
from fetch_currency_conversion_rates import fetch_timeseries, validate_date, validate_symbols, main

# Test cases for code/fetch_currency_conversion_rates.py.
class TestCurrencyConversionRates(unittest.TestCase):
    """
    Unit tests for the currency conversion rates API.

    This class contains tests to validate the behavior of the 
    `fetch_timeseries` function and its associated functionalities. 
    It checks for successful API responses, error handling for 
    unauthorized requests, and the validation of date and symbol 
    formats. Additionally, it tests the main function that 
    integrates the fetching and displaying of conversion rates.
    """
    def test_fetch_timeseries_success(self):
        """Test that fetch_timeseries handles a successful API response correctly."""
        # Mock response data
        mock_response_data = {
					'meta': {
						'code': 200,
						'disclaimer': 'Usage subject to terms: https://currencybeacon.com/terms'
					},
					'response': {
						'2024-09-01': {'HTG': 131.8400},
						'2024-09-02': {'HTG': 131.8500},
						'2024-09-03': {'HTG': 131.8300},
						'2024-09-04': {'HTG': 131.4700}
					}
        }

        # Mocking the requests.get call to return our mock response
        with patch('fetch_currency_conversion_rates.requests.get') as mock_get:
            mock_get.return_value = MagicMock(
              status_code=200,
              json=lambda: mock_response_data
            )

            # Call the fetch_timeseries function
            base_currency = 'USD'
            symbols = ['HTG']
            start_date = '2024-09-01'
            end_date = '2024-09-04'

            result = fetch_timeseries(base_currency, symbols, start_date, end_date)

            # Check if the function returns the correct formatted response
            expected_result = [
              {'date': '2024-09-01', 'source': 'USD', 'dest': 'HTG', 'rate': 131.8400},
              {'date': '2024-09-02', 'source': 'USD', 'dest': 'HTG', 'rate': 131.8500},
              {'date': '2024-09-03', 'source': 'USD', 'dest': 'HTG', 'rate': 131.8300},
              {'date': '2024-09-04', 'source': 'USD', 'dest': 'HTG', 'rate': 131.4700}
            ]
            self.assertEqual(result, expected_result)

    def test_fetch_timeseries_success2(self):
        """Test that fetch_timeseries handles a successful API response correctly."""
        # Mock response data
        mock_response_data = {
					'meta': {
						'code': 200,
						'disclaimer': 'Usage subject to terms: https://currencybeacon.com/terms'
					},
					'response': 
					{
						'2024-10-22': {'EUR': 0.92574291, 'GBP': 0.77009081}, 
						'2024-10-23': {'EUR': 0.92704996, 'GBP': 0.77363489}, 
						'2024-10-24': {'EUR': 0.9261928, 'GBP': 0.77054473}
					},
					'2024-10-22': {'EUR': 0.92574291, 'GBP': 0.77009081}, 
					'2024-10-23': {'EUR': 0.92704996, 'GBP': 0.77363489}, 
					'2024-10-24': {'EUR': 0.9261928, 'GBP': 0.77054473}
        }

        # Mocking the requests.get call to return our mock response
        with patch('fetch_currency_conversion_rates.requests.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_response_data)

            # Call the fetch_timeseries function
            base_currency = 'USD'
            symbols = ['HTG','GBP']
            start_date = '2024-09-01'
            end_date = '2024-09-04'

            result = fetch_timeseries(base_currency, symbols, start_date, end_date)

            # Check if the function returns the correct formatted response
            expected_result = [
							{'date': '2024-10-22', 'source': 'USD', 'dest': 'EUR', 'rate': 0.9257},
							{'date': '2024-10-22', 'source': 'USD', 'dest': 'GBP', 'rate': 0.7701},
							{'date': '2024-10-23', 'source': 'USD', 'dest': 'EUR', 'rate': 0.927},
							{'date': '2024-10-23', 'source': 'USD', 'dest': 'GBP', 'rate': 0.7736},
							{'date': '2024-10-24', 'source': 'USD', 'dest': 'EUR', 'rate': 0.9262},
							{'date': '2024-10-24', 'source': 'USD', 'dest': 'GBP', 'rate': 0.7705}
            ]
            self.assertEqual(result, expected_result)

    def test_fetch_timeseries_error_401(self):
        """Test that fetch_timeseries raises an exception for unauthorized request."""
        with patch('fetch_currency_conversion_rates.requests.get') as mock_get:
            mock_get.return_value = MagicMock(
                status_code=401, text="Unauthorized - API key missing or incorrect."
            )

            with self.assertRaises(Exception) as context:
                fetch_timeseries('USD', ['HTG'], '2024-09-01', '2024-09-04')
            self.assertTrue(
							'Unauthorized - API key missing or incorrect.' in str(context.exception)
						)

    def test_validate_date(self):
        """Test the validate_date function."""
				# Valid date
        self.assertTrue(validate_date('2024-09-01'))
				# Invalid date (September has 30 days)
        self.assertFalse(validate_date('2024-09-31'))
				# Invalid format
        self.assertFalse(validate_date('09-01-2024'))

    def test_validate_symbols(self):
        """Test the validate_symbols function."""
				# Valid symbol
        self.assertTrue(validate_symbols('HTG'))
				# Valid comma-separated symbols
        self.assertTrue(validate_symbols('HTG,USD'))
				# Invalid symbol (AB is not a 3-letter code)
        self.assertFalse(validate_symbols('HTG,USD,AB'))
				# Invalid format (contains numbers)
        self.assertFalse(validate_symbols('HTG123'))

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', new=[
			'fetch_currency_conversion_rates.py',
			'USD', 
			'HTG',
			'2024-09-01',
			'2024-09-04'
		])
    @patch('fetch_currency_conversion_rates.requests.get')
    def test_main_function(self, mock_get, mock_stdout):
        """Test the main function with mocked inputs and API response."""
        # Mock API response
        mock_response_data = {
            'meta': {
							'code': 200,
							'disclaimer': 'Usage subject to terms: https://currencybeacon.com/terms'
            },
            'response': {
                '2024-09-01': {'HTG': 131.8400}
            }
          }

        mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_response_data)

        # Call the main function
        main()

        # Check the printed output
        expected_output = (
            "[{'date': '2024-09-01', "
            "'source': 'USD', "
            "'dest': 'HTG', "
            "'rate': 131.84}]"
            "\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
