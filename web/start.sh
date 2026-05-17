#!/usr/bin/env bash

set -e

echo "Starting Flask application..."
python /app/app.py &

echo "Starting Nginx..."
nginx -g "daemon off;"