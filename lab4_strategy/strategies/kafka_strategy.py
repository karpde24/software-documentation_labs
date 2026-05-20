import json


class KafkaOutputStrategy:
    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic

    def output(self, data):
        from kafka import KafkaProducer

        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda value: json.dumps(value).encode("utf-8")
        )

        producer.send(self.topic, data)
        producer.flush()
        producer.close()

        print(f"Data was written to Kafka topic: {self.topic}")
