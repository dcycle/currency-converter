"""
fetch_currency_conversion_rates_csv.py

A script to fetch data from the API_ENDPOINT using API_KEY and store it in json and csv file if
provided in arguments to fetch_currency_conversion_rates_csv.py.

You have to set environment variable API_KEY, API_ENDPOINT before executing code.

Usage:
    python fetch_currency_conversion_rates_csv.py
      <base> <symbols> <start_date> <end_date> <api_key> <api_endpoint> [<output_file>]

Arguments:
    base (str): Source Currency Code.
    symbols (list): Comma Separated Destination Currency Codes.
    start_date (Date): From Date.
    to_date (Date): To Date.
    output_file (str): The path to the output JSON and CSV file.

For example:-
    You can run this inside python:3-alpine container 

    $ export API_KEY="$1" 
    $ export API_ENDPOINT="$2"     
    $ pip install requests && python3 /app/scripts/fetch_currency_conversion_rates_csv.py \
      USD HTG,XOF,CAD,EUR 2025-03-01 2025-05-31 ./app/unversioned/result
"""
import os
import csv
from collections import defaultdict, OrderedDict
# pylint: disable=E0401
from fetch_currency_conversion_rates import (
    fetch_timeseries,
    save_data_to_json,
    UnauthorizedError,
    parse_and_validate_args
)

def save_data_to_csv(data, output_file):
    """
    Saves the provided data to a specified csv file.

    Parameters:
    - data (list): The data to be saved, typically a list of dictionaries.
    - output_file (str): The path to the output csv file.

    Raises:
    - IOError: If there is an issue writing to the file.
    """
    if not data:
        raise ValueError("No data provided to save.")

    if not isinstance(data, list) or not all(
        isinstance(item, dict) and {'date', 'source', 'dest', 'rate'}.issubset(item)
        for item in data
    ):
        raise ValueError(
            "Data must be a list of dictionaries with "
            "'date', 'source', 'dest', and 'rate' keys."
        )

    # Ordered sets using dicts to preserve order
    seen_dates = OrderedDict()
    seen_pairs = OrderedDict()
    pivoted_data = defaultdict(dict)

    for row in data:
        date = row['date']
        pair = f"{row['source']}-{row['dest']}"
        rate = row['rate']

        seen_dates.setdefault(date, None)
        seen_pairs.setdefault(pair, None)
        pivoted_data[date][pair] = rate

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['date'] + list(seen_pairs.keys())
        writer.writerow(header)

        for date in seen_dates.keys():
            row = [date] + [pivoted_data[date].get(pair, '') for pair in seen_pairs]
            writer.writerow(row)
        print(f"Data saved to {output_file}")

# Main function
def main():
    """
    The main function that parses command-line arguments, validates them, and fetches
    the currency exchange rates from the CurrencyBeacon API.
    """
    # pylint: disable=R0801
    args = parse_and_validate_args()

    # Fetch data from CurrencyBeacon API
    try:
        symbols_list = args.symbols.split(',')
        data = fetch_timeseries(args.base, symbols_list, args.start_date, args.end_date)
        if args.output_file:
            print(f"Attempting to save data to {args.output_file} json and csv files")
            save_data_to_json(data, args.output_file + '.json')
            save_data_to_csv(data, args.output_file + '.csv')
    # pylint: disable=R0801
        else:
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

# pylint: disable=R0801
if __name__ == "__main__":
    main()
