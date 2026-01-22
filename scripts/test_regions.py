#!/usr/bin/env python3
"""
Region detection script for Genesys Cloud API.

This script tests different Genesys Cloud regions to automatically
find the correct region for your organization.

Usage:
    python scripts/test_regions.py
    or
    .venv/bin/python scripts/test_regions.py
"""

import sys
import logging
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import CLIENT_ID, CLIENT_SECRET
from src.auth import GenesysCloudAuth
from PureCloudPlatformClientV2.rest import ApiException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# List of common regions to test
REGIONS_TO_TEST = [
    "usw2.pure.cloud",
    "useast1.pure.cloud",
    "euw2.pure.cloud",
    "apne1.pure.cloud",
    "aps1.pure.cloud",
    "cac1.pure.cloud",
    "euc1.pure.cloud",
    "sae1.pure.cloud",
]


def test_region(region):
    """
    Test authentication with a specific region.
    
    Args:
        region (str): Region to test
        
    Returns:
        tuple: (success: bool, region_name: str or None)
    """
    print(f"\n{'='*70}")
    print(f"Testing region: {region}")
    print(f"{'='*70}")
    
    try:
        auth = GenesysCloudAuth(CLIENT_ID, CLIENT_SECRET, region)
        api_client = auth.authenticate()
        print(f"✅ SUCCESS! The correct region is: {region}")
        return True, region
    except ApiException as e:
        error_body = {}
        try:
            if hasattr(e, 'body') and e.body:
                import json
                error_body = json.loads(e.body) if isinstance(e.body, str) else e.body
        except:
            pass
        
        error_code = error_body.get('error', 'unknown')
        print(f"❌ Error: {error_code} - {error_body.get('error_description', str(e))}")
        return False, None
    except Exception as e:
        print(f"❌ Error: {str(e)[:200]}")
        return False, None


def main():
    """Test all common regions."""
    print("="*70)
    print("REGION DETECTION - GENESYS CLOUD")
    print("="*70)
    print(f"Client ID: {CLIENT_ID[:20]}...")
    print("\nTesting different regions...")
    
    successful_region = None
    
    for region in REGIONS_TO_TEST:
        success, region_name = test_region(region)
        if success:
            successful_region = region_name
            break
    
    print("\n" + "="*70)
    if successful_region:
        print(f"✅ REGION FOUND: {successful_region}")
        print(f"\nUpdate genesys_cloud/src/config.py with:")
        print(f'REGION = "{successful_region}"')
    else:
        print("❌ Could not authenticate with any common region.")
        print("\nPossible causes:")
        print("  1. Credentials are incorrect")
        print("  2. OAuth client is not enabled")
        print("  3. Client does not have 'Client Credentials' as Grant Type")
        print("  4. Organization uses a custom region")
        print("\nContact your Genesys Cloud administrator to verify:")
        print("  - That the OAuth client is active")
        print("  - That it has 'Client Credentials' enabled")
        print("  - The correct region for the organization")
    print("="*70)
    
    return 0 if successful_region else 1


if __name__ == "__main__":
    sys.exit(main())
