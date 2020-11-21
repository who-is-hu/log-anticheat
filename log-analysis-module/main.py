from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import requests
import time

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

        if len(msg_pack) != 0:
            print("========================")
            docs = fetchAll('test')
            print(docs)

        consumer.commit()

if __name__ == '__main__':
    consume_loop()