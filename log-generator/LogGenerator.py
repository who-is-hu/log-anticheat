from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
import random
import json
import os

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

    time.sleep(3)

# 로그 생성 #
'''
0. 유저 이름과 아이디는 임의로 들어감
1. logData.txt에 저장된 값을 가져온다.
2. 데이터에서 대략 +-5 내에 랜덤으로 1개 생성
'''
# log data Json format
logFormat = {
    'user': {
        'uid' : 'uid01',
        'name' : 'name',
        'rank' : 1
    },

    'round' : {
        'rid' : 'rid01',
        'r_starttime' : '2000-10-00 12:00:00',
        'r_endtime' : '2000-10-00 13:00:00'
    },

    'shot_acc' : 67.00,
    'headshot_rate' : 20.00,
    'kill' : 10,
    'death' : 3,
    'assist' : 4,
    'max_kill_streak' : 7,
    'time' : '2000-10-00 13:00:00'
}

while(True) :
    print("Log Data 생성")

    # logData.txt 읽기
    logfiledir = os.getenv("LOG_FILE_DIR", "log-generator")
    logDataFile = open(os.path.join(logfiledir, "logData.txt"), "r") # 읽기 모드로 파일을 읽음
    line = logDataFile.readlines() # 파일을 줄단위로 list로 저장

    # log Data 생성
    size = len(line)
    logData = line[random.randrange(1, size)] # 저장된 log random 선택, 0번째 줄은 순서를 써둔것이라 무시
    logDataSplit = logData.split("|") # 읽은 log를 분리
    '''
    0. rank = user->rank
    1. rid = round->rid
    2. start time = round->r_starttime
    3. end time = round->r_endtime
    4. 명중률 = shot_acc
    5. 헤드샷 = headshot_rate
    6. 킬 = kill
    7. 데스 = death
    8. 어시 = assist
    9. 목숨당 최대 킬수 = max_kill_streak
    10. 시간 = time
    '''
    for i in range(0,10) :
        # log Data random create
        logFormat['user']['uid'] = 'ID0' + i
        logFormat['user']['name'] = 'Name0' + i
        logFormat['user']['rank'] = int(logDataSplit[0])
        logFormat['round']['rid'] = logDataSplit[1]
        logFormat['round']['r_starttime'] = logDataSplit[2]
        logFormat['round']['r_endtime'] = logDataSplit[3]
        logFormat['headshot_rate'] = int(logDataSplit[5]) + random.randrange(-5,6)
        logFormat['kill'] = int(logDataSplit[6]) + random.randrange(-2,3)
        logFormat['death'] = int(logDataSplit[7]) + random.randrange(-2,6)
        logFormat['shot_acc'] = round((logFormat['kill']*100) / (logFormat['kill'] + logFormat['death']), 2)
        logFormat['assist'] = int(logDataSplit[8]) + random.randrange(-5,6)
        logFormat['max_kill_streak'] = int(logDataSplit[9]) + random.randrange(-5,6)
        logFormat['time'] = logDataSplit[10]

        # random data range error handling
        if (logFormat['headshot_rate'] < 0) : logFormat['headshot_rate'] = 0            
        if (logFormat['kill'] < 0) : logFormat['kill'] = 0            
        if (logFormat['death'] < 0) : logFormat['death'] = 0
        if (logFormat['assist'] < 0) : logFormat['assist'] = 0
        if (logFormat['max_kill_streak'] > logFormat['kill']) : logFormat['max_kill_streak'] = logFormat['kill']
        
        logJson = json.dumps(logFormat)
        print(logJson)
        print(type(logJson))

    # 카프카 실행
        print('send to kafka...')
    try:                    
            future = producer.send('log-topic', logJson)

            record_metadata = future.get(timeout=10)

            print (record_metadata.topic)
            print (record_metadata.partition)
            print (record_metadata.offset)

            time.sleep(2)
            
    except Exception as e:
        print(e)

    time.sleep(3)

# 계속되는 실행을 막기위해 5분에 한번씩 10번 보냄
time.sleep(300)