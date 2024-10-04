from confluent_kafka.admin import AdminClient, NewTopic
from config.settings import KAFKA_BOOTSTRAP_SERVERS
from loguru import logger

class KafkaAdmin:
    def __init__(self):
        self.admin_client = AdminClient({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS, 'socket.timeout.ms': 50000, 'session.timeout.ms': 90000})

    def create_topics(self, topics):
        """Create Kafka topics if they don't exist."""
        topic_list = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]
        futures = self.admin_client.create_topics(topic_list)

        for topic, future in futures.items():
            try:
                future.result()  # Wait for topic creation to complete
                logger.info(f"Topic '{topic}' created successfully.")
            except Exception as e:
                logger.warning(f"Failed to create topic '{topic}': {e}")

    def close(self):
        """Close the admin client connection."""
        logger.info("Kafka Admin Client closed.")
