# Hotot: RabbitMQ/Requests Python client

**Hotot** is a thin wrapper around [Pika](https://github.com/pika/pika) and [requests](http://docs.python-requests.org/en/master/) to provide: 
* clients that handles connection, publish and receive operations on RabbitMQ without any hassle.
* functions to simplify API calls

Each *service* from the [backend](https://gitlab.lancey.fr/nuage/backend) should use this package to make (a)synchronous requests to internals APIs or brokers.

This package is named after the *(cute)* french rabbit [Blanc de Hotot](https://en.wikipedia.org/wiki/Blanc_de_Hotot). To contribute, please follow the [contributions guidelines](CONTRIBUTING.md).

## How to use


### Installation

Install it with [pip](https://pypi.org/project/pip/). Add `hotot` to your [requirements.txt](https://pip.pypa.io/en/stable/user_guide/#id1) if needed. As easy as pie! 🥧

```
pip install hotot
```


### API calls

With the function `api`, you can construct a new single function to call your API with the right endpoint parameters to make `GET`, `POST` or `PUT` calls. The function assumes that the response can be parsed as a JSON object and will be returned as such. If the request has failed for any reason, the function will return `None`.

``` python
from hotot import api

os.environ['API_ENDPOINT'] = 'localhost'
os.environ['API_PORT'] = '5000'

# api() can detect environment variables 
# or directly uses variables, strings, ints,...
db_api = api('GET', 'API_ENDPOINT', 'API_PORT')
# is equivalent to
db_api = api('GET', 'localhost', 5000)

# the db_api() function has the same parameters as requests.get()
# http://docs.python-requests.org/en/master/user/quickstart/#make-a-request

# curl -X GET "http://localhost:5000/heaters/" -H  "accept: application/json"
print(db_api('heaters')) 

# curl -X GET "http://localhost:5000/frames/main/0?last=1" -H  "accept: application/json"
print(db_api('frames/main/0', params={'last': 1}))

# To make POST calls
post_api = api('POST', 'API_ENDPOINT', 'API_PORT')

# curl -X POST http://localhost:5000/frames/main/new -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" 
print(post_api('frames/main/new', params={'last': 1}))

# To make PUT calls
put_api = api('PUT', 'API_ENDPOINT', 'API_PORT')


# By default, the `api` function will provide logging on the standard output to the `ERROR` level. 
# You can provide our own logger using

import logging

logging.basicConfiglevel(level=logging.INFO)
# Only your imagination limits you
logger = logging.getLogger(__name__)

db_api = api('GET', 'localhost', 5000, logger=logger)
# or 
db_api = api('GET', 'localhost', 5000, logger)

# A mask can be applied to filter the fields returned in the response

print(db_api('heaters'))
print(db_api('heaters', mask='id'))
print(db_api('heaters', mask=['id', 'title']))
# -> [{'id': 1, 'title': 'A', 'body': 'A'}, {'id': 2, 'title': 'B', 'body': 'B'}]
# -> [1, 2]
# -> [{'id': 1, 'title': 'A'}, {'id': 1, 'title': 'B'}]

```


### RPC client

**RpcClient** is a [Remote Procedure Call](https://www.rabbitmq.com/tutorials/tutorial-six-python.html) client.

``` python
from hotot import RpcClient

with RpcClient('localhost') as client:
    
    # Send a RPC with call()
    response = client.call('rpc_queue', a=1, b=2)
    # which is equivalent to
    body = {'a': 1, 'b': 2}
    response = client.call('rpc_queue', **body)
    
    # The send() will not await any response
    client.send('rpc_queue', a=1)

    # Check a response on the callback queue each second for 15 seconds
    response = client.wait(1, 15)

with RpcClient(host, exchange = '', callback_exchange= '', header = {}, timeout=60, connection_attempts=100) as client:
    # host:     the RabbitMQ endpoint
    # exchange: the exchange where the message will be sent
    # callback_exchange: the exchange where the response will be sent (assumed to be of direct type and durable)
    # header:   an optional dict that will be added to the body
    # timeout:  the number of seconds before a call() is considered closed
    # connection_attempts: the number of connexions retries to the host before aborting
    pass
```

The RabbitMQ messages will be sent and received with an `application/json` content type.


### Consumer client

**ConsumerClient** is a synchronous [RabbitMQ consumer](https://www.rabbitmq.com/tutorials/tutorial-three-python.html) client, creating a blocking connection to listen to arriving messages on a exchange.

``` python
with ConsumerClient(host, exchange='', queue='', exchange_type='direct', routing_key=None, exclusive=False, durable=False, retry_ttl=None, max_retries=None, **kwargs) as client:
    # host:             the RabbitMQ endpoint
    # exchange:         the exchange from where the messages are consumed
    # exchange_type:    the exchange type (fanout, direct, topic)
    # queue:            the queue name where the messages are directed, an empty string will define a random name
    # routing_key:      the binding key between the queue and the exchange
    # exclusive:        a boolean flag to set that no others consumers can be feed from this queue
    # durable:          a boolean flag to set that this queue contents may not be destroyed in case of failure
    # retry_ttl:        Number of milliseconds between retries. If 0 or None, no retry strategy.
    # max_retries:      Maximum number of retries
    # connection_attempts: the number of connexions retries to the host before aborting
    # logging_level:    Pika logging level   
    pass
```

To process incoming messages, you have to write a [callback function](https://www.rabbitmq.com/tutorials/tutorial-two-python.html).

* The `body` argument has been automatically converted to a `dict` or `list` object. No need to use `json.loads`.
* If the callback execution is successful, the client will automatically acknowledge the message. No need to use `basic_ack`. * If an exception has been raised during callback execution, an error will be displayed **and the message negatively acknowledge and discarded**.

``` python
def callback(ch, method, properties, body):
    # Do what you want with the received data...
    pass 

client = ConsumerClient(host, 'consumer-exchange', 'consumer-queue')
client.consume(callback) # Blocking function!
```

If the parameter `retry_ttl` is set during initialisation, the client will create a [Dead Letter Exchange](https://www.rabbitmq.com/dlx.html) to intercept failed messages. If a message cannot be treated, raising a `RetryException` will send this message to the DLX which will send back the message to the original queue after waiting for `retry_ttl` milliseconds.

``` python
from hotot import ConsumerClient, RetryException

    def callback(ch, method, properties, body):
        # Code, code, code
        # An error appears!
        # An exception should be raised...
        raise RetryException

client = ConsumerClient(host, 'consumer-exchange', 'consumer-queue', retry_ttl=1000, max_retries=5)
client.consume(callback) # Blocking function!
```

### ProducerClient

**ProducerClient** is a synchronous [RabbitMQ producer](https://www.rabbitmq.com/tutorials/tutorial-three-python.html) client, creating a blocking connection to publish messages on a exchange.

``` python
with ProducerClient(self, host, exchange='', ack_receipt=False, max_retries=None, **kwargs) as client:
    # host:             the RabbitMQ endpoint
    # exchange:         the exchange where the messages are sent
    # ack_receipt:      Check if the message has been persisted onto a queue
    # max_retries:      Maximum number of send retries
    # connection_attempts: the number of connexions retries to the host before aborting  
    # logging_level:    Pika logging level   
    pass
```

The client assumes that the exchange already exists, thus does not declares it.

``` python
client = ProducerClient(host, 'producer-exchange', ack_receipt=True, max_retries=3)

body = {'a': 1, 'b': 2}
client.publish('producer-queue', a=1, b=2)

if client.publish('producer-queue', **body):
    print('Message received by RabbitMQ')
else:
    print('Message not received...')
```

