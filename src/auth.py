"""
Authentication module for Genesys Cloud API using Client Credentials.

This module handles OAuth2 Client Credentials authentication flow,
region configuration, and error handling for authentication failures.

Classes:
    GenesysCloudAuth: Manages authentication with Genesys Cloud API
"""

import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
import logging

logger = logging.getLogger(__name__)

# Region mapping for common Genesys Cloud regions
REGION_MAP = {
    'usw2.pure.cloud': PureCloudPlatformClientV2.PureCloudRegionHosts.us_west_2,
    'useast1.pure.cloud': PureCloudPlatformClientV2.PureCloudRegionHosts.us_east_1,
    'euw2.pure.cloud': PureCloudPlatformClientV2.PureCloudRegionHosts.eu_west_2,
    'apne1.pure.cloud': PureCloudPlatformClientV2.PureCloudRegionHosts.ap_northeast_1,
    'aps1.pure.cloud': PureCloudPlatformClientV2.PureCloudRegionHosts.ap_southeast_1,
    'cac1.pure.cloud': PureCloudPlatformClientV2.PureCloudRegionHosts.ca_central_1,
    'euc1.pure.cloud': PureCloudPlatformClientV2.PureCloudRegionHosts.eu_central_1,
    'sae1.pure.cloud': PureCloudPlatformClientV2.PureCloudRegionHosts.sa_east_1,  # South America East 1
}


class GenesysCloudAuth:
    """
    Handles authentication with Genesys Cloud API using Client Credentials.
    
    This class manages OAuth2 Client Credentials authentication flow,
    automatically configures the region, and provides detailed error messages
    for authentication failures.
    
    Attributes:
        client_id (str): OAuth Client ID
        client_secret (str): OAuth Client Secret
        region (str): Genesys Cloud region
        api_client: Authenticated API client instance
    
    Example:
        >>> auth = GenesysCloudAuth(client_id, client_secret, "sae1.pure.cloud")
        >>> api_client = auth.authenticate()
    """
    
    def __init__(self, client_id, client_secret, region="usw2.pure.cloud"):
        """
        Initialize the authentication client.
        
        Args:
            client_id (str): OAuth Client ID
            client_secret (str): OAuth Client Secret
            region (str): Genesys Cloud region (e.g., 'sae1.pure.cloud')
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.api_client = None
        
    def authenticate(self):
        """
        Authenticate using Client Credentials and return the API client.
        
        This method:
        1. Configures the region/host based on the provided region
        2. Creates an API client instance
        3. Authenticates using Client Credentials OAuth flow
        4. Returns the authenticated client
        
        Returns:
            PureCloudPlatformClientV2.api_client.ApiClient: Authenticated API client
            
        Raises:
            Exception: If authentication fails with detailed error message
        """
        try:
            logger.info(f"Authenticating with Genesys Cloud in region: {self.region}")
            
            # Configure region/host
            if self.region in REGION_MAP:
                region_host = REGION_MAP[self.region]
                PureCloudPlatformClientV2.configuration.host = region_host.get_api_host()
                logger.info(f"Region configured: {region_host.get_api_host()}")
            else:
                # If region is not in the map, try to use it directly as host
                # Expected format: https://api.{region}
                if not self.region.startswith('http'):
                    api_host = f"https://api.{self.region}"
                else:
                    api_host = self.region
                PureCloudPlatformClientV2.configuration.host = api_host
                logger.info(f"Host configured directly: {api_host}")
            
            # Create API client and get token using Client Credentials
            self.api_client = PureCloudPlatformClientV2.api_client.ApiClient()
            
            # Authenticate using Client Credentials
            self.api_client.get_client_credentials_token(
                self.client_id,
                self.client_secret
            )
            
            logger.info("✓ Authentication successful")
            return self.api_client
            
        except ApiException as e:
            logger.error(f"Authentication error: {e}")
            
            # Extract error information
            error_body = {}
            try:
                if hasattr(e, 'body') and e.body:
                    import json
                    error_body = json.loads(e.body) if isinstance(e.body, str) else e.body
            except:
                pass
            
            error_code = error_body.get('error', 'unknown')
            error_description = error_body.get('error_description', error_body.get('description', str(e)))
            
            if e.status == 400:
                if error_code == 'invalid_client':
                    raise Exception(
                        f"Error 400 - Invalid client:\n"
                        f"  - Verify that CLIENT_ID and CLIENT_SECRET are correct\n"
                        f"  - Verify that REGION is correct (current: {self.region})\n"
                        f"  - Verify that the OAuth client is enabled in Genesys Cloud\n"
                        f"  - Verify that the client has 'Client Credentials' as Grant Type\n"
                        f"  - Description: {error_description}\n"
                        f"  - Configured host: {PureCloudPlatformClientV2.configuration.host}"
                    )
                else:
                    raise Exception(
                        f"Error 400 - Bad Request:\n"
                        f"  - Code: {error_code}\n"
                        f"  - Description: {error_description}\n"
                        f"  - Region: {self.region}\n"
                        f"  - Host: {PureCloudPlatformClientV2.configuration.host}"
                    )
            elif e.status == 401:
                raise Exception(
                    f"Error 401 - Invalid credentials:\n"
                    f"  - Verify CLIENT_ID and CLIENT_SECRET\n"
                    f"  - Description: {error_description}"
                )
            elif e.status == 403:
                raise Exception(
                    "Access forbidden (403 Forbidden). "
                    "The client does not have the necessary permissions. "
                    "Contact the administrator to authorize the required permissions."
                )
            else:
                raise Exception(
                    f"Authentication error (Status {e.status}):\n"
                    f"  - Code: {error_code}\n"
                    f"  - Description: {error_description}\n"
                    f"  - Region: {self.region}"
                )
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {e}")
            raise
    
    def get_api_client(self):
        """
        Return the authenticated API client.
        If not authenticated, performs authentication first.
        
        Returns:
            PureCloudPlatformClientV2.api_client.ApiClient: Authenticated API client
        """
        if self.api_client is None:
            self.authenticate()
        return self.api_client
