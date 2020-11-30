from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from clustering import ClusteringMgr
import json
import time
import requests
import os

print('start analysis module')

print('wait elastic...')
# elasticsearch 서버 정보
es_server = os.getenv('ES_SERVER', "http://localhost:9200")
index = ""
# elastic 연결을 기다림
elastic_connection_check = False
while elastic_connection_check == False:
    try:
        requests.get(es_server)
        elastic_connection_check = True
    except Exception as e:
        print(e)
    time.sleep(3)
es = Elasticsearch(es_server, timeout=30,
                   max_retries=10, retry_on_timeout=True)
print('elastic search connected')

# kafka setup
kafka_server = os.getenv('KAFKA_SERVER', "localhost:9092")
bootstrap_servers = [kafka_server]
topic_name = 'parsed-topic'
group_name = 'group1'

kafka_connection_check = False

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
print('kafka connected')

clusteringMgr = {}


def preprocess(dict_obj):
    # 임시로 uid, rid, timestamp 제거
    dict_obj.pop('user')
    dict_obj.pop('rid')
    dict_obj.pop('time')
    # print(dict_obj)
    return list(dict_obj.values())


def fetchAll(_index):
    res = es.search(index=_index, body={
        "query": {"match_all": {}}
    }, size=1000)
    docs = []
    for record in res['hits']['hits']:
        valueList = preprocess(record['_source'])
        docs.append(valueList)
    # for d in docs:
    #     print(d)
    return docs


def consume_loop(running_mode):
    print("RUNNING :" + running_mode)
    while True:
        try:
            msg_pack = consumer.poll(timeout_ms=500)
            for partition_batch in msg_pack.values():
                for msg in partition_batch:
                    print("===================================")
                    message = msg.value
                    print(message)
                    if running_mode == "DATA_ANALYSIS_MODE":
                        dict_data = json.loads(message)
                        result = clusteringMgr.predictNewData(
                            [preprocess(dict_data)])[0]
                        # if result == 0:
                        #    send to alertmodule
                        dict_data.update({'label': result})
                        print('predict done')
                        jsonformat = json.dumps(dict_data)
                    else:
                        print('just send data for collect')
                        jsonformat = message
                    res = es.index(index=index, doc_type="_doc",
                                   body=jsonformat)
                    print(res)
            consumer.commit()
            time.sleep(1)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # 데이터 분석 모드
    if es.indices.exists(index="source"):
        docs = fetchAll("source")
        for i in docs:
            print(i)
        index = "result"
        mode = "DATA_ANALYSIS_MODE"
        clusteringMgr = ClusteringMgr(docs)
    # 데이터 수집 모드
    else:
        index = "source"
        es.indices.create(index=index)
        mode = "DATA_COLLECT_MODE"
    consume_loop(mode)
