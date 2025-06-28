"""
test_fetch_currency_conversion_rates_csv.py

A script to test fetch_currency_conversion_rates_csv.py.

Usage:
    python test_fetch_currency_conversion_rates_csv.py

"""
import unittest
from unittest.mock import patch, MagicMock
import csv
import os
from io import StringIO
import tempfile

# Import the main, save_data_to_csv function from your module
# pylint: disable=E0401
from fetch_currency_conversion_rates_csv import main, save_data_to_csv

# Test cases for code/fetch_currency_conversion_rates_csv.py.
class TestCurrencyConversionRatesCsv(unittest.TestCase):
    """
    Unit tests for the currency conversion rates to csv.

    This class contains tests to validate the behavior of the 
    `save_data_to_csv` function and the main function that 
    stores conversion rates in csv and json.
    """
    @patch('fetch_currency_conversion_rates_csv.save_data_to_csv')
    @patch('fetch_currency_conversion_rates_csv.save_data_to_json')
    @patch('fetch_currency_conversion_rates_csv.fetch_timeseries')
    @patch('fetch_currency_conversion_rates_csv.parse_and_validate_args')
    def test_main_successful_save(self, mock_parse_args, mock_fetch, mock_save_json, mock_save_csv):
        """
        Test that the main function works correctly when the data is valid.
        This includes:
        - Fetching data successfully.
        - Saving the data to both JSON and CSV files.
        Mocks the necessary parts of the code to avoid actual I/O operations.
        """
        # Arrange
        mock_args = MagicMock()
        mock_args.base = 'USD'
        mock_args.symbols = 'EUR,GBP'
        mock_args.start_date = '2023-01-01'
        mock_args.end_date = '2023-01-31'
        mock_args.output_file = 'test_output'

        mock_parse_args.return_value = mock_args
        mock_fetch.return_value = [{
          'date': '2023-01-01',
          'source': 'USD',
          'dest': 'EUR',
          'rate': 0.85
        }]

        # Redirect stdout to capture print statements
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        # Assert
        mock_fetch.assert_called_once()
        mock_save_json.assert_called_once()
        mock_save_csv.assert_called_once()
        self.assertIn("Attempting to save data to test_output json and csv files", output)

    @patch(
      'fetch_currency_conversion_rates_csv.fetch_timeseries',
      side_effect=ValueError("Invalid API response")
    )
    @patch('fetch_currency_conversion_rates_csv.parse_and_validate_args')
    # pylint: disable=W0613
    def test_main_value_error(self, mock_parse_args, mock_fetch):
        """
        Test that the main function raises a ValueError if invalid data is provided.
        Mocks the command-line argument parsing and data fetching functions.
        """
        mock_args = MagicMock()
        mock_args.base = 'USD'
        mock_args.symbols = 'EUR,GBP'
        mock_args.start_date = '2023-01-01'
        mock_args.end_date = '2023-01-31'
        mock_args.output_file = None

        mock_parse_args.return_value = mock_args

        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        self.assertIn("Value Error: Invalid API response", output)

    def test_save_data_to_csv_valid(self):
        """
        Test that the function save_data_to_csv correctly writes data to a CSV file.
        The function should:
        - Generate the correct header based on 'source' and 'dest' currencies.
        - Populate the rows with exchange rates.
        """
        data = [
            {'date': '2023-01-01', 'source': 'USD', 'dest': 'EUR', 'rate': 0.85},
            {'date': '2023-01-01', 'source': 'USD', 'dest': 'GBP', 'rate': 0.75},
            {'date': '2023-01-02', 'source': 'USD', 'dest': 'EUR', 'rate': 0.86},
        ]

        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_csv:
            output_file = temp_csv.name

        try:
            save_data_to_csv(data, output_file)

            # Check file content
            with open(output_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)

            # Assert header and row contents
            expected_header = ['date', 'USD-EUR', 'USD-GBP']
            expected_rows = [
                ['2023-01-01', '0.85', '0.75'],
                ['2023-01-02', '0.86', '']
            ]

            self.assertEqual(rows[0], expected_header)
            self.assertEqual(rows[1:], expected_rows)
        finally:
            os.remove(output_file)

    def test_save_data_to_csv_empty_data(self):
        """
        Test that the function save_data_to_csv raises a ValueError when no data is provided.
        """
        with self.assertRaises(ValueError) as cm:
            save_data_to_csv([], 'dummy.csv')
        self.assertEqual(str(cm.exception), "No data provided to save.")

    def test_save_data_to_csv_invalid_structure(self):
        """
        Test that the function save_data_to_csv raises a ValueError when the data structure
        is invalid. Specifically, the data must be a list of dictionaries containing
        'date', 'source', 'dest', and 'rate' keys.
        """
        bad_data = [{'invalid': 'structure'}]  # Missing keys like 'date', 'source', etc.
        with self.assertRaises(ValueError) as cm:
            save_data_to_csv(bad_data, 'dummy.csv')
        self.assertEqual(
          str(cm.exception),
          "Data must be a list of dictionaries with 'date', 'source', 'dest', and 'rate' keys."
        )

if __name__ == '__main__':
    unittest.main()
