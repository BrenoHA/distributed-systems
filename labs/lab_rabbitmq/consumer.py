import pika

def callback(ch, method, properties, body):
    print(f" [x] Recebido {body.decode()}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Esperando por mensagens. Para sair pressione CTRL+C')
channel.start_consuming()
