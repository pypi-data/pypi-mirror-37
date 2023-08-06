# -*- coding: utf-8 -*-

import os
import re
import traceback


from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions
from kafka.client import SimpleClient
from kafka.consumer import KafkaConsumer
from kafka.common import OffsetRequestPayload, TopicPartition


class KafkaAdmin:
    def __init__(self):
        pass

    def list_topic(self):
        list = []
        admin_client = self._get_admin_client()
        md = admin_client.list_topics(timeout=10)
        for t in iter(md.topics.values()):
            list.append(str(t))

        return list

    def find_topics_by_regex(self, regex):
        topic_names = []
        admin_client = self._get_admin_client()
        md = admin_client.list_topics(timeout=10)

        for t in iter(md.topics.values()):
            if re.search(regex, str(t)) is not None:
                topic_names.append(str(t))

        print('topics: [%s]' % ', '.join(map(str, topic_names)))
        return topic_names

    def delete_topic(self, topic_name):
        admin_client = self._get_admin_client()
        fs = admin_client.delete_topics([topic_name], operation_timeout=30)

        # Wait for operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} deleted".format(topic))
            except Exception as e:
                print("Failed to delete topic {}: {}".format(topic, e))

    def get_group_lag(self, topic, group):
        broker = os.getenv('KAFKA_BROKERS')
        broker_list = broker.split(",")

        lag = -1
        try:
            topic_offset = self.get_topic_offset(topic, broker_list=broker_list)
            group_offset = self._get_group_offset(broker_list, group, topic)
            lag = topic_offset - group_offset
        except:
            print('Can\'t get sum of lag in topic({}) with group({})'.format(topic, group))

        return lag if lag >= 0 else -1

    def create_topic(self, topic):
        admin_client = self._get_admin_client()

        number_partition = os.getenv('KAFKA_PARTITION_NUMBER')

        if self.is_topic_exist(topic):
            self._create_partitions(topic, number_partition)
        else:
            new_topic = [NewTopic(topic, num_partitions=int(number_partition), replication_factor=1)]

            fs = admin_client.create_topics(new_topic)

            for topic, f in fs.items():
                try:
                    f.result()
                    print("Topic {} created".format(topic))
                except Exception as e:
                    print("Failed to create topic {}: {}".format(topic, e))

    def is_topic_exist(self, topic_name):
        admin_client = self._get_admin_client()
        md = admin_client.list_topics(timeout=10)

        for t in iter(md.topics.values()):
            if str(t) == topic_name:
                return True

        return False

    def _create_partitions(self, topic, new_partition):
        admin_client = self._get_admin_client()

        new_part = [NewPartitions(topic, int(new_partition))]
        fs = admin_client.create_partitions(new_part, validate_only=False)

        # Wait for operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Set partitions({}) to topic {}".format(str(new_partition), topic))
            except Exception as e:
                print("Failed to set partitions({}) to topic {}: {}".format(str(new_partition), topic, e))

    def _get_admin_client(self):
        admin_config = {
            'bootstrap.servers': os.getenv('KAFKA_BROKERS')
        }
        admin_client = AdminClient(admin_config)

        return admin_client

    def get_topic_offset(self, topic, broker_list=None):
        if broker_list is None:
            broker = os.getenv('KAFKA_BROKERS')
            broker_list = broker.split(",")

        client = SimpleClient(broker_list)
        partitions = client.topic_partitions[topic]
        offset_requests = [OffsetRequestPayload(topic, p, -1, 1) for p in partitions.keys()]
        offsets_responses = client.send_offset_request(offset_requests)
        return sum([r.offsets[0] for r in offsets_responses])

    def _get_group_offset(self, brokers, group_id, topic):
        consumer = KafkaConsumer(bootstrap_servers=brokers,
                                 group_id=group_id)
        pts = [TopicPartition(topic=topic, partition=i) for i in
               consumer.partitions_for_topic(topic)]
        result = consumer._coordinator.fetch_committed_offsets(pts)
        return sum([r.offset for r in result.values()])
