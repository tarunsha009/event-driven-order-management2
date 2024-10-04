import psycopg2

try:
    connection = psycopg2.connect(
        user="postgres",
        password="mypassword",  # Update with your password
        host="172.18.0.4",
        port="5432",
        database="orders_db"
    )
    print("Database connection successful")
except Exception as error:
    print(f"Error: {error}")
