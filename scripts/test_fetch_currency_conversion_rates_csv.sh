echo "-- starting docker python instance --"

docker run -v $(pwd):/app --rm --entrypoint /bin/sh -e API_KEY="$1" -e API_ENDPOINT="$2" python:3-alpine -c \
  "pip install requests && python3 /app/scripts/test_fetch_currency_conversion_rates_csv.py"