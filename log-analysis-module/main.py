from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from clustering import ClusteringMgr
import json
import time

# elasticsearch 서버 정보
es = Elasticsearch("http://localhost:9200")
index = "test"
#es.info()

# kafka setup
# bootstrap_servers = ["localhost:9092"]
# topic_name = 'parsed-topic'
# group_name = 'group1'
# consumer = KafkaConsumer(topic_name, 
#                         bootstrap_servers=bootstrap_servers, 
#                         enable_auto_commit=False,
#                         group_id=group_name
#                         )

clusteringMgr = {}

def preprocess(dict_obj):
    #임시로 uid, rid, timestamp 제거
    dict_obj.pop('user')
    dict_obj.pop('rid')
    dict_obj.pop('time')
    return list(dict_obj.values())
    
def fetchAll(_index):
    res = es.search(index=_index, body={
        "query":{"match_all":{}}
    })
    docs = []
    for record in res['hits']['hits']:
        valueList = preprocess(record['_source'])
        docs.append(valueList)
    # for d in docs:
    #     print(d)
    return docs

def consume_loop():
    while True:
        msg_pack = consumer.poll(timeout_ms=1000)
        for partition_batch in msg_pack.values():
            for msg in partition_batch:
                message = msg.value.decode('utf-8')
                try:
                    dict_data = json.loads(message)
                    result = clusteringMgr.predictNewData(dict_data)
                    #if result == 0:
                    #    send to alertmodule
                    dict_data.update({'label':result})
                    jsonformat = json.dumps(dict_data)
                    res = es.index(index=index, doc_type="_doc", body=jsonformat)
                    print(res)
                except Exception as e:
                    print(e)
        consumer.commit()

if __name__ == '__main__':
    # insert data to ES
    # for i in range(10):
    #     msg = '{"shot_acc":0.67,"headshot_rate":0.33,"kill":%d,"death":3,"assist":4,"max_kill_streak":7,"time":"2000-10-01 13:00:00","rid":"rid01","user":"uid01"}' % (i)
    #     res = es.index(index=index, doc_type="_doc", body=msg)
    #     print(res)    
    
    # test clustering one new data
    clusteringMgr = ClusteringMgr(fetchAll(index))
    print(clusteringMgr.kmeans.labels_)
    msg = '{"shot_acc":0.67,"headshot_rate":0.33,"kill":999,"death":3,"assist":4,"max_kill_streak":7,"time":"2000-10-01 13:00:00","rid":"rid01","user":"uid01"}'
    dicto = json.loads(msg)
    p_data = [preprocess(dicto)] # convert 2d array
    print(p_data)
    result = clusteringMgr.predictNewData(p_data)
    print('label of new data : %d' % (result))

    #consume_loop()