#!/usr/bin/env python3
"""
List all resources script for Genesys Cloud API.

This script lists all organizations, groups, divisions, and data tables
available in your Genesys Cloud instance and saves the results to a JSON file.

Usage:
    python scripts/list_resources.py
    or
    .venv/bin/python scripts/list_resources.py
"""

import sys
import logging
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client import GenesysCloudClient
from src.config import CLIENT_ID, CLIENT_SECRET, REGION
from PureCloudPlatformClientV2.rest import ApiException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def print_section(title):
    """Print a section title."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def list_divisions(client):
    """List all divisions."""
    print_section("DIVISIONS")
    
    try:
        auth_api = client.get_divisions_api()  # AuthorizationApi contains division methods
        divisions = auth_api.get_authorization_divisions()
        
        if not divisions.entities or len(divisions.entities) == 0:
            print("  No divisions found.")
            return []
        
        print(f"  Total divisions: {len(divisions.entities)}\n")
        
        division_list = []
        for i, division in enumerate(divisions.entities, 1):
            div_info = {
                'id': division.id,
                'name': division.name,
                'description': getattr(division, 'description', 'N/A'),
                'home_division': getattr(division, 'home_division', False)
            }
            division_list.append(div_info)
            
            print(f"  {i}. {division.name}")
            print(f"     ID: {division.id}")
            if hasattr(division, 'description') and division.description:
                print(f"     Description: {division.description}")
            if hasattr(division, 'home_division'):
                print(f"     Home division: {division.home_division}")
            print()
        
        return division_list
        
    except ApiException as e:
        if e.status == 403:
            print(f"  ❌ Error 403: You don't have permissions to view divisions.")
            print("     Contact the administrator to authorize the 'organization:division:view' permission")
        else:
            print(f"  ❌ Error listing divisions: {e}")
        logger.exception("Detailed error:")
        return []
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        logger.exception("Detailed error:")
        return []


def list_groups(client):
    """List all groups."""
    print_section("GROUPS")
    
    try:
        groups_api = client.get_groups_api()
        
        # Get all groups (may require pagination)
        page_size = 100
        page_number = 1
        all_groups = []
        
        while True:
            groups = groups_api.get_groups(page_size=page_size, page_number=page_number)
            
            if not groups.entities or len(groups.entities) == 0:
                break
            
            all_groups.extend(groups.entities)
            
            # Check if there are more pages
            if len(groups.entities) < page_size:
                break
            
            page_number += 1
        
        if len(all_groups) == 0:
            print("  No groups found.")
            return []
        
        print(f"  Total groups: {len(all_groups)}\n")
        
        group_list = []
        for i, group in enumerate(all_groups, 1):
            group_info = {
                'id': group.id,
                'name': group.name,
                'description': getattr(group, 'description', 'N/A'),
                'member_count': getattr(group, 'member_count', 0),
                'division': getattr(group, 'division', {}).get('name', 'N/A') if hasattr(group, 'division') and group.division else 'N/A'
            }
            group_list.append(group_info)
            
            print(f"  {i}. {group.name}")
            print(f"     ID: {group.id}")
            if hasattr(group, 'description') and group.description:
                print(f"     Description: {group.description}")
            if hasattr(group, 'member_count'):
                print(f"     Members: {group.member_count}")
            if hasattr(group, 'division') and group.division:
                print(f"     Division: {group.division.name}")
            print()
        
        return group_list
        
    except ApiException as e:
        if e.status == 403:
            print(f"  ❌ Error 403: You don't have permissions to view groups.")
            print("     Contact the administrator to authorize the 'directory:group:view' permission")
        else:
            print(f"  ❌ Error listing groups: {e}")
        logger.exception("Detailed error:")
        return []
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        logger.exception("Detailed error:")
        return []


def list_external_organizations(client):
    """List all external organizations."""
    print_section("EXTERNAL ORGANIZATIONS")
    
    try:
        external_contacts_api = client.get_external_contacts_api()
        
        # Get all external organizations (may require pagination)
        page_size = 100
        page_number = 1
        all_orgs = []
        
        while True:
            orgs = external_contacts_api.get_externalcontacts_organizations(
                page_size=page_size,
                page_number=page_number
            )
            
            if not orgs.entities or len(orgs.entities) == 0:
                break
            
            all_orgs.extend(orgs.entities)
            
            # Check if there are more pages
            if len(orgs.entities) < page_size:
                break
            
            page_number += 1
        
        if len(all_orgs) == 0:
            print("  No external organizations found.")
            return []
        
        print(f"  Total external organizations: {len(all_orgs)}\n")
        
        org_list = []
        for i, org in enumerate(all_orgs, 1):
            org_info = {
                'id': org.id,
                'name': getattr(org, 'name', 'N/A'),
                'employee_count': getattr(org, 'employee_count', 0),
                'website': getattr(org, 'website', 'N/A'),
                'industry': getattr(org, 'industry', 'N/A')
            }
            org_list.append(org_info)
            
            print(f"  {i}. {getattr(org, 'name', 'No name')}")
            print(f"     ID: {org.id}")
            if hasattr(org, 'employee_count'):
                print(f"     Employees: {org.employee_count}")
            if hasattr(org, 'website') and org.website:
                print(f"     Website: {org.website}")
            if hasattr(org, 'industry') and org.industry:
                print(f"     Industry: {org.industry}")
            print()
        
        return org_list
        
    except ApiException as e:
        if e.status == 403:
            print(f"  ❌ Error 403: You don't have permissions to view external organizations.")
            print("     Contact the administrator to authorize the 'externalContacts:externalOrganization:view' permission")
        else:
            print(f"  ❌ Error listing external organizations: {e}")
        logger.exception("Detailed error:")
        return []
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        logger.exception("Detailed error:")
        return []


def list_data_tables(client):
    """List all data tables."""
    print_section("DATA TABLES")
    
    try:
        architect_api = client.get_architect_api()
        
        # Get all data tables (may require pagination)
        page_size = 100
        page_number = 1
        all_tables = []
        
        while True:
            tables = architect_api.get_flows_datatables(
                page_size=page_size,
                page_number=page_number
            )
            
            if not tables.entities or len(tables.entities) == 0:
                break
            
            all_tables.extend(tables.entities)
            
            # Check if there are more pages
            if len(tables.entities) < page_size:
                break
            
            page_number += 1
        
        if len(all_tables) == 0:
            print("  No data tables found.")
            return []
        
        print(f"  Total data tables: {len(all_tables)}\n")
        
        table_list = []
        for i, table in enumerate(all_tables, 1):
            table_info = {
                'id': table.id,
                'name': table.name,
                'description': getattr(table, 'description', 'N/A'),
                'schema': getattr(table, 'schema', {})
            }
            table_list.append(table_info)
            
            print(f"  {i}. {table.name}")
            print(f"     ID: {table.id}")
            if hasattr(table, 'description') and table.description:
                print(f"     Description: {table.description}")
            if hasattr(table, 'schema') and table.schema:
                schema_info = table.schema
                if hasattr(schema_info, 'properties'):
                    print(f"     Columns: {len(schema_info.properties) if schema_info.properties else 0}")
            print()
        
        return table_list
        
    except ApiException as e:
        if e.status == 403:
            print(f"  ❌ Error 403: You don't have permissions to view data tables.")
            print("     Contact the administrator to authorize the 'architect:datatable:view' permission")
        else:
            print(f"  ❌ Error listing data tables: {e}")
        logger.exception("Detailed error:")
        return []
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        logger.exception("Detailed error:")
        return []


def get_organization_info(client):
    """Get main organization information."""
    print_section("ORGANIZATION INFORMATION")
    
    try:
        org_api = client.get_organization_api()
        org = org_api.get_organizations_me()
        
        print(f"  Name: {org.name}")
        print(f"  ID: {org.id}")
        if hasattr(org, 'domain'):
            print(f"  Domain: {org.domain}")
        if hasattr(org, 'features'):
            print(f"  Features: {', '.join(org.features) if org.features else 'N/A'}")
        print()
        
        return {
            'id': org.id,
            'name': org.name,
            'domain': getattr(org, 'domain', 'N/A'),
            'features': org.features if hasattr(org, 'features') else []
        }
        
    except ApiException as e:
        if e.status == 403:
            print(f"  ❌ Error 403: You don't have permissions to view organization information.")
        else:
            print(f"  ❌ Error getting organization information: {e}")
        logger.exception("Detailed error:")
        return None
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        logger.exception("Detailed error:")
        return None


def save_to_json(data, filename):
    """Save data to a JSON file."""
    try:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Data saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"\n⚠️  Could not save JSON file: {e}")
        return None


def main():
    """Main function."""
    print("="*70)
    print("GENESYS CLOUD RESOURCES LISTING")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Region: {REGION}")
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
        
        # Collect all information
        all_data = {
            'timestamp': datetime.now().isoformat(),
            'region': REGION,
            'organization': None,
            'divisions': [],
            'groups': [],
            'external_organizations': [],
            'data_tables': []
        }
        
        # Get organization information
        all_data['organization'] = get_organization_info(client)
        
        # List divisions
        all_data['divisions'] = list_divisions(client)
        
        # List groups
        all_data['groups'] = list_groups(client)
        
        # List external organizations
        all_data['external_organizations'] = list_external_organizations(client)
        
        # List data tables
        all_data['data_tables'] = list_data_tables(client)
        
        # Summary
        print_section("SUMMARY")
        print(f"  Organization: {all_data['organization']['name'] if all_data['organization'] else 'N/A'}")
        print(f"  Divisions: {len(all_data['divisions'])}")
        print(f"  Groups: {len(all_data['groups'])}")
        print(f"  External organizations: {len(all_data['external_organizations'])}")
        print(f"  Data tables: {len(all_data['data_tables'])}")
        
        # Save to JSON
        filename = f"genesys_resources_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_to_json(all_data, filename)
        
        print("\n" + "="*70)
        print("✅ Process completed")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.exception("Detailed error:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
