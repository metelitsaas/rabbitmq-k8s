import time
import pika
from pika.exceptions import AMQPConnectionError
from utils.logger import logger

RECONNECT_PERIOD = 1


class RabbitClient:
    """
    RabbitMQ client, realized as singleton
    """
    def __init__(self, host: str, port: str, virtual_host: str, login: str, password: str):
        """
        :param host: RabbitMQ hostname
        :param port: RabbitMQ port
        :param virtual_host: RabbitMQ virtual host
        :param login: RabbitMQ login
        :param password: RabbitMQ password
        """
        self._host = host
        self._port = int(port)
        self._virtual_host = virtual_host
        self._credentials = pika.PlainCredentials(login, password)
        self._connection_params = pika.ConnectionParameters(host=self._host,
                                                            port=self._port,
                                                            virtual_host=self._virtual_host,
                                                            credentials=self._credentials)
        self.channel = None
        self.connect()

    def connect(self) -> pika.connection:
        """
        Connect to RabbitMQ instance and create channel
        Reconnect number of attempts if disconnected, otherwise exit
        :return: RabbitMQ connection
        """
        while True:

            try:
                logger.info(f'Connecting to {self._host}:{self._port}')
                connection = pika.BlockingConnection(self._connection_params)
                self.channel = connection.channel()
                logger.info(f'Connected')
                break

            except AMQPConnectionError as error:
                logger.warning(error)
                logger.warning(f'Unable to connect, reconnecting...')
                time.sleep(RECONNECT_PERIOD)
