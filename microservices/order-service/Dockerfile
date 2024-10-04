# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to avoid Python writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to install dependencies
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire order-service codebase into /app directory in the container
COPY . /app/

# Set PYTHONPATH to /app to ensure app module can be found
ENV PYTHONPATH=/app

# Add an additional check to log the structure for debugging
RUN echo "PYTHONPATH is: $PYTHONPATH" && ls /app

# Ensure Kafka and PostgreSQL environment variables are set
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=orders_db
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# Run the application
CMD ["python", "app/order_service.py"]
