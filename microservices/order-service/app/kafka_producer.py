from confluent_kafka import Producer
from config.settings import KAFKA_BOOTSTRAP_SERVERS

class KafkaProducerSingleton:
    """Singleton class for Kafka Producer to avoid creating multiple producer instances."""
    _instance = None

    @staticmethod
    def get_instance():
        if KafkaProducerSingleton._instance is None:
            KafkaProducerSingleton._instance = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS, 'socket.timeout.ms': 50000, 'session.timeout.ms': 90000})
        return KafkaProducerSingleton._instance
