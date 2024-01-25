#!/usr/bin/env bash

echo "Mongo not yet run..."
while ! nc -z mongo 27017; do
  sleep 0.1
done
