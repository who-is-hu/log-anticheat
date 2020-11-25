# 2020 DS

### PREINSTALLATION
    - Docker, Docker Compose
    - Kafka
    - Fluentd
    - ElasticSearch
    - Kibana
    - python 3.7, pip
     
### 로그 생성기


### 분석 모듈


### 알람 모듈


### Kafka


### Fluentd


### Elastic


### 프로젝트 실행
```bash
# kafka, fluentd, elasticsearch, kibana 실행
./start.sh up kfek
# 로그 생성기, 로그 분석 모듈 실행
./start.sh up log
```

### 프로젝트 종료
```bash
# kafka, fluentd, elasticsearch, kibana 종료
./start.sh down kfek
# 로그 생성기, 로그 분석 모듈 종료
./start.sh down log
```
