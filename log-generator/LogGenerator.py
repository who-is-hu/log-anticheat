from kafka import KafkaProducer
from kafka.errors import KafkaError

# 카프카 연결 설정 #
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
##

# 로그 생성 #

##

future = producer.send('log-topic', b'test')

try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    pass

print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)