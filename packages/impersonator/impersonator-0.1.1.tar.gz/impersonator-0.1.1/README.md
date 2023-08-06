# Impersonator Python Client

A Python client for the [Impersonator service](https://github.com/Stavatech/Impersonator).

## Installation

Install with:

```
pip install impersonator
```

Or:

```
git clone https://github.com/Stavatech/Impersonator-Python-Client.git
cd Impersonator-Python-Client
pip install .
```

## Tests

Run tests from root of repository with:

```
python -m unittest discover
```

## Example usage

Run a command via an instance of the [Impersonator service](https://github.com/Stavatech/Impersonator) running on the localhost on port 31000.

```python
from imperonator.client import Impersonator

client = Impersonator() # defaults to 127.0.0.1:31000

client.login('username', 'password')
output = client.execute('whoami') # { 'code': 0, 'err': '', 'out': 'username\n' }
client.logout()
```

## API

### Instantiation
```python
client = Impersonator(host = "127.0.0.1", port = 31000, token=None, token_endpoint="tokens", command_endpoint="")
```

Parameters:
* `host` - The host that the Impersonator instance is running on.
* `port` - The port that the Impersonator instance is running on.
* `token` - Instantiate with an existing token so login is not required.
* `token_endpoint` - The relative URL for token management. Should be left as default.
* `command_endpoint` - The relative URL for running commands. Should be left as default.

### Login
```python
token = client.login(username = 'username', password = 'password', private_key = 'key_string', host = "127.0.0.1", port = 22)
```

Parameters:
* `username` - The username of the user account to SSH into (required).
* `password` - The password of the user account to SSH into (required if `private_key` not provided).
* `private_key` - A private SSH key used to access the user account (required if `password` not provided).
* `host` - The host to SSH into (defaults to `127.0.0.1`).
* `port` - The port that SSH is running on (defaults to `22`).

Return value:
* A string representing the access token for executing commands

### Executing commands
```python
output = client.execute(command = 'whoami')
```

Parameters:
* `command` - the command to execute.

Return value:
* A Python dictionary containing the following keys:
    * `out` - The output stream from the executed command
    * `err` - The error stream from the executed command
    * `code` - The exit code from the executed command

### Logout
```
client.logout()
```

Parameters:
* None

Return value:
* None - sets the token attribute on the client instance to `None`