# RabbitMQ Lab

This lab demonstrates a basic implementation of RabbitMQ message broker using Python. The project consists of a simple producer-consumer pattern where messages are sent and received through a queue.

## Project Structure

- `producer.py`: A simple message producer that sends "Hello World!" messages to a queue
- `consumer.py`: A message consumer that receives and processes messages from the queue

## Prerequisites

- Python 3.x
- pika library (`pip install pika`)
- Docker (for running RabbitMQ)

## Running the Project

1. Start the RabbitMQ server using Docker:

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

2. Run the consumer in one terminal:

```bash
python consumer.py
```

3. Run the producer in another terminal:

```bash
python producer.py
```

## Accessing the Management Interface

The RabbitMQ management interface is available at:

- URL: http://localhost:15672
- Default credentials: guest/guest
