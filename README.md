# Genesys Cloud API Client

A professional Python library for interacting with the Genesys Cloud Platform API using OAuth2 Client Credentials authentication. This package provides a clean, well-documented interface for accessing Genesys Cloud resources including organizations, groups, divisions, reports, and more.

##  Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Scripts](#scripts)
- [Error Handling](#error-handling)
- [Documentation](#documentation)
- [Contributing](#contributing)

##  Features

- **OAuth2 Client Credentials Authentication**: Secure server-to-server authentication
- **Automatic Region Detection**: Automatically finds the correct Genesys Cloud region
- **Comprehensive API Access**: Access to Reporting, Analytics, Routing, Groups, Divisions, and more
- **Error Handling**: Detailed error messages with actionable suggestions
- **Resource Listing**: Scripts to list all available resources
- **Well Documented**: Complete documentation in English for team collaboration
- **Clean Architecture**: Organized code structure following best practices

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# From the project root
pip install -r requirements.txt
```

Required packages:
- `PureCloudPlatformClientV2>=240.0.0` - Official Genesys Cloud Python SDK
- `requests>=2.31.0` - HTTP library

##  Configuration

### 1. Configure Credentials

The configuration file is located at `src/config.py`. It already contains the credentials, but if you need to update them:

1. Edit `src/config.py` directly, or
2. Copy `config.example.py` to `src/config.py` and fill in your credentials

```python
# src/config.py
CLIENT_ID = "your-client-id-here"
CLIENT_SECRET = "your-client-secret-here"
REGION = "sae1.pure.cloud"  # Your Genesys Cloud region
```

### 2. Region Configuration

The region is already configured as `sae1.pure.cloud` (South America East 1).

If you need to change the region, you can:
- Edit `src/config.py` directly, or
- Run the region detection script:
  ```bash
  python scripts/test_regions.py
  ```

Common regions:
- `sae1.pure.cloud` - South America East 1 (currently configured)
- `usw2.pure.cloud` - US West 2
- `useast1.pure.cloud` - US East 1
- `euw2.pure.cloud` - EU West 2

## 🎯 Quick Start

### Test Connection

```bash
# Using virtual environment
.venv/bin/python scripts/test_connection.py

# Or directly
python scripts/test_connection.py
```

### Basic Usage

```python
from genesys_cloud.src import GenesysCloudClient
from genesys_cloud.src.config import CLIENT_ID, CLIENT_SECRET, REGION

# Create client
client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)

# Test connection
result = client.test_connection()
print(result)

# Access specific APIs
reporting_api = client.get_reporting_api()
groups_api = client.get_groups_api()
divisions_api = client.get_divisions_api()
```

## 📁 Project Structure

```
genesys_cloud/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── auth.py                  # Authentication module
│   ├── client.py                # Main client class
│   └── config.py                # Configuration (credentials)
├── scripts/                      # Utility scripts
│   ├── test_connection.py       # Test API connection
│   ├── test_regions.py          # Auto-detect region
│   └── list_resources.py        # List all resources
├── examples/                     # Usage examples
│   └── example_reports.py       # Reporting examples
├── docs/                         # Documentation
│   └── README.md                # This file
├── config.example.py            # Configuration template
├── .gitignore                   # Git ignore rules
└── README.md                    # Main documentation
```

## 💡 Usage Examples

### List All Resources

```bash
python scripts/list_resources.py
```

This script will:
- List all divisions
- List all groups
- List all external organizations
- List all data tables
- Save results to a JSON file in `../output/`

### Get Organization Information

```python
from genesys_cloud.src import GenesysCloudClient
from genesys_cloud.src.config import CLIENT_ID, CLIENT_SECRET, REGION

client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)
org_api = client.get_organization_api()
org = org_api.get_organizations_me()

print(f"Organization: {org.name}")
print(f"Domain: {org.domain}")
```

### List Groups

```python
from genesys_cloud.src import GenesysCloudClient
from genesys_cloud.src.config import CLIENT_ID, CLIENT_SECRET, REGION

client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)
groups_api = client.get_groups_api()

groups = groups_api.get_groups(page_size=100)
for group in groups.entities:
    print(f"Group: {group.name} (ID: {group.id})")
```

### List Divisions

```python
from genesys_cloud.src import GenesysCloudClient
from genesys_cloud.src.config import CLIENT_ID, CLIENT_SECRET, REGION

client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)
auth_api = client.get_divisions_api()

divisions = auth_api.get_authorization_divisions()
for division in divisions.entities:
    print(f"Division: {division.name} (ID: {division.id})")
```

## 🔧 Scripts

### test_connection.py

Tests the connection to Genesys Cloud API and verifies credentials.

```bash
python scripts/test_connection.py
```

### test_regions.py

Automatically tests different regions to find the correct one for your organization.

```bash
python scripts/test_regions.py
```

### list_resources.py

Lists all available resources (divisions, groups, organizations, data tables) and saves them to a JSON file.

```bash
python scripts/list_resources.py
```

Output is saved to: `../output/genesys_resources_YYYYMMDD_HHMMSS.json`

##  Error Handling

### Error 403 Forbidden

If you receive a 403 error, it means the OAuth client doesn't have the necessary permissions. In this case:

1. Note the exact error and the action you tried to execute
2. Contact your Genesys Cloud administrator
3. Request that the corresponding permission be authorized in the role associated with the client

### Error 401 Unauthorized

If you receive a 401 error, verify that:
- The `CLIENT_ID` is correct
- The `CLIENT_SECRET` is correct
- The credentials haven't been revoked or regenerated

### Error 400 Invalid Client

If you receive a 400 "invalid_client" error:
- Verify credentials are correct
- Verify the region is correct
- Run `python scripts/test_regions.py` to find the correct region

##  Documentation

### API Reference

- [Genesys Cloud Platform API Documentation](https://developer.genesys.cloud/)
- [Python SDK Documentation](https://github.com/MyPureCloud/platform-client-sdk-python)
- [OAuth Client Credentials Flow](https://developer.genesys.cloud/api/rest/authorization/use-client-credentials)

### Code Documentation

All code is documented with:
- Module-level docstrings
- Class docstrings
- Method docstrings with parameter descriptions
- Type hints where applicable
- Usage examples

##  Security Notes

- **Never commit `src/config.py`** with real credentials to the repository
- Use `config.example.py` as a template
- The `.gitignore` file is configured to exclude `src/config.py`
- Store credentials securely in your environment
- Rotate credentials regularly

##  Contributing

When contributing to this project:

1. Follow the existing code structure
2. Document all code in English
3. Add docstrings to all functions and classes
4. Update this README if adding new features
5. Test your changes before committing

##  Important Notes

- **Client Credentials**: This authentication type has no user context, so some user-specific APIs (like `GET /v2/users/me`) won't work
- **Permissions**: The client has a role with restrictions. If you need access to new functionalities, request the corresponding permissions
- **Region**: Make sure the region is correctly configured for your organization

##  Support

For issues or questions:
1. Check the error messages - they often contain helpful suggestions
2. Review the Genesys Cloud API documentation
3. Contact your Genesys Cloud administrator for permission issues
4. Check the logs for detailed error information

##  License

This project is for internal use. All rights reserved.

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-21  
**Maintainer**: Gustavo Arteaga
# genesys_cloud
