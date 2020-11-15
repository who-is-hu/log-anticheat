from kafka import KafkaConsumer
from json import loads

bootstrap_servers = ["localhost:9092"]
topic_name = 'parsed-topic'
group_name = 'group1'

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
                print(msg.value.decode('utf-8'))
        consumer.commit()

if __name__ == '__main__':
    consume_loop()