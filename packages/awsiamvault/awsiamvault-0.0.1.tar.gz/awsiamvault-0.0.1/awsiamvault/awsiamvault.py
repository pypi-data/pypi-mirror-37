# Retrieves secrets from Vault, authenticating using the instances IAM role
import hvac
import boto3


class BadCredentials(Exception):
    pass


def _get_aws_credentials():
    """
        Return keys and token for the instances IAM role.
    """
    session = boto3.Session()
    credentials = session.get_credentials()
    credentials = credentials.get_frozen_credentials()

    if not hasattr(credentials, 'access_key'):
        raise BadCredentials

    if len(credentials.access_key) < 16:
        raise BadCredentials

    return credentials


def _connect_to_vault(url, access_key, secret_key, token, region):
    """
        Return Vault client using supplied IAM credentials.
    """
    vault_client = hvac.Client(url=url)
    vault_client.auth_aws_iam(access_key,
                              secret_key,
                              token,
                              region=region)
    return vault_client


def _read_vault(vault_client, path):
    """
        Return the secret at path.
    """
    return vault_client.read(path)


def read_secret(region, vault_url, path):
    """
        Authenticates to Vault using the instances IAM role and
        retrieves a secret.

        :param region: aws region
        :param vault_url: url for vault API
        :param path: vault secret path

        :returns: the object from the vault secret path
    """
    aws_credentials = _get_aws_credentials()
    vault_client = _connect_to_vault(vault_url,
                                     aws_credentials.access_key,
                                     aws_credentials.secret_key,
                                     aws_credentials.token,
                                     region=region)
    return _read_vault(vault_client, path)
