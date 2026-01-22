#!/usr/bin/env python3
"""
Test connection script for Genesys Cloud API.

This script verifies that the connection to Genesys Cloud API is working
correctly with the configured credentials and region.

Usage:
    python scripts/test_connection.py
    or
    .venv/bin/python scripts/test_connection.py
"""

import sys
import logging
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import CLIENT_ID, CLIENT_SECRET, REGION
from src.client import GenesysCloudClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function to test the connection."""
    print("="*70)
    print("GENESYS CLOUD API CONNECTION TEST")
    print("="*70)
    print(f"Client ID: {CLIENT_ID[:20]}...")
    print(f"Region: {REGION}")
    print("="*70)
    
    try:
        # Create client
        client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)
        
        # Test connection
        print("\n🔌 Testing connection...")
        result = client.test_connection()
        
        print(f"\n📊 Result: {result['status']}")
        print(f"💬 Message: {result['message']}")
        
        if result['status'] == 'success':
            print("\n✅ Connection successful!")
            print("\nYou can now start using Genesys Cloud APIs.")
            print("\nUsage example:")
            print("  from genesys_cloud.src import GenesysCloudClient")
            print("  from genesys_cloud.src.config import CLIENT_ID, CLIENT_SECRET, REGION")
            print("  ")
            print("  client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)")
            print("  reporting_api = client.get_reporting_api()")
            return 0
        elif result['status'] == 'forbidden':
            print("\n❌ Error 403 Forbidden")
            print("\nThe client does not have the necessary permissions.")
            print("Please inform the administrator about this error and")
            print("the action you want to execute to authorize the permission.")
            if 'error' in result:
                print(f"\nError details: {result['error']}")
            return 1
        else:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
            print("\n💡 SUGGESTION: If the error is 'invalid_client', try running:")
            print("   python scripts/test_regions.py")
            print("   This will test different regions to find the correct one.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.exception("Detailed error:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
