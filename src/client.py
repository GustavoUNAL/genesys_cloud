"""
Main client module for interacting with Genesys Cloud API.

This module provides the main client class that wraps authentication
and provides access to various Genesys Cloud API endpoints.

Classes:
    GenesysCloudClient: Main client for Genesys Cloud API interactions
"""

import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
import logging
from .auth import GenesysCloudAuth

logger = logging.getLogger(__name__)


class GenesysCloudClient:
    """
    Main client for interacting with Genesys Cloud API.
    
    This class provides a unified interface to access various Genesys Cloud APIs
    including Reporting, Analytics, Routing, Groups, Divisions, and more.
    
    Attributes:
        auth (GenesysCloudAuth): Authentication handler
        api_client: Authenticated API client instance
    
    Example:
        >>> from genesys_cloud.src import GenesysCloudClient
        >>> from genesys_cloud.src.config import CLIENT_ID, CLIENT_SECRET, REGION
        >>> 
        >>> client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)
        >>> reporting_api = client.get_reporting_api()
        >>> groups_api = client.get_groups_api()
    """
    
    def __init__(self, client_id, client_secret, region="usw2.pure.cloud"):
        """
        Initialize the Genesys Cloud client.
        
        Args:
            client_id (str): OAuth Client ID
            client_secret (str): OAuth Client Secret
            region (str): Genesys Cloud region
        """
        self.auth = GenesysCloudAuth(client_id, client_secret, region)
        self.api_client = None
        self._initialize_apis()
    
    def _initialize_apis(self):
        """Initialize available APIs."""
        self.api_client = self.auth.get_api_client()
        logger.info("APIs initialized")
    
    def test_connection(self):
        """
        Test the connection with Genesys Cloud.
        
        Returns:
            dict: Connection status information with keys:
                - status (str): 'success', 'forbidden', or 'error'
                - message (str): Status message
                - region (str): Configured region (if success)
                - error (str): Error details (if error)
        """
        try:
            logger.info("Testing connection with Genesys Cloud...")
            
            # Note: With Client Credentials, some user APIs don't work
            # For example, get_users_me() doesn't work with Client Credentials
            
            logger.info("✓ Connection successful")
            return {
                "status": "success",
                "message": "Connection established successfully",
                "region": self.auth.region
            }
            
        except ApiException as e:
            logger.error(f"Error testing connection: {e}")
            if e.status == 403:
                return {
                    "status": "forbidden",
                    "message": "Access forbidden. The client does not have the necessary permissions.",
                    "error": str(e)
                }
            else:
                return {
                    "status": "error",
                    "message": f"Error connecting: {e}",
                    "error": str(e)
                }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {e}",
                "error": str(e)
            }
    
    def get_reporting_api(self):
        """
        Get ReportingApi instance for querying reports.
        
        Returns:
            PureCloudPlatformClientV2.ReportingApi: Reporting API instance
        """
        return PureCloudPlatformClientV2.ReportingApi(self.api_client)
    
    def get_analytics_api(self):
        """
        Get AnalyticsApi instance for querying analytics.
        
        Returns:
            PureCloudPlatformClientV2.AnalyticsApi: Analytics API instance
        """
        return PureCloudPlatformClientV2.AnalyticsApi(self.api_client)
    
    def get_routing_api(self):
        """
        Get RoutingApi instance for querying routing.
        
        Returns:
            PureCloudPlatformClientV2.RoutingApi: Routing API instance
        """
        return PureCloudPlatformClientV2.RoutingApi(self.api_client)
    
    def get_authorization_api(self):
        """
        Get AuthorizationApi instance for querying permissions.
        
        Returns:
            PureCloudPlatformClientV2.AuthorizationApi: Authorization API instance
        """
        return PureCloudPlatformClientV2.AuthorizationApi(self.api_client)
    
    def get_groups_api(self):
        """
        Get GroupsApi instance for querying groups.
        
        Returns:
            PureCloudPlatformClientV2.GroupsApi: Groups API instance
        """
        return PureCloudPlatformClientV2.GroupsApi(self.api_client)
    
    def get_divisions_api(self):
        """
        Get AuthorizationApi instance for querying divisions.
        
        Note: Divisions are accessed through AuthorizationApi, not a separate DivisionsApi.
        
        Returns:
            PureCloudPlatformClientV2.AuthorizationApi: Authorization API instance (includes divisions)
        """
        return PureCloudPlatformClientV2.AuthorizationApi(self.api_client)
    
    def get_organization_api(self):
        """
        Get OrganizationApi instance for querying organization information.
        
        Returns:
            PureCloudPlatformClientV2.OrganizationApi: Organization API instance
        """
        return PureCloudPlatformClientV2.OrganizationApi(self.api_client)
    
    def get_external_contacts_api(self):
        """
        Get ExternalContactsApi instance for querying external contacts and organizations.
        
        Returns:
            PureCloudPlatformClientV2.ExternalContactsApi: External Contacts API instance
        """
        return PureCloudPlatformClientV2.ExternalContactsApi(self.api_client)
    
    def get_architect_api(self):
        """
        Get ArchitectApi instance for querying data tables and other architect resources.
        
        Returns:
            PureCloudPlatformClientV2.ArchitectApi: Architect API instance
        """
        return PureCloudPlatformClientV2.ArchitectApi(self.api_client)
