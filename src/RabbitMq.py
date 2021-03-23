import pika
from retry import retry

class RabbitMq:
    config = {
    'host': '0.0.0.0',
    'port': 5678,
    'username': 'student',
    'password': 'student',
    'exchange': 'alphapp.direct',
    'routing_key': 'alphapp.routingkey1',
    'queue': 'alphapp.queue'
    }
    credentials = pika.PlainCredentials(config['username'],
    config['password'])
    parameters = (pika.ConnectionParameters(host=config['host']),
    pika.ConnectionParameters(port=config['port']),
    pika.ConnectionParameters(credentials=credentials))

    def on_received_message(self, blocking_channel, deliver, properties, message):
        result = message.decode('utf-8')
        blocking_channel.confirm_delivery()
        try:
            print(result)
            blocking_channel.stop_consuming()
        except Exception as e:
            print(e)
            print("wrong data format")
        finally:
            blocking_channel.stop_consuming()

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def receive_message(self):
        # automatically close the connection
        with pika.BlockingConnection(self.parameters) as connection:
        # automatically close the channel
            with connection.channel() as channel:
                channel.basic_consume(self.config['queue'], self.on_received_message, auto_ack=True)
                try:
                    channel.start_consuming()
                    # Don't recover connections closed by server
                except pika.exceptions.ConnectionClosedByBroker:
                    print("Connection closed by broker.")
                    # Don't recover on channel errors
                except pika.exceptions.AMQPChannelError:
                    print("AMQP Channel Error")
                    # Don't recover from KeyboardInterrupt
                except KeyboardInterrupt:
                    print("Application closed.")

    def clear_queue(self, channel):
        channel.queue_purge(self.config['queue'])