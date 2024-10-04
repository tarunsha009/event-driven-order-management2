import redis
from config.settings import REDIS_HOST, REDIS_PORT
from loguru import logger

class InventoryManager:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.initialize_inventory()

    def initialize_inventory(self):
        """Initialize inventory with predefined stock levels."""
        initial_stock = {
            'item1': 100,
            'item2': 50,
            'item3': 200
        }

        # Set initial stock in Redis
        for product, stock in initial_stock.items():
            self.redis_client.set(product, stock)
            logger.info(f"Initialized {product} with stock: {stock}")

    def check_inventory(self, product, quantity):
        """Check if there is enough stock available for the product."""
        stock = self.redis_client.get(product)
        if stock is None:
            logger.error(f"Product {product} not found in inventory.")
            return False
        if int(stock) < quantity:
            logger.error(f"Insufficient stock for product {product}. Requested: {quantity}, Available: {stock}")
            return False
        return True

    def update_inventory(self, product, quantity):
        """Update inventory by reducing the quantity in Redis."""
        current_stock = int(self.redis_client.get(product))
        new_stock = current_stock - quantity
        self.redis_client.set(product, new_stock)
        logger.info(f"Inventory updated for product {product}: New stock is {new_stock}.")
