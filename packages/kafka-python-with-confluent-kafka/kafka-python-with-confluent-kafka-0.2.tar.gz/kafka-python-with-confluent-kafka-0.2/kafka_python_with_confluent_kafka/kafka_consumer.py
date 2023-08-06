# -*- coding: utf-8 -*-

from confluent_kafka import Consumer
from kafka_python_with_confluent_kafka.kafka_admin import KafkaAdmin


class KafkaConsumer:
    def __init__(self, brokers):
        self.brokers = brokers

    def consume(self, topic_name, group_name, poll_timeout=10):
        # check topic is exist at first
        client = KafkaAdmin(self.brokers)
        if not client.is_topic_exist(topic_name):
            print('Topic: {} not found'.format(topic_name))
            return

        lag = client.get_group_lag(topic_name, group_name)
        if lag == 0:
            print('Topic: {} has no lag.'.format(topic_name))
            return

        config = {
            'bootstrap.servers': self.brokers,
            'group.id': group_name,
            'default.topic.config': {
                'auto.offset.reset': 'smallest'
            }
        }

        consumer = Consumer(config)

        consumer.subscribe([topic_name], on_assign=self._print_assignment)

        try:
            while True:
                msg = consumer.poll(timeout=float(poll_timeout))
                if msg is None:
                    break
                if msg.error():
                    continue
                else:
                    yield msg.value()

        except KeyboardInterrupt:
            pass

        finally:
            consumer.close()

    def _print_assignment(self, consumer, partitions):
        print('Assignment:', partitions)
