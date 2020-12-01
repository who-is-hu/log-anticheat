@echo off

If  %1 == up goto:up
If  %1 == down goto:down
If  %1 == abnormalup goto:abnormalup
If  %1 == abnormaldown goto:abnormaldown

:down
  echo "down docker containers of log anticheat..."
  docker-compose -f kafka-docker-compose/docker-compose.yml -f elastic-kibana/docker-compose.yaml -f fluentd/docker-compose.yaml down --volume
  docker-compose -f python3.7/docker-compose.yaml down --volume
goto:eof


:up
  echo "start log anticheat..."
  docker-compose -f kafka-docker-compose/docker-compose.yml -f elastic-kibana/docker-compose.yaml -f fluentd/docker-compose.yaml up -d --build
  docker-compose -f python3.7/docker-compose.yaml up -d --build
goto:eof

:abnormalup
  echo "start abnormal-log-generator..."
  docker-compose -f abnormal-log-generator/docker-compose.yaml up -d --build
goto:eof

:abnormaldown
  echo "down abnormal-log-generator..."
  docker-compose -f abnormal-log-generator/docker-compose.yaml down --volume
goto:eof