#!/bin/bash

start() {
    echo "start log anticheat..."
    set -x
    docker-compose -f kafka-docker-compose/docker-compose.yml -f elastic-kibana/docker-compose.yaml -f fluentd/docker-compose.yaml up -d --build
    set +x
}

down() {
    echo "down docker containers of log anticheat..."
    set -x
    docker-compose -f kafka-docker-compose/docker-compose.yml -f elastic-kibana/docker-compose.yaml -f fluentd/docker-compose.yaml down --volume
    set +x
}


if [ $# -ne 1 ]; then
    exit 0
fi

if [ $1 == "start" ]; then
    start
elif [ $1 == "down" ]; then
    down
fi