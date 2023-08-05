## 0.5.2 (2018-10-16)

### Changes

* #28: Callback exchange can be specified in `RpcClient`

## 0.5.1 (2018-09-24)

### Bug fixes

* #25: Remove Content-Type from API headers

## 0.5.0 (2018-09-20)

### Features

* #24: PUT method available for `api`

### Changes

* #19: Body is automatically loaded as JSON in `ProducerClient` callback
* #20: If an exception is raised during callback execution, the error message will be displayed (with no traceback)
* #21: Option to set Pika logging level


## 0.4.1 (2018-08-20)

### Changes

* #12: New `mask` option in for API calls 

## 0.4.0 (2018-08-20)

### Features

* #10: New POST method option in API calls
* #7: New RabbitMQ `ProducerClient`

## 0.3.0 (2018-08-19)

### Features

* #16, #17: Introduction of Contribution guide and Changelog
* #13, #14: PEP8 automatic check & compliance
* #12: New `wait` function for `RpcClient`
* #11: `ConsumerClient` can create a Dead Letter exchange for failure retries

### Fixes

* #9: Fix the behavior of the durable argument in `ConsumerClient`

## 0.2.1 (2018-08-01)

### Fixes

* #8: Add an `exchange_type` parameter to `ConsumerClient` to determine the [type exchange](https://www.rabbitmq.com/tutorials/tutorial-four-python.html) (fanout, direct, topic)

## 0.2.0 (2018-07-31)

### Features

* New `api` function: 
  * Simplify calls to internal REST APIs
  * Status code error handling
  * Logging management
* New `ConsumerClient` class: 
  * Pika client with a blocking connection
  * Bind a queue to an exchange to consume incoming messages

### Changes

*  The default logging level for every Pika client is set to `logging.INFO`

## 0.1.1 (2018-07-23)

### Changes

* `MANIFEST.in` added to `setup.py` process

## 0.1.0 (2018-07-23)

### Features

* `RpcClient` class with context manager, and `call/send` public methods 
* Test suite foundations using [pytest](https://docs.pytest.org/en/latest/) accessible in the `tests/` folder
* Gitlab pipeline introduction: test suite execution, `.tar.gz` distribution package build, deployement to Pypi