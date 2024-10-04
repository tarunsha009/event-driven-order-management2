import json
from loguru import logger
from app.db import SessionLocal, Order, create_tables, engine
from app.kafka_producer import KafkaProducerSingleton
from app.inventory_manager import InventoryManager
import time
from sqlalchemy.exc import OperationalError

# Ensure database tables are created once
create_tables()

class OrderService:
    def __init__(self):
        self.producer = KafkaProducerSingleton.get_instance()
        self.inventory_manager = InventoryManager()
        self.db = SessionLocal()

    def place_order(self, order_id, product, quantity):
        """Place an order if stock is available."""
        if not self.inventory_manager.check_inventory(product, quantity):
            logger.error(f"Insufficient stock for product {product}. Order cannot be placed.")
            return False

        # Create order object
        order = Order(id=order_id, product=product, quantity=quantity)

        # Save order to PostgreSQL and produce to Kafka
        self.save_order_to_db(order)
        self.produce_order_to_kafka(order)

        # Update inventory after placing order
        self.inventory_manager.update_inventory(product, quantity)

        return True

    def save_order_to_db(self, order):
        """Persist the order in PostgreSQL using SQLAlchemy."""
        try:
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            logger.info(f"Order {order.id} saved to database.")
        except Exception as e:
            logger.error(f"Error saving order to database: {e}")
            self.db.rollback()

    def produce_order_to_kafka(self, order):
        """Produce the order to Kafka topic."""
        order_data = {
            "order_id": order.id,
            "product": order.product,
            "quantity": order.quantity
        }
        self.producer.produce('orders', key=str(order.id), value=json.dumps(order_data))
        self.producer.flush()
        logger.info(f"Order {order.id} produced to Kafka topic 'orders'.")


# Kafka Admin Initialization Logic
def initialize_kafka_topics():
    from app.kafka_admin import KafkaAdmin
    kafka_admin = KafkaAdmin()
    kafka_admin.create_topics(['orders', 'validated-orders'])
    kafka_admin.close()
    logger.info("Kafka topics 'orders' and 'validated-orders' initialized successfully.")


# Retry logic for waiting on Postgres
def wait_for_db(engine, retries=5, delay=5):
    while retries > 0:
        try:
            # Try creating a connection to the DB
            conn = engine.connect()
            conn.close()
            return True
        except OperationalError:
            print(f"Database not ready, retrying in {delay} seconds...")
            time.sleep(delay)
            retries -= 1
    raise Exception("Could not connect to the database after several attempts.")


if __name__ == "__main__":
    logger.add("order_service.log", rotation="500 MB")

    # Wait for PostgreSQL to be ready before starting the service
    wait_for_db(engine)

    # Initialize Kafka topics (runs only once)
    initialize_kafka_topics()

    # Start the order service
    order_service = OrderService()

    while True:
        order_id = int(time.time())
        if order_service.place_order(order_id, "item1", 10):
            logger.info("Order placed successfully!")
        else:
            logger.error("Order could not be placed due to insufficient stock.")
        
        # Sleep to avoid tight looping, simulate waiting for a new order
        time.sleep(10)
