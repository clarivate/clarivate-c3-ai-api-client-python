# Clarivate's AI-API

A client interface and sample code for Clarivate's AI-API and the available content sets.

## Description

Clarivate AI API provides a pathway to seek prediction from Clarivate models by passing feature values through API call.
The models and data are always current and always available.

## Getting Started

### Authorization
A valid API KEY is required.
first, you need a valid Clarivate subscription ([Sales enquiries](https://clarivate.com/contact-us/sales-enquiries/)).
then, you need to self-register for an API KEY into our [Clarivate Developer Portal](https://developer.clarivate.com/).

### Dependencies

* Poetry for Python package and environment management

The library is written in python and support python version >= 3.9.0, You can also use [Pyenv](https://github.com/pyenv/pyenv) for this
```
pyenv install 3.9.0
```

To switch current python version then you can execute
```bash
pyenv local 3.9.0
```

* Create a new virtual environment
```bash
python3 -m venv .venv
```

and activate it
```bash
 source <venv>/bin/activate  # POSIX
 <venv>\Scripts\activate.bat  # Windows CMD
 <venv>\Scripts\Activate.ps1  # Windows Powershell
```

Alternatively, you can use Intellij IDEA SDK Management

* Install poetry within virtual environment
```bash
python -m pip install poetry
```

* Install project dependencies
```bash
 poetry install
```

## How to use the library?
### Import

```
from aiapi_client import aiapi
```

### Examples
```
client = aiapi.Client('api key', 'server url')
response, process_logs = client.<endpoint function>('input parameters')
```

Note 1: 'api key' and 'server url' can be directly set into the config.py file.

Note 2: the <endpoint function> are
| Endpoint | Description |
| ----------- | ----------- |
| .info('subscribed dataset') | Returns the description of the subscribed dataset |
| .ontologies('subscribed dataset') | Returns the description of the subscribed dataset |
| .ontology('subscribed dataset', 'ontology name', 'search parameter - optional') | Returns all ontology terms or those matching the search paramaeter |
| .predictions('subscribed dataset') | Returns the list of available predictions |
| predict('prediction', inputs) | Executes a prediction |

Note 3: 'input parameters' depends on the subscribed datase but the pattern is
```
inputs = {
        "model": "model number",
        "inputs": [
        {
            "field": "field name",
            "op": "eq",
            "value": "field value"
        },
        ...
    ]
    }
```

## Help
### Support
* For technical help or questions regarding the repo, you can leave a message into github;
* The Swagger documentation (API endpoints) is available from the dedicated page at [Clarivate Developer Portal](https://developer.clarivate.com/apis/ric-download-api).

### Authors
* © 2024 Clarivate

### License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Version History
### 1.0 - 2024/01/01
    * Initial Release
