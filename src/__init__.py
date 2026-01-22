"""
Genesys Cloud API Client Library

A Python library for interacting with the Genesys Cloud Platform API
using OAuth2 Client Credentials authentication.

This package provides:
- Authentication management using Client Credentials flow
- Main client class for accessing Genesys Cloud APIs
- Configuration management
- Error handling and logging

Example:
    >>> from genesys_cloud.src import GenesysCloudClient
    >>> from genesys_cloud.src.config import CLIENT_ID, CLIENT_SECRET, REGION
    >>> 
    >>> client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)
    >>> reporting_api = client.get_reporting_api()
"""

from .auth import GenesysCloudAuth
from .client import GenesysCloudClient
from .config import CLIENT_ID, CLIENT_SECRET, REGION

__version__ = "1.0.0"
__all__ = [
    'GenesysCloudAuth',
    'GenesysCloudClient',
    'CLIENT_ID',
    'CLIENT_SECRET',
    'REGION'
]
