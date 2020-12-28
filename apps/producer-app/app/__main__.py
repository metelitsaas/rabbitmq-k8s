import time
import json
import pika
import pika.exceptions
from utils.logger import logger
from functions import *

UPDATE_PERIOD = 1  # second

RABBITMQ_HOST = '192.168.99.106'
RABBITMQ_PORT = 32037
RABBITMQ_LOGIN = 'QW5uCWWkLdEkiWcHcLl1vLB-VgjYL0at'
RABBITMQ_PASS = 'XFr5TnE55Nnn_dM6YpecoCykVnjSXiz7'
RABBITMQ_VIRTUAL_HOST = '/'
RABBITMQ_QUEUE = 'person_queue'


def main():

    connection = None

    try:
        credentials = pika.PlainCredentials(RABBITMQ_LOGIN, RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,
                                                                       port=RABBITMQ_PORT,
                                                                       virtual_host=RABBITMQ_VIRTUAL_HOST,
                                                                       credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(RABBITMQ_QUEUE)

        while True:
            data = generate_fake_data()
            channel.basic_publish(exchange='',
                                  routing_key=RABBITMQ_QUEUE,
                                  body=json.dumps(data))
            logger.info(data)
            time.sleep(1)

    except Exception as pika_ex:
        logger.warning(pika_ex)

    finally:
        connection.close()


if __name__ == '__main__':

    try:
        logger.info('Producer application started')
        main()

    except Exception as exception:
        logger.warning(exception)

    finally:
        logger.info('Producer application stopped')
