from setuptools import setup

setup(
    name='kafka-python-with-confluent-kafka',
    install_requires=['kafka-python>=1.4', 'confluent-kafka'],
    packages=['kafka_python_with_confluent_kafka'],
    version='0.2',
    description='This python project use to consume/produce/manager the Kafka',
    author='py2k',
    author_email='py2kpy2k@gmail.com',
    url='https://gitlab.com/py2kpy2k/kafka-python-with-confluent-kafka.git',
    download_url='https://gitlab.com/py2kpy2k/kafka-python-with-confluent-kafka/tags/v0.2',
    keywords=['kafka', 'kafka-admin', 'kafka-consumer', 'kafka-producer'],
    classifiers=[],
)
