"""
fetch_currency_conversion_rates.py

A script to fetch data from fetch_currency_conversion_rates.py.

You have set environment variable API_KEY, API_ENDPOINT before executing code.

Usage:
    python fetch_currency_conversion_rates.py
      <base> <symbols> <start_date> <end_date> <api_key> <api_endpoint>

Arguments:
    base (str): Source Currency Code.
    symbols (list): Destination Currency Codes.
    start_date (Date): From Date.
    to_dend_dateate (Date): To Date.
    api_key(str): Authorized Api key.
    api_endpoint(str): Currency Exchange provider api.
"""
import os
import sys
from datetime import datetime
import argparse
# pylint: disable=E0401
import requests


class APILimitExceededError(Exception):
    """Exception raised when the API limit is exceeded."""

class UnauthorizedError(Exception):
    """Exception raised for unauthorized access due to incorrect API key."""

class UnprocessableEntityError(Exception):
    """Exception raised for invalid parameters."""

class InternalServerError(Exception):
    """Exception raised for internal server errors."""

class ServiceUnavailableError(Exception):
    """Exception raised when the service is unavailable."""

class UnexpectedError(Exception):
    """Exception raised for unexpected errors."""

# Function to make the API request
def fetch_timeseries(base, symbols, start_date, end_date):
    """
    Fetches the historical currency exchange rates from the CurrencyBeacon API.

    Parameters:
    - base (str): The base currency code (e.g., "USD").
    - symbols (list): A list of target currency codes (e.g., ["EUR", "GBP"]).
    - start_date (str): The start date for the timeseries in YYYY-MM-DD format.
    - end_date (str): The end date for the timeseries in YYYY-MM-DD format.

    Returns:
    - dict: The JSON response from the API containing the exchange rates.

    Raises:
    - Exception: If there is an error in the API request, an exception is raised.
    """
    api_key = os.getenv("API_KEY")
    endpoint = os.getenv("API_ENDPOINT")

    # Prepare the request URL
    url = f"{endpoint}/timeseries"
    params = {
        'base': base,
        'start_date': start_date,
        'end_date': end_date,
        'symbols': ','.join(symbols),
        'api_key': api_key
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Handle response
    if response.status_code == 200:
        return format_data(base, response)

    if response.status_code == 401:
        raise UnauthorizedError("Unauthorized - API key missing or incorrect.")
    if response.status_code == 422:
        raise UnprocessableEntityError("Unprocessable Entity - Check your parameters.")
    if response.status_code == 500:
        raise InternalServerError("Internal Server Error.")
    if response.status_code == 503:
        raise ServiceUnavailableError("Service Unavailable - Try again later.")
    if response.status_code == 429:
        raise APILimitExceededError("Too many requests - API limits reached.")

    raise UnexpectedError(f"Unexpected error: {response.status_code} - {response.text}")

# Function format the response
def format_data(base, response):
    """
    Function format the response return from api.

    Parameters:
    - base (str): Base currency code.
    - response (object): Response return from api.

    Returns:
    - list: formatted response.
    """

    formatted_data = []
    for date, rates in response.json()['response'].items():
        for symbol, rate in rates.items():
            formatted_data.append({
                'date': date,
                'source': base,
                'dest': symbol,
                'rate': round(rate, 4)  # rounding to 4 decimal places for consistency
            })
    # print(formatted_data)
    return formatted_data

# Function to validate date format (YYYY-MM-DD)
def validate_date(date_str):
    """
    Validates if the date string is in the format YYYY-MM-DD.

    Parameters:
    - date_str (str): The date string to validate.

    Returns:
    - bool: True if the date string is in valid format, otherwise False.
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Function to validate currency symbols
def validate_symbols(symbols):
    """
    Validates if the currency symbols are provided as a comma-separated list.

    Parameters:
    - symbols (str): A comma-separated list of currency codes.

    Returns:
    - bool: True if the symbols are valid, otherwise False.
    """
    if symbols:
        valid_symbols = symbols.split(',')
        if all(symbol.isalpha() and len(symbol) == 3 for symbol in valid_symbols):
            return True
    return False

# Main function
def main():
    """
    The main function that parses command-line arguments, validates them, and fetches
    the currency exchange rates from the CurrencyBeacon API.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch historical currency exchange rates")
    parser.add_argument('base', help="The base currency for the rates (e.g., USD)")
    parser.add_argument('symbols', help="Comma-separated list of target currencies (e.g., EUR,GBP)")
    parser.add_argument(
      'start_date',
      help="Start date for the timeseries in YYYY-MM-DD format (e.g., 2023-01-01)"
    )
    parser.add_argument(
      'end_date',
      help="End date for the timeseries in YYYY-MM-DD format (e.g., 2023-01-31)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not validate_date(args.start_date):
        print(f"Error: Invalid start date format: {args.start_date}. Expected format: YYYY-MM-DD.")
        sys.exit(1)

    if not validate_date(args.end_date):
        print(f"Error: Invalid end date format: {args.end_date}. Expected format: YYYY-MM-DD.")
        sys.exit(1)

    if not validate_symbols(args.symbols):
        print("Error: Invalid currency symbols: " + args.symbols)
        print("Each symbol must be a 3-letter code separated by commas (e.g., EUR,GBP).")
        sys.exit(1)

    # Fetch data from CurrencyBeacon API
    try:
        symbols_list = args.symbols.split(',')
        data = fetch_timeseries(args.base, symbols_list, args.start_date, args.end_date)
        print(data)
    except ValueError as ve:
        print("Value Error: " + str(ve))
    except KeyError as ke:
        print("Key Error: " + str(ke))
    except UnauthorizedError as ue:
        print("Unauthorized: " + str(ue))
    # Add more specific exceptions as needed
    # pylint: disable=W0718
    except Exception as e:  # This can still be used to catch unexpected errors
        print("Unexpected Error: " + str(e))

if __name__ == "__main__":
    main()
