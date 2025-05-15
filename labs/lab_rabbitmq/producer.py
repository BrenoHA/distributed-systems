import pika

# Conecta ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Cria a fila chamada 'hello'
channel.queue_declare(queue='hello')

# Envia a mensagem "Hello World"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Enviado 'Hello World!'")

connection.close()
