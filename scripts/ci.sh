#!/bin/bash
#
# Run tests on circleci.
#
set -e

echo '=> Run python lint.'
./scripts/python-lint.sh

echo "=> RUN All tests"
./scripts/test_fetch_currency_conversion_rates.sh
./scripts/test_fetch_currency_conversion_rates_csv.sh

echo "** All tests are passed **"
