# Contribution guidelines


## Release & Development version

All your code should be deployed on the `dev` branch using this scenario:
* Choose an [issue](https://gitlab.lancey.fr/nuage/hotot/issues)
* Create a branch starting with the issue number
* Commit your code 
* Push the feature branch on Gitlab
* Create a [new merge request](https://gitlab.lancey.fr/nuage/hotot/merge_requests/new)
* If needed, continue to iterate on the same branch
* When the branch has been approved and merged, delete your local version

Only maintainers can merge on the `dev` and `master` branches and creates tags.

Each release is automatically uploaded to [PyPI](https://pypi.org/project/hotot/#history) for every tagged commit on the `master` branch. The tag version must be [PEP400](https://www.python.org/dev/peps/pep-0440/) compliant, and have not been already used for any previous *(even deleted)* release.

In case you need to try the deployement without publishing on PyPI, you can upload the build on [the test version of PyPI](https://test.pypi.org/project/hotot) and create a virtualenv to try to download and install it:

```
pip install twine
VERSION=1.0 python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
virtualenv py3
source py3/bin/activate
pip install --extra-index-url https://test.pypi.org/simple hotot==1.0dev
```

With `$VERSION`, you specify a version number (not already used for any previous *- even deleted -* release). A `dev` will be automatically appended to the version number.


## Style guide

The code style should be [PEP8](https://www.python.org/dev/peps/pep-0008/) compliant and is tested during the CI. To test your code before committing, you can use:

```
pip install pycodestyle
pycodestyle --statistics --ignore=E501 --filename=*.py
```

## Test suite

A test suite is available in `tests/`. Every new commit to the repo will automatically trigger a new [test suite pipeline](https://gitlab.lancey.fr/nuage/hotot/pipelines). Adding or modifying a *Hotot* feature should add new tests or modify the related ones. **A new release will be only deployed if the pipeline status is green**.

The suite uses [pytest](https://docs.pytest.org/en/latest/) as its main framework. If you want to launch the test suite locally, you need to launch our own instance of RabbitMQ before firing up the suite (or a single test):

```
pip install pytest
docker run -p 5672:5672 -p 15672:15672 -d rabbitmq:3.7-rc-management

python setup.py test
pytest tests/test_consumer.py -s -k 'test_retry'
```