"""
Configuration template for Genesys Cloud API connection.

Copy this file to src/config.py and fill in your credentials.

IMPORTANT: Do not commit src/config.py with real credentials to the repository.
"""

# OAuth Client Credentials
CLIENT_ID = "your-client-id-here"
CLIENT_SECRET = "your-client-secret-here"

# Genesys Cloud Region
# Common options: 'sae1.pure.cloud', 'usw2.pure.cloud', 'useast1.pure.cloud', etc.
# If unsure, consult with your Genesys Cloud administrator or run:
# python scripts/test_regions.py
REGION = "sae1.pure.cloud"  # Change according to your region

# Additional Configuration
ENVIRONMENT = "mypurecloud.com"  # Can be 'mypurecloud.com' or 'genesyscloud.com'
