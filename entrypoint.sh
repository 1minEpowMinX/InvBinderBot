#!/bin/bash
set -e

CERT_PATH="${CORP_ROOT_CA_PATH:-/app/certs/corp_root_ca.crt}"

# Check and install corporate root certificate if it exists
if [ -f "$CERT_PATH" ]; then
    cp "$CERT_PATH" /usr/local/share/ca-certificates/corp_root_ca.crt
    update-ca-certificates

    # Append the corporate root certificate to certifi's bundle
    cat /usr/local/share/ca-certificates/corp_root_ca.crt >> $(python -m certifi)

	export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
    export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
    export CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

	echo "Installed $CERT_PATH as a trusted certificate"
else
    echo "Warning: $CERT_PATH not found, skipping certificate installation"
fi

exec python /app/main.py
