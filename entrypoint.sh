#!/bin/bash
set -e

# Check and install corporate certificate if it exists
if [ -f /app/certs/corp.crt ]; then
    cp /app/certs/corp.crt /usr/local/share/ca-certificates/corp.crt
    update-ca-certificates

    # Append the corporate certificate to certifi's bundle
    cat /usr/local/share/ca-certificates/corp.crt >> $(python -m certifi)

    export REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/corp.crt
    export CURL_CA_BUNDLE=/usr/local/share/ca-certificates/corp.crt
else
    echo "Warning: /app/certs/corp.crt not found, skipping certificate installation"
fi

exec python /app/main.py
