#!/bin/bash
set -e

# Add corporate CA to system trust store
if [ -f /app/certs/corp.crt ]; then
    csplit -sz /app/certs/corp.crt '/-----BEGIN CERTIFICATE-----/' '{*}'
    for cert in xx*; do
        mv "$cert" /usr/local/share/ca-certificates/
    done
    update-ca-certificates

    # Add to Python certifi bundle
    cat /usr/local/share/ca-certificates/*.crt >> $(python -m certifi)
    export REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/corp.crt
fi

# Export .env variables
if [ -f /app/.env ]; then
    export $(grep -v '^#' /app/.env | xargs)
fi

# Run main application
exec python /app/main.py
