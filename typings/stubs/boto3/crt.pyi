"""
This type stub file was generated by pyright.
"""

"""
This file contains private functionality for interacting with the AWS
Common Runtime library (awscrt) in boto3.

All code contained within this file is for internal usage within this
project and is not intended for external consumption. All interfaces
contained within are subject to abrupt breaking changes.
"""
CRT_S3_CLIENT = ...
BOTOCORE_CRT_SERIALIZER = ...
CLIENT_CREATION_LOCK = ...
PROCESS_LOCK_NAME = ...
def get_crt_s3_client(client, config): # -> CRTS3Client | None:
    ...

class CRTS3Client:
    """
    This wrapper keeps track of our underlying CRT client, the lock used to
    acquire it and the region we've used to instantiate the client.

    Due to limitations in the existing CRT interfaces, we can only make calls
    in a single region and does not support redirects. We track the region to
    ensure we don't use the CRT client when a successful request cannot be made.
    """
    def __init__(self, crt_client, process_lock, region, cred_provider) -> None:
        ...
    


def is_crt_compatible_request(client, crt_s3_client): # -> Literal[False]:
    """
    Boto3 client must use same signing region and credentials
    as the CRT_S3_CLIENT singleton. Otherwise fallback to classic.
    """
    ...

def compare_identity(boto3_creds, crt_s3_creds): # -> Literal[False]:
    ...

def create_crt_transfer_manager(client, config): # -> CRTTransferManager | None:
    """Create a CRTTransferManager for optimized data transfer."""
    ...
