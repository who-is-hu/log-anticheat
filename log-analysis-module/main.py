from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import requests
import time

<<<<<<< HEAD
# elasticsearch 서버 정보
es = Elasticsearch("http://localhost:9200")
# es.info()
index = "test"


# kafka setup
bootstrap_servers = ["localhost:9092"]
topic_name = 'parsed-topic'
group_name = 'group1'
consumer = KafkaConsumer(topic_name, 
                        bootstrap_servers=bootstrap_servers, 
                        enable_auto_commit=False,
                        group_id=group_name
                        )

def fetchAll(_index):
    res = es.search(index=_index, body={
        "query":{"match_all":{}}
    })
    docs = []
    for dicto in res['hits']['hits']:
        docs.append(dicto['_source'])
    return docs
    
=======
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

>>>>>>> 39d3df01a0b992fee7e3cad0f9412e454ac93d45
def consume_loop():
    docs = fetchAll('test')
    print(docs)

    while True:
        msg_pack = consumer.poll(timeout_ms=1000)
        for partition_batch in msg_pack.values():
            for msg in partition_batch:
                message = msg.value.decode('utf-8')
                try:
                    json_data = json.loads(message)
                    res = es.index(index=index, doc_type="_doc", body=json_data)
                    print(res)
                except Exception as e:
                    print(e)

<<<<<<< HEAD
        if len(msg_pack) != 0:
            print("========================")
            docs = fetchAll('test')
            print(docs)
=======
def send_json_to_elastic(json_data):
    # test uri
    data_url = f'/test/_doc/{json_data["id"]}'
    uri = elastic_server + data_url
>>>>>>> 39d3df01a0b992fee7e3cad0f9412e454ac93d45

        consumer.commit()

if __name__ == '__main__':
    consume_loop()