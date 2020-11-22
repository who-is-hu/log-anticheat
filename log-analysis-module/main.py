from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from clustering import ClusteringMgr
import json
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

clusteringMgr = {}

def fetchAll(_index):
    res = es.search(index=_index, body={
        "query":{"match_all":{}}
    })
    docs = []
    for dicto in res['hits']['hits']:
        docs.append(dicto['_source'])
    return docs

def consume_loop():
    while True:
        msg_pack = consumer.poll(timeout_ms=1000)
        for partition_batch in msg_pack.values():
            for msg in partition_batch:
                message = msg.value.decode('utf-8')
                try:
                    dict_data = clusteringMgr.preprocess(message)
                    result = clusteringMgr.predictNewData(dict_data)
                    #if result == 0:
                    #    send to alertmodule
                    dict_data.update({'label':result})
                    jsonformat = json.dumps(dict_data)
                    res = es.index(index=index, doc_type="_doc", body=jsonformat)
                    print(res)
                except Exception as e:
                    print(e)

        #if len(msg_pack) != 0:
        #    print("========================")
        #    docs = fetchAll('test')
        #    print(docs)

        consumer.commit()

if __name__ == '__main__':
    # for i in range(100):
    #     msg = '{"shot_acc":0.67,"headshot_rate":0.33,"kill":%d,"death":3,"assist":4,"max_kill_streak":7,"time":"2000-10-01 13:00:00","rid":"rid01","user":"uid01"}' % (i)
    #     res = es.index(index=index, doc_type="_doc", body=msg)
    #     print(res)    
    
    clusteringMgr = ClusteringMgr(fetchAll(index))
    #msg = '{"shot_acc":0.67,"headshot_rate":0.33,"kill":999,"death":3,"assist":4,"max_kill_streak":7,"time":"2000-10-01 13:00:00","rid":"rid01","user":"uid01"}'

    consume_loop()