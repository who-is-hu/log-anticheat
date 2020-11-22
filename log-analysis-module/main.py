from kafka import KafkaConsumer
from json import loads
import requests
import time

bootstrap_servers = ["kafka:9092"]
topic_name = 'parsed-topic'
group_name = 'group1'

# elasticsearch 서버 정보
elastic_server = 'http://es01:9200'


kafka_connection_check = False
elastic_connection_check = False
print('start analysis module')
print('wait elastic...')
# elastic 연결을 기다림
while elastic_connection_check == False:
    try:
        requests.get(elastic_server)
        elastic_connection_check = True
    except Exception as e:
        print(e)
    time.sleep(3)

# 카프카 연결을 기다림
while kafka_connection_check == False:
    print('try connect kafka...')
    try:
        consumer = KafkaConsumer(topic_name,
            bootstrap_servers=bootstrap_servers, 
            enable_auto_commit=False,
            group_id=group_name)
        
        kafka_connection_check = True
    except Exception as e:
        print(e)
    
    time.sleep(3)

def consume_loop():
    while True:
        msg_pack = consumer.poll(timeout_ms=500)

        for partition_batch in msg_pack.values():
            for msg in partition_batch:
                message = msg.value.decode('utf-8')
                print(message)
                json_data = loads(message)
                send_json_to_elastic(json_data)
        consumer.commit()

def send_json_to_elastic(json_data):
    # test uri
    data_url = f'/test/_doc/{json_data["id"]}'
    uri = elastic_server + data_url

    res = requests.put(uri, json=json_data)
    print(res.json())

if __name__ == '__main__':
    consume_loop()