# aws-iam-vault
Helper to retrieve a secret from Hashicorp Vault using an EC2 instance's IAM role to authenticate.

Use on an AWS EC2 instance with a role that has access to the Vault path to be retrieved.

Install:
```console
pip install awsiamvault
```
Use:
```python
from awsiamvault import read_secret

secret = read_secret(region, vault_url, path)
```
Test:
```console
nosetests -v --with-cover --cover-erase --cover-tests --cover-package=awsiamvault
```
