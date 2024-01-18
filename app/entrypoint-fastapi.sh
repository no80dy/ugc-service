#!/usr/bin/env bash

MONGODB_INSTANCES=("mongos1:27017" "mongos2:27017")
MAX_ATTEMPTS=30
SLEEP_INTERVAL=5

exponential_backoff() {
    local instance="$1"
    local attempt=0

    while [ $attempt -lt $MAX_ATTEMPTS ]; do
        nc -zv $instance 2>/dev/null

        if [ $? -eq 0 ]; then
            echo "Instance $instance is ready!"
            return 0
        else
            echo "Attempt $((attempt + 1)): Instance $instance not yet reachable. Retrying in $SLEEP_INTERVAL seconds..."
            sleep $SLEEP_INTERVAL
            ((attempt++))
        fi
    done

    echo "Maximum attempts reached for instance $instance. MongoDB cluster is still not fully reachable. Exiting..."
    return 1
}

check_mongodb_cluster() {
    echo "Waiting for MongoDB cluster to be ready..."

    for instance in "${MONGODB_INSTANCES[@]}"; do
        exponential_backoff $instance || return 1
    done

    echo "All MongoDB instances are ready. Starting your service..."
    return 0
}

check_mongodb_cluster && gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
