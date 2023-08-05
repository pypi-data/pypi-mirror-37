import sys
import time
import uuid
import json
import pika
import datetime
import itertools

import logging

logging.getLogger('pika').setLevel(logging.INFO)

logger = logging.getLogger('hotot')


class BaseClient(object):
    def __init__(self, host, exchange='', header={}, timeout=60, connection_attempts=100, logging_level=None):
        self.timeout = timeout
        self.exchange = exchange
        self.header = header
        self.response = None

        if logging_level:
            logging.getLogger('pika').setLevel(logging_level)

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                connection_attempts=connection_attempts,
                retry_delay=5
            )
        )

        self.channel = self.connection.channel()

    def _publish(self, routing_key, props, mandatory=False, persistent=False, **kwargs):
        return self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            properties=pika.BasicProperties(**{
                **props,
                **{
                    'content_type': 'application/json',
                    'delivery_mode': 2 if persistent else 1
                }
            }),
            mandatory=mandatory,
            body=json.dumps({**self.header, **kwargs})
        )

    def exit(self):
        self.channel.stop_consuming()
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit()


class RetryException(Exception):
    pass


class StopRetryException(Exception):
    pass


def ack(func):
    def func_wrapper(ch, method, properties, body):
        try:
            func(ch, method, properties, json.loads(body))
            ch.basic_ack(method.delivery_tag)
        except Exception as e:
            logger.error('{}'.format(e))
            ch.basic_reject(method.delivery_tag, requeue=False)
    return func_wrapper


def retry(exchange, max_retries):
    def _retry(func, error):
        def func_wrapper(ch, method, properties, body):
            try:
                json_body = json.loads(body)
                func(ch, method, properties, json_body)
                ch.basic_ack(method.delivery_tag)
            except RetryException:
                ch.basic_reject(method.delivery_tag, requeue=False)
                count = 0
                if properties.headers:
                    count = properties.headers['x-death'][0]['count']
                logger.warning('({}/{}) Rerouting message {} {}'.format(count, max_retries, method.routing_key, body))
                if max_retries and count >= max_retries:
                    error(ch, method, properties, json_body)
                    return
                else:
                    ch.basic_publish(exchange=exchange,
                                     routing_key=method.routing_key,
                                     properties=properties,
                                     body=body)
            except StopRetryException:
                ch.basic_reject(method.delivery_tag, requeue=False)
                error(ch, method, properties, json_body)
                return
        return func_wrapper
    return _retry


def default_callback_max_retries(ch, method, properties, body):
    print('Stop retrying...')


class ConsumerClient(BaseClient):
    def __init__(self,
                 host,
                 exchange='',
                 queue='',
                 exchange_type='direct',
                 routing_key=None,
                 exclusive=False,
                 durable=False,
                 retry_ttl=None,
                 max_retries=None,
                 **kwargs):

        super().__init__(host, exchange, **kwargs)

        self.queue = queue
        self.channel.exchange_declare(self.exchange, exchange_type=exchange_type, durable=durable)
        result = self.channel.queue_declare(queue=self.queue, exclusive=exclusive, durable=durable)
        self.channel.queue_bind(exchange=self.exchange, queue=result.method.queue, routing_key=routing_key)

        self.retry_ttl = retry_ttl
        if self.retry_ttl:
            self.max_retries = max_retries
            self.dlx = 'dlx-' + self.exchange

            self.channel.exchange_declare(self.dlx, exchange_type='fanout', auto_delete=True)
            result = self.channel.queue_declare(
                queue='dlq-' + self.queue,
                auto_delete=True,
                arguments={
                    'x-message-ttl': self.retry_ttl,
                    'x-dead-letter-exchange': self.exchange
                }
            )
            self.channel.queue_bind(exchange=self.dlx, queue=result.method.queue)

    def consume(self, callback, callback_max_retries=None):
        """ Consume messages from queue using a callback """
        if self.retry_ttl:
            if not callback_max_retries:
                callback_max_retries = default_callback_max_retries
            rt = retry(self.dlx, self.max_retries)
            callback = rt(callback, callback_max_retries)
        else:
            callback = ack(callback)

        self.channel.basic_consume(callback, queue=self.queue)
        self.channel.start_consuming()


class ProducerClient(BaseClient):

    def __init__(self, host, exchange='', ack_receipt=False, max_retries=None, **kwargs):
        super().__init__(host, exchange, **kwargs)
        self.ack_receipt = ack_receipt
        self.max_retries = max_retries
        if self.ack_receipt:
            self.channel.confirm_delivery()

    def publish(self, routing_key, **kwargs):
        """ Publish a message on the output exchange """
        if self.ack_receipt:
            retries = range(self.max_retries) if self.max_retries else itertools.repeat(None)
            for _ in retries:
                if self._publish(routing_key, {}, mandatory=True, **kwargs):
                    return True
            return False
        else:
            self._publish(routing_key, {}, **kwargs)


class RpcClient(BaseClient):

    def __init__(self, host, exchange='', callback_exchange='', exchange_type='direct', durable=False, **kwargs):
        super().__init__(host, exchange, **kwargs)
        if self.exchange:
            self.channel.exchange_declare(self.exchange, exchange_type=exchange_type, durable=durable)
        self.callback_exchange = callback_exchange

    def _on_response(self, ch, method, props, body):
        """ Filter incoming responses on correlation ID """
        if not(hasattr(self, 'corr_id')) or self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def _wait(self, frequency=0, timeout=None):
        """ Check for a response at a specific frequency during a defined duration """
        t_end = time.time() + (timeout if timeout else self.timeout)
        while self.response is None:
            time.sleep(frequency)
            if time.time() > t_end:
                break
            self.connection.process_data_events()

    def _open_callback(self, queue=''):
        """ Declare and start the callback queue if needed
            If no queue name is provided, a random name is chosen and the queue is exclusive
        """
        if not hasattr(self, 'callback_queue'):
            if self.callback_exchange:
                self.channel.exchange_declare(self.callback_exchange, exchange_type='direct', durable=True)
  
            result = self.channel.queue_declare(queue=queue, exclusive=not(bool(queue)))
            self.callback_queue = result.method.queue
      
            if self.callback_exchange:
                self.channel.queue_bind(
                    exchange=self.callback_exchange,
                    queue=self.callback_queue,
                    routing_key=self.callback_queue
                )

            self.channel.basic_consume(
                self._on_response,
                no_ack=True,
                queue=self.callback_queue
            )

    def call(self, routing_key, **kwargs):
        """ Publish a message and await for the response """
        self.response = None
        self._open_callback()

        self.corr_id = str(uuid.uuid4())

        self._publish(
            routing_key, {
                'reply_to': self.callback_queue,
                'correlation_id': self.corr_id
            }, **kwargs)

        self._wait()
        return self.response

    def send(self, routing_key, **kwargs):
        """ Publish a message on the output exchange without a waiting block """
        return self._publish(routing_key, {}, **kwargs)

    def wait(self, frequency=0, timeout=None):
        """ Wait for a response on the callback queue """
        self.response = None
        self._wait(frequency, timeout)
        return self.response
