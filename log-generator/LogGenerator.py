from kafka import KafkaProducer
from kafka.errors import KafkaError
<<<<<<< HEAD
import random

# 카프카 연결 설정 #
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
##

# 로그 생성 #
'''
1. 유저 이름 입력
2. logData.txt에 저장된 값을 가져온다.
3. 데이터에서 대략 +-5 내에 랜덤으로 1개 생성
'''
while(True) :
    print("Log Data 생성")

    # 유저 이름 입력
    print("user name : ")
    userName = input()

    # logData.txt 읽기
    logDataFile = open("log-generator\logData.txt", "r") # 읽기 모드로 파일을 읽음
    line = logDataFile.readlines() # 파일을 줄단위로 list로 저장

    # log Data 생성
    size = len(line)
    logData = line[random.randrange(0, size)] # random으로 저장된 log 선택
    logDataSplit = logData.split("|") # 읽은 log를 분리
    '''
    0. round
    1. 명중률
    2. 헤드샷
    3. 킬
    4. 데스
    5. 어시
    6. 목숨당 최대 킬수
    7. 시간
    '''
    # log Data random
    logDataSplit[2] = str(int(logDataSplit[2]) + random.randrange(-5,6))
    logDataSplit[3] = str(int(logDataSplit[3]) + random.randrange(-2,3))
    logDataSplit[4] = str(int(logDataSplit[4]) + random.randrange(-2,6))
    if (int(logDataSplit[4]) < 0) : logDataSplit[4] = '0'
    logDataSplit[1] = repr(round((int(logDataSplit[3])*100) / (int(logDataSplit[3]) + int(logDataSplit[4])), 2))
    logDataSplit[5] = str(int(logDataSplit[5]) + random.randrange(-5,6))
    logDataSplit[6] = str(int(logDataSplit[6]) + random.randrange(-5,6))
    if (int(logDataSplit[6]) > int(logDataSplit[3])) : logDataSplit[6] = logDataSplit[3]
    logData = "|".join(logDataSplit)

    log = userName + "|" + logData
    print(log)
##

future = producer.send('log-topic', log)
=======
import time

kafka_connection_check = False
print('start log generator')

# 카프카 연결을 기다림
while kafka_connection_check == False:
    print('try connect kafka...')
    try:
        producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
        kafka_connection_check = True
    except Exception as e:
        print(e)
>>>>>>> 39d3df01a0b992fee7e3cad0f9412e454ac93d45

    time.sleep(3)

a = 1
j = ''

while True:
    try:
        j = f'{{"id":{a}, "text":"bb"}}'
        a = a + 1
        print(f'send to kafka... data: {j}')
        future = producer.send('log-topic', j.encode())

        record_metadata = future.get(timeout=10)

        print (record_metadata.topic)
        print (record_metadata.partition)
        print (record_metadata.offset)
    except Exception as e:
        print(e)

    time.sleep(2)