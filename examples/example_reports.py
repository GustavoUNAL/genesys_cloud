#!/usr/bin/env python3
"""
Example script for querying billing reports in Genesys Cloud.

This script demonstrates how to use the Reporting APIs to retrieve
billing and reporting data from Genesys Cloud.

Usage:
    python examples/example_reports.py
"""

import sys
import logging
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client import GenesysCloudClient
from src.config import CLIENT_ID, CLIENT_SECRET, REGION
from PureCloudPlatformClientV2.rest import ApiException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def list_available_reports(client):
    """
    List available reports.
    
    Args:
        client: GenesysCloudClient instance
    """
    try:
        reporting_api = client.get_reporting_api()
        
        print("\n📊 Available Reports:")
        print("(Note: Consult Genesys Cloud documentation for specific endpoints)")
        
        # Example of how to get reports (adjust according to the real API)
        # reports = reporting_api.get_reporting_reports()
        # for report in reports.entities:
        #     print(f"  - {report.name} (ID: {report.id})")
        
    except ApiException as e:
        if e.status == 403:
            print(f"\n❌ Error 403: You don't have permissions to access reports.")
            print("Contact the administrator to authorize the 'reporting:report:view' permission")
        else:
            print(f"\n❌ Error listing reports: {e}")
        logger.exception("Detailed error:")


def get_billing_report(client, report_id=None, start_date=None, end_date=None):
    """
    Get a billing report.
    
    Args:
        client: GenesysCloudClient instance
        report_id: Report ID (optional)
        start_date: Start date (ISO 8601 format)
        end_date: End date (ISO 8601 format)
    """
    try:
        reporting_api = client.get_reporting_api()
        
        print("\n📋 Getting billing report...")
        print("(Note: Adjust this code according to specific billing endpoints)")
        
        # Example of how to get a billing report
        # Adjust according to Genesys Cloud API documentation
        
        # report = reporting_api.get_reporting_report(report_id)
        # print(f"Report: {report.name}")
        
    except ApiException as e:
        if e.status == 403:
            print(f"\n❌ Error 403: You don't have permissions to access this report.")
            print("Contact the administrator to authorize the necessary permissions.")
        else:
            print(f"\n❌ Error getting report: {e}")
        logger.exception("Detailed error:")


def main():
    """Main function."""
    print("="*70)
    print("EXAMPLE: BILLING REPORTS QUERY")
    print("="*70)
    
    try:
        # Create client
        print("\n🔌 Connecting to Genesys Cloud...")
        client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)
        
        # Test connection
        result = client.test_connection()
        if result['status'] != 'success':
            print(f"\n❌ Connection error: {result['message']}")
            return 1
        
        print("✅ Connection successful\n")
        
        # List available reports
        list_available_reports(client)
        
        # Get billing report (example)
        # get_billing_report(client, report_id="your-report-id")
        
        print("\n" + "="*70)
        print("NOTE: This is a basic example.")
        print("Consult Genesys Cloud API documentation for:")
        print("  - Specific billing endpoints")
        print("  - Required parameters for each report")
        print("  - Available date formats and filters")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.exception("Detailed error:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
