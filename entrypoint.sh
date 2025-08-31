#!/bin/bash
set -e

# If corporate CA certificate exists, add it to the system's trusted certificates
if [ -f /app/certs/corp.crt ]; then
    # split the corp.crt file into individual certificate files
    csplit -sz /app/certs/corp.crt '/-----BEGIN CERTIFICATE-----/' '{*}'

    # move the split certificate files to the system's CA directory
    for cert in xx*; do
        mv "$cert" /usr/local/share/ca-certificates/
    done

    # update the system's trusted certificates
    update-ca-certificates
fi

# export environment variables from .env file if it exists
if [ -f /app/.env ]; then
    export $(grep -v '^#' /app/.env | xargs)
fi

# run the main application
exec python /app/main.py
