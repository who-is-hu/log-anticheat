If  %1 == up goto:up
If  %1 == down goto:down

:down
echo "down docker containers of log anticheat..."
docker-compose -f kafka-docker-compose/docker-compose.yml -f elastic-kibana/docker-compose.yaml -f fluentd/docker-compose.yaml down
docker-compose -f python3.7/docker-compose.yaml down
goto:eof


:up
echo "start log anticheat..."
docker-compose -f kafka-docker-compose/docker-compose.yml -f elastic-kibana/docker-compose.yaml -f fluentd/docker-compose.yaml up -d --build
docker-compose -f python3.7/docker-compose.yaml up -d --build
goto:eof