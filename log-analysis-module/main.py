from kafka import KafkaConsumer
from json import loads
import requests

bootstrap_servers = ["localhost:9092"]
topic_name = 'parsed-topic'
group_name = 'group1'

# elasticsearch 서버 정보
elastic_server = 'http://localhost:9200'

consumer = KafkaConsumer(topic_name, 
                        bootstrap_servers=bootstrap_servers, 
                        enable_auto_commit=False,
                        group_id=group_name
                        )
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
    data_url = '/test/_doc/1'
    uri = elastic_server + data_url

    res = requests.put(uri, json=json_data)
    print(res.json())

if __name__ == '__main__':
    consume_loop()