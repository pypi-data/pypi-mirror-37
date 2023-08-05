import time
import logging

import asyncio
from threading import Thread

import pika


class RabbitMQAsyncClient(object):
    """
    This client will handle rabbit MQ connections, failures and will allow for asynchronous message
    sending and receiving.

    It's supposed to be handy and very simple, so it won't let you create any exchange or channel.

    Based on pika package examples.
    """

    def __init__(self, parameters, on_message_callback, on_channel_callback, log_level=None, log_prefix="[RMQ] "):
        """
        :param pika.ConnectionParameters parameters: Connection parameters
        :param function on_message_callback(text): Function called when a message is received
        :param function on_channel_callback(RabbitMQAsyncClient instance): Function called when connection to RabbitMQ is established and channel is opened
        :param logging logger: Should accept .debug(), .info() and .error() methods (default: python logging)
        :param str log_prefix: A string displayed a the beginning of log message (default: "[RMQ] ")
        """
        self.connection = None
        self.channel = None
        self.closing = False
        self.consuming = False
        self.params = parameters

        fmt = ' '.join((log_prefix, '%(asctime)s - [%(levelname)s] %(message)s'))
        logging.basicConfig(level=log_level if log_level else logging.DEBUG, format=fmt)
        self.log = logging.getLogger(__name__)

        self.rcv_callback = on_message_callback
        self.channel_callback = on_channel_callback

    def connect(self):
        """ Open connection and handle disconnections. """
        self.log.info("Connecting to RabbitMQ server.")
        self.connection = pika.SelectConnection(
            parameters=self.params,
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_error,
            on_close_callback=self.on_connection_closed
        )
        self.run_ioloop_thread()

    def run_ioloop_thread(self):
        self.loop = Thread(target=self.run_ioloop)
        self.loop.start()

    def run_ioloop(self):
        self.connection.ioloop.start()

    def on_connection_open(self, connection):
        """ Open channel when connection is opened. """
        self.log.info("Connection opened.")
        self.open_channel()

    def on_connection_error(self, connection, error):
        """ Called when connection can't be opened. """
        self.log.error("Cannot connect: {}. Retrying in 5s.".format(error))
        self.connection.add_timeout(5, self.connect)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """
        Notify disconnection. We cannot set a timer to reconnect because the ioloop will be stopped.

        :param pika.connection.Connection connection: The closed connection object
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given
        """
        self.channel = None
        self.log.info("Connection closed: ({0}) {1}.".format(reply_code, reply_text))

    def disconnect(self):
        """ Stop ongoing operations and disconnect from RabbitMQ server. """
        self.closing = True
        if self.consuming:
            self.stop_consuming()
        else:
            self.close_channel()
            self.connection.close()

    def open_channel(self):
        self.log.info("Opening a new channel.")
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.log.info("Channel opened.")
        self.channel = channel
        self.channel.add_on_close_callback(self.on_channel_closed)
        if self.channel_callback:
            self.channel_callback(self)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """
        Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Will try to reopen later.

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        self.log.warning("Channel {0} closed: ({1}) {2}. Retrying in 5s.".format(channel.channel_number, reply_code, reply_text))
        self.connection.add_timeout(5, self.open_channel)
        self.channel = None
        self.consuming = False
        # self.connection.close()

    def close_channel(self):
        if self.channel:
            self.channel.close()
            self.log.info("Closing channel.")

    def start_consuming(self, queue):
        """
        Receive incoming messages.

        :param str queue: Queue from which to receive messages
        """
        self.log.info("Now consuming queue {}.".format(queue))
        self.channel.add_on_cancel_callback(self.on_consumer_cancelled)
        self.consumer_tag = self.channel.basic_consume(self.on_message, queue)
        self.consuming = True

    def on_message(self, channel, basic_deliver, properties, body):
        """
        Triggered when a message is received.
        This function is a first filter before calling user callback with less complexity.

        :param pika.channel.Channel channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """
        self.log.debug("Received message '{0}'.".format(body))
        channel.basic_ack(basic_deliver.delivery_tag)
        self.rcv_callback(body)

    def on_consumer_cancelled(self, method_frame):
        """
        Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame
        """
        self.log.info("Consumer was cancelled remotely: {0}.".format(method_frame))
        if self.channel:
            self.channel.close()
        self.consuming = False

    def stop_consuming(self):
        """ Stop receiving incoming messages. """
        if self.channel:
            self.channel.basic_cancel(self.on_cancelok, self.consumer_tag)

    def on_cancelok(self, rabbitmq_cancel_frame):
        """ Triggered when RabbitMQ acknowledges consuming cancelation. """
        self.log.info("Sucessfully canceled consuming.")
        self.consuming = False
        if self.closing:
            self.close_channel()
            self.connection.close()

    def send(self, exchange, key, message):
        """
        Send a message.

        :param str exchange: The exchange
        :param str key: The routing key
        :param str message: The message body (text)

        :return bool: Whether the message was sent or not
        """
        self.log.debug("sending " + str(message))
        if not self.channel:
            self.log.warning("Cannot send message: channel is not opened!")
            return False
        try:
            self.channel.basic_publish(exchange=exchange, routing_key=key, body=message)
            self.log.debug("Sent message '{0}' through exhange {1} with key {2}.".format(message, exchange, key))
            return True
        except pika.exceptions.ConnectionClosed as e:
            self.log.error("Cannot send message: connection is closed. Reconnecting and sending again in 5s.")
            self.connect()
            self.connection.add_timeout(5, self.send, [exchange, key, message])
            pass
        return False

    def on_delivery_confirmation(self, method_frame):
        """
        UNUSED
        Invoked when message destination answers to incoming message.

        :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame
        """
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        self.log.debug(str(method_frame.method.NAME))
        if confirmation_type == 'ack':
            self.log.debug("Message received by destination.")
        elif confirmation_type == 'nack':
            self.log.warning("Message was not received by destination.")
