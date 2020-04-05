#!/usr/bin/env bash

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 3
done

nameko run --config config.yml tweets.service
