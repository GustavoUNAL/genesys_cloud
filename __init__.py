"""
Genesys Cloud API Client Package

A Python library for interacting with the Genesys Cloud Platform API
using OAuth2 Client Credentials authentication.

This package provides a clean, well-documented interface for accessing
Genesys Cloud resources.

Quick Start:
    >>> from genesys_cloud.src import GenesysCloudClient
    >>> from genesys_cloud.src.config import CLIENT_ID, CLIENT_SECRET, REGION
    >>> 
    >>> client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)
    >>> reporting_api = client.get_reporting_api()
"""

__version__ = "1.0.0"
