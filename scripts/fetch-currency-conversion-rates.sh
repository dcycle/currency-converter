#!/bin/bash
#
# Run ./fetch_currency_conversion_rates.py in a Docker container
#

set -e

# Function to print error messages in red
print_error() {
   echo -e "\033[31m$1\033[0m"
}

# Check if arguments are provided
if [ $# -lt 6 ]; then
  print_error "Error: Insufficient arguments. Usage: $0 <arg1> <arg2> <arg3> <arg4> <arg5> <arg6> [app/<output_file>]"
  exit 1
fi

mkdir -p unversioned

echo "-- starting docker python instance --"

docker run -v $(pwd):/app --rm --entrypoint /bin/sh -e API_KEY="$1" -e API_ENDPOINT="$2" python:3-alpine -c \
  "pip install requests && python3 /app/scripts/fetch_currency_conversion_rates.py $3 $4 $5 $6 ${7:-}"