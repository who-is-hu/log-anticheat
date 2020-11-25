#!/bin/bash

up() {
    echo "start log anticheat..."

    if [ $1 == "kfek" ]; then
        set -x
        docker-compose \
            -f kafka-docker-compose/docker-compose.yml \
            -f elastic-kibana/docker-compose.yaml \
            -f fluentd/docker-compose.yaml \
            up -d --build
        set +x
    elif [ $1 == "log" ]; then
        set -x
        docker-compose \
            -f python3.7/docker-compose.yaml \
            up -d --build
        set +x
    fi    
}

down() {
    echo "down docker containers of log anticheat..."

    if [ $1 == "kfek" ]; then
        set -x
        docker-compose \
            -f kafka-docker-compose/docker-compose.yml \
            -f elastic-kibana/docker-compose.yaml \
            -f fluentd/docker-compose.yaml \
            down --volume
        set +x
    elif [ $1 == "log" ]; then
        set -x
        docker-compose \
            -f python3.7/docker-compose.yaml \
            down --volume
        set +x
    fi
}


if [ $# -ne 2 ]; then
    exit 0
fi

if [ $1 == "up" ]; then
    up $2
elif [ $1 == "down" ]; then
    down $2
fi