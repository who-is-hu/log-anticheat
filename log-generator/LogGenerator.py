from kafka import KafkaProducer
from kafka.errors import KafkaError
import random

# 카프카 연결 설정 #
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
##

# 로그 생성 #
'''
1. 정상데이터(1), 비정상데이터(2) 선택
2. 유저 이름 입력
3. logData.txt에 저장된 값을 가져온다.
4. 정상데이터 경우 +-5 내에 랜덤으로 10개 생성 - 일단 안씀
5. 비정상데이터 경우 1개만 생성
'''
while(True) :
    print("Log Data 생성")

    '''
    print("정상데이터 = 1, 비정상 데이터 = 2")
    sel = input()
    '''

#    if(sel == "1") : # 정상데이터 생성
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
    '''
    elif(sel == "2") : # 비정상데이터 생성
    print("user name : ")
    userName = input()

    logDataFile = open("log-generator\logData.txt", "r") # 읽기 모드로 파일을 읽음

    else : # sel이 1, 2 외의 값을 가지면 처음으로 돌아감.
    print("잘못된 값 입력")
    continue
    '''
##

future = producer.send('log-topic', b'test')

try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    pass

print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)