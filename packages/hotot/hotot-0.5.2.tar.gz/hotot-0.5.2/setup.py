import os
import setuptools

with open('INFO.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name=os.environ.get('CI_PROJECT_NAME', 'hotot'),
    version=os.environ.get('CI_COMMIT_TAG', os.environ.get('VERSION', '') + 'dev'),
    author='Lancey Energy Storage',
    description='RabbitMQ/Pika Python client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=os.environ.get('CI_PROJECT_URL', ''),
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'License :: Public Domain'
    ),
    install_requires=['pika', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
