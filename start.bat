@echo off

If  %1 == up goto:up
If  %1 == down goto:down
If  %1 == abnormalup goto:abnormalup
If  %1 == abnormaldown goto:abnormaldown

:down
  echo "down docker containers of log anticheat..."
  If  %2 == kfek docker-compose -f kafka-docker-compose/docker-compose.yml -f elastic-kibana/docker-compose.yaml -f fluentd/docker-compose.yaml down --volume
  If  %2 == log docker-compose -f python3.7/docker-compose.yaml down --volume
  If  %2 == abnormal docker-compose -f abnormal-log-generator/docker-compose.yaml up -d --build

goto:eof


:up
  echo "start log anticheat..."
  If  %2 == kfek docker-compose -f kafka-docker-compose/docker-compose.yml -f elastic-kibana/docker-compose.yaml -f fluentd/docker-compose.yaml up -d --build
  If  %2 == log docker-compose -f python3.7/docker-compose.yaml up -d --build
  If  %2 == abnormal docker-compose -f abnormal-log-generator/docker-compose.yaml down --volume

goto:eof