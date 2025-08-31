#!/bin/bash
set -e

# update CA certificates in case custom certs are added
update-ca-certificates

# export environment variables from .env file if it exists
if [ -f /app/.env ]; then
    export $(grep -v '^#' /app/.env | xargs)
fi

# run the main application
exec python /app/main.py