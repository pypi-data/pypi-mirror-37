# -*- coding: utf-8 -*-

import json
import traceback


from confluent_kafka import Producer
from kafka_python_with_confluent_kafka.kafka_admin import KafkaAdmin


class KafkaProducer:
    def __init__(self, brokers):
        self.producer = None
        self.cache_topics = None
        self.brokers = brokers

    def produce(self, topic_name, push_data, create_topic=False):

        # create topic if necessary
        if create_topic:
            if self.cache_topics is None or len(self.cache_topics) is 0:
                self._update_cache_list()

            # create topic if topic is not exist at first
            if topic_name not in self.cache_topics:
                client = KafkaAdmin(self.brokers)
                client.create_topic(topic_name)  # create topic
                self._update_cache_list()  # update cache

        if self.producer is None:  # load producer at first time
            self.producer = self._get_producer()

        self.producer.produce(topic_name, value=str(json.dumps(push_data)))

    def flush(self):
        if self.producer:
            self.producer.flush()

    def _get_producer(self):
        config = {
            'bootstrap.servers': self.brokers
        }

        producer = Producer(config)
        return producer

    def _update_cache_list(
            self):  # need a lots of cost time for list topic, so use cache list for reducing request time
        client = KafkaAdmin()
        try:
            self.cache_topics = client.list_topic()
        except:
            self.cache_topics = None
            traceback.print_exc()
