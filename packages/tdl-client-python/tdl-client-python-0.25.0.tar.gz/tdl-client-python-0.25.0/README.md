
[![Python Version](http://img.shields.io/badge/Python-2.7-blue.svg)](https://www.python.org/download/releases/2.7/)
[![PyPi Version](http://img.shields.io/pypi/v/tdl-client-python.svg)](https://pypi.python.org/pypi/tdl-client-python)
[![Codeship Status for julianghionoiu/tdl-client-python](https://img.shields.io/codeship/52428c40-5fc8-0133-41cc-5eb6f5612d28.svg)](https://codeship.com/projects/111924)
[![Coverage Status](https://coveralls.io/repos/github/julianghionoiu/tdl-client-python/badge.svg?branch=HEAD)](https://coveralls.io/github/julianghionoiu/tdl-client-python?branch=HEAD)

# tdl-client-python Development

### Submodules

Project contains submodules as mentioned in the `.gitmodules` file:

- broker
- tdl/client (gets cloned into test/features)
- wiremock 

### Getting started

Python client to connect to the central kata server.

Setting up a development environment:
```
pip install tox
pip install coverage
cd tdl-client-python
git submodule update --init
tox -e devenv
```
Your virtualenv will be created in `./devenv/`

Running all the tests,
```
tox
```

Pass arguments to behave, e.g. to run a specific scenario,
```
tox -- -n 'Should not timeout prematurely'
```

# How to use Python virtualenvs

Link: http://www.marinamele.com/2014/05/install-python-virtualenv-virtualenvwrapper-mavericks.html

# Testing

#### Manual 

To run the acceptance tests, start the WireMock servers:
```
python wiremock/wiremock-wrapper.py start 41375
python wiremock/wiremock-wrapper.py start 8222
```

And the broker, with:
```
python broker/activemq-wrapper.py start
```

All test require the ActiveMQ broker to be started.
The following commands are available for the broker.

```
python ./broker/activemq-wrapper.py start
python wiremock/wiremock-wrapper.py start 41375
python wiremock/wiremock-wrapper.py start 8222
```

Run tests with `tox`.

Stopping the above services would be the same, using the `stop` command instead of the `start` command.

#### Automatic (via script)

Start and stop the wiremocks and broker services with the below:
 
```bash
./startExternalDependencies.sh
``` 

```bash
./stopExternalDependencies.sh
``` 

# Cleanup

Stop external dependencies
```
python ./broker/activemq-wrapper.py stop
python wiremock/wiremock-wrapper.py stop 41375
python wiremock/wiremock-wrapper.py stop 8222
```

or

```bash
./stopExternalDependencies.sh
``` 


# To release

Run
```
./release.sh
```
