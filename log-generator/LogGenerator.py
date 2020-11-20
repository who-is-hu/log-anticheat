from kafka import KafkaProducer
from kafka.errors import KafkaError
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