#!/bin/bash
set -e

# update CA certificates if custom certificate is provided
if [ -f /usr/local/share/ca-certificates/corp.crt ]; then
    update-ca-certificates
fi

# export environment variables from .env file if it exists
if [ -f /app/.env ]; then
    export $(grep -v '^#' /app/.env | xargs)
fi

# run the main application
exec python /app/main.py