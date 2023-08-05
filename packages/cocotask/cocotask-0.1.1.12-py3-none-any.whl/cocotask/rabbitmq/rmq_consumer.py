# -*- coding: utf-8 -*-
import pika.exceptions as exceptions
from ..base_consumer import CocoBaseConsumer
from .common import createBlockingConnection
from ..logger import logger
import time


class CocoRMQConsumer(CocoBaseConsumer):

    def __init__(self, conf, worker, logger = None):
        self._exchange_name = conf['EXCHANGE_NAME']
        self._queue_name = conf['QUEUE_NAME']
        self._connection = None
        self._t = None
        super().__init__(conf, worker, logger)

    def connect(self):
        logger.info("CocoRMQConsumer starts working")
        while True:
            logger.info("Trying to connect RabbitMQ server ...")
            try:
                self._connection, channel = createBlockingConnection(self._config)
                break
            except exceptions.AMQPConnectionError as e:
                logger.error("Connect failed, exp: %s" % e)
                logger.debug("Will Try later after 10 seconds...")
                time.sleep(10)

        logger.info("Connected, starts consuming ...")
        channel.queue_bind(exchange=self._exchange_name, queue=self._queue_name)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.on_message, queue=self._queue_name, no_ack=True)
        try:
            channel.start_consuming()
        except exceptions.AMQPConnectionError or exceptions.ChannelError as e:
            logger.error("AMQPConnection or Channel error, exp: %s" % e)
            logger.debug("Trying to reconnect ...")
            self.connect()

        logger.error("Consuming stopped")

    def on_message(self, ch, method, properties, body):
        self._worker.process(body)
