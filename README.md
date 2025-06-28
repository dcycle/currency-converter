# currency-exchange-rates

https://freecurrencyapi.com  don't have free access to historical exchange rates data api.

Hence I am using api from https://currencybeacon.com/ .


* Goto https://currencybeacon.com/register page and Register with basic details.
* Once you registered it will redirect to https://currencybeacon.com/account/dashboard
* Scroll down to API Token Information. Copy Api token.

* We need to access historical exchange rates using timeseries api endpoint	https://api.currencybeacon.com/v1/timeseries by passing below parameters.

    base - Required - The base currency you would like to use for your rates.
    start_date - Required - The start date for the time series you would like to access
    end_date - Required - The end date for the time series you would like to access
    symbols - A list of currencies you will like to see the rates for. You can refer to a list all supported currencies here.

* Follow https://currencybeacon.com/api-documentation for more info.


Api response has disclaimer link.

```
{'meta': {'code': 200, 'disclaimer': 'Usage subject to terms: https://currencybeacon.com/terms'}, 'response': {'2024-10-22': {'HTG': 131.54578724}}, '2024-10-22': {'HTG': 131.54578724} ....}
```

Using format_data method we are extracting response.


** Run exchange rates functionaitlity as below :-

```
./scripts/fetch-currency-conversion-rates.sh <api_key> "https://api.currencybeacon.com/v1" source destinations from_date end_date [app/output_file]
```

```
./scripts/fetch-currency-conversion-rates.sh  <your_api_key>   "https://api.currencybeacon.com/v1" USD EUR,GBP 2023-01-01 2023-01-31 
```

```
./scripts/fetch-currency-conversion-rates.sh  <your_api_key>   "https://api.currencybeacon.com/v1" USD HTG 2023-01-01 2023-01-31 
```

If you want to write output to a json file: 
```
apiKey=<your_api_key>
./scripts/fetch-currency-conversion-rates.sh $apiKey "https://api.currencybeacon.com/v1" USD HTG 2023-01-01 2023-01-31 ./app/unversioned/result.json
```

** RUN tests
```
% ./scripts/test_fetch_currency_conversion_rates.sh
```

Generate currency conversion rates json and csv file.
-----

```
./scripts/fetch-currency-conversion-rates-csv.sh <api_key> "https://api.currencybeacon.com/v1" source destinations from_date end_date [app/output_file]
```

example:-

```
apiKey=<your_api_key>
./scripts/fetch-currency-conversion-rates-csv.sh $apiKey "https://api.currencybeacon.com/v1" USD HTG 2023-01-01 2023-01-31 ./app/unversioned/result
```

Now you will see currency conversion rates output files at ./app/unversioned/result.json and ./app/unversioned/result.csv respectively.

** RUN tests
```
% ./scripts/test_fetch_currency_conversion_rates_csv.sh
```

note:- Mention file name without extension and path as a outputfile, In script while generating json and csv file we appending .json and .csv extension to files respectively.

example:- ./app/unversioned/result

