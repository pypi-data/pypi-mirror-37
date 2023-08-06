# Chargehound python bindings 

[![Build Status](https://travis-ci.org/chargehound/chargehound-python.svg?branch=master)](https://travis-ci.org/chargehound/chargehound-python) [![PyPI version](https://badge.fury.io/py/chargehound.svg)](https://badge.fury.io/py/chargehound)

## Installation

`pip install chargehound`

## Usage

Import chargehound and set your API key.

```python
import chargehound
chargehound.api_key = '{ YOUR_API_KEY }'
```

### Requests

Every resource is accessed via the Chargehound module.

```python
dispute = chargehound.Disputes.submit('dp_123', fields={'customer_name': 'Susie'})
```

### Response

Responses from the API are automatically parsed from JSON and returned as Python objects.

Responses also include the HTTP status code on the response object as the status field.

```python
dispute = chargehound.Disputes.retrieve('dp_123')

print dispute.state
# 'needs_response'
print dispute.response.status
# 200
```

## Documentation

[Disputes](https://www.chargehound.com/docs/api/index.html?python#disputes)

[Errors](https://www.chargehound.com/docs/api/index.html?python#errors)

## Development

To build and install from the latest source:

```bash
$ git clone git@github.com:chargehound/chargehound-python.git
$ pip install -r dev_requirements.txt
```

Run tests:

```bash
$ python setup.py test
```

## Deployment

If you added a new depency, make sure the change is reflected in the 
`requirements.txt` file (for unit tests), the `dev_requirements.txt` file (for module publishers)
and the `setup.py` file (for module consumers).

To deploy a new version of the SDK, you will need Pandoc (http://pandoc.org/) installed.
Pandoc will convert the README.md into the .rst format required for the Python repository.
Instructions are here: [http://pandoc.org/installing.html](http://pandoc.org/installing.html).

Next, install PyPandoc, the Python wrapper for Pandoc, following [these instructions](https://pypi.python.org/pypi/pypandoc).
 
The last pre-requisite is [Twine](https://pypi.python.org/pypi/twine), a utility for interacting with PyPi.

Once Pandoc, PyPandoc and Twine are installed, you can build and deploy a new module to PyPi with the following steps:

 1. Update the CHANGELOG to describe what feature have been added.
 2. Bump the version number in `chargehound/version.py` and `setup.py`
 3. Rebuild and deploy the package with:
   ```python setup.py sdist```
 4. Upload the distributable to PyPi using:   
   ```twine upload dist/{name_of_generated_package}```
 4. Confirm the new package version is available at [https://pypi.python.org/pypi/chargehound](https://pypi.python.org/pypi/chargehound)
