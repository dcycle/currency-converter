#!/bin/bash
#
# Lint Python script.
# See https://github.com/dcycle/docker-python-lint.
#
set -e

echo "Linting Python with https://github.com/dcycle/docker-python-lint"
echo ""
echo "To ignore a warning, place a comment before the offending line:"
echo ""
echo "# pylint: disable=E0401"
echo ""
docker run --rm -v $(pwd)/scripts:/app/code dcycle/python-lint:2 ./code
