# Import the 'pika' library for RabbitMQ communication.
import pika

# Parse the AMQP URL to extract connection parameters.
url_params = pika.URLParameters('amqp://rabbit_mq?connection_attempts=10&retry_delay=10')

# Establish a blocking connection to the RabbitMQ server.
connection = pika.BlockingConnection(url_params)

channel = connection.channel()

# Объявляем exchange с типом 'headers'
exchange_name = 'headers_logs'
channel.exchange_declare(exchange=exchange_name, exchange_type='headers')

# Объявляем очередь
queue_name = 'my_headers'
channel.queue_declare(queue=queue_name)

# Создаем привязку (binding) с заданными аргументами заголовков
binding_arguments = {
    'x-match': 'any',  # 'any' означает, что сообщение будет маршрутизировано, если хотя бы один из заголовков совпадает
    'header1': 'value1',  # Пример заголовка и его значения для привязки
}

# Привязываем очередь к exchange с определенными аргументами заголовков
channel.queue_bind(exchange=exchange_name, queue=queue_name, arguments=binding_arguments)

# Задаем заголовки сообщения
headers = {
    'header1': 'value1',  # Пример заголовка и значения для отправляемого сообщения
}

# Текст сообщения для отправки
message = 'This is a message with headers.'

# Публикуем сообщение в exchange с указанными заголовками
channel.basic_publish(exchange=exchange_name, routing_key='', body=message, properties=pika.BasicProperties(headers=headers))

print(f"Sent: '{message}' with ")

# Close the channel.
channel.close()

# Close the connection to RabbitMQ.
connection.close()