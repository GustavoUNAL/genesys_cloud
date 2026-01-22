#!/usr/bin/env python3
"""
Script para listar las organizaciones disponibles en la licencia de Genesys Cloud.

Este script obtiene información sobre:
- La organización principal
- Organizaciones externas (si están disponibles)
- Información detallada de la licencia y características

Usage:
    python scripts/list_organizations.py
    or
    ./run.sh scripts/list_organizations.py
"""

import sys
import logging
import os
import json
from datetime import datetime

# Add parent directory to path for imports
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


def print_section(title):
    """Print a section title."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def get_organization_details(client):
    """Obtener información detallada de la organización principal."""
    print_section("ORGANIZACIÓN PRINCIPAL")
    
    try:
        org_api = client.get_organization_api()
        org = org_api.get_organizations_me()
        
        print(f"  Nombre: {org.name}")
        print(f"  ID: {org.id}")
        print(f"  Dominio: {getattr(org, 'domain', 'N/A')}")
        
        # Información adicional si está disponible
        if hasattr(org, 'features') and org.features:
            print(f"\n  Características de la licencia:")
            for feature in org.features:
                print(f"    • {feature}")
        
        if hasattr(org, 'default_language'):
            print(f"  Idioma por defecto: {org.default_language}")
        
        if hasattr(org, 'third_party_org_name'):
            print(f"  Nombre de organización de terceros: {org.third_party_org_name}")
        
        if hasattr(org, 'settings'):
            settings = org.settings
            if hasattr(settings, 'password_expiration_days'):
                print(f"  Expiración de contraseña (días): {settings.password_expiration_days}")
        
        print()
        
        return {
            'id': org.id,
            'name': org.name,
            'domain': getattr(org, 'domain', 'N/A'),
            'features': org.features if hasattr(org, 'features') else [],
            'default_language': getattr(org, 'default_language', 'N/A'),
            'third_party_org_name': getattr(org, 'third_party_org_name', None),
            'type': 'principal'
        }
        
    except ApiException as e:
        if e.status == 403:
            print(f"  ❌ Error 403: No tienes permisos para ver la información de la organización.")
            print("     Contacta al administrador para autorizar el permiso 'organization:organization:view'")
        else:
            print(f"  ❌ Error obteniendo información de la organización: {e}")
        logger.exception("Detailed error:")
        return None
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        logger.exception("Detailed error:")
        return None


def list_external_organizations(client):
    """Listar todas las organizaciones externas."""
    print_section("ORGANIZACIONES EXTERNAS")
    
    try:
        external_contacts_api = client.get_external_contacts_api()
        
        # Obtener todas las organizaciones externas (puede requerir paginación)
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
            
            # Verificar si hay más páginas
            if len(orgs.entities) < page_size:
                break
            
            page_number += 1
        
        if len(all_orgs) == 0:
            print("  No se encontraron organizaciones externas.")
            return []
        
        print(f"  Total organizaciones externas: {len(all_orgs)}\n")
        
        org_list = []
        for i, org in enumerate(all_orgs, 1):
            org_info = {
                'id': org.id,
                'name': getattr(org, 'name', 'N/A'),
                'employee_count': getattr(org, 'employee_count', 0),
                'website': getattr(org, 'website', 'N/A'),
                'industry': getattr(org, 'industry', 'N/A'),
                'type': 'externa'
            }
            org_list.append(org_info)
            
            print(f"  {i}. {getattr(org, 'name', 'Sin nombre')}")
            print(f"     ID: {org.id}")
            if hasattr(org, 'employee_count') and org.employee_count:
                print(f"     Empleados: {org.employee_count}")
            if hasattr(org, 'website') and org.website:
                print(f"     Sitio web: {org.website}")
            if hasattr(org, 'industry') and org.industry:
                print(f"     Industria: {org.industry}")
            print()
        
        return org_list
        
    except ApiException as e:
        if e.status == 403:
            print(f"  ❌ Error 403: No tienes permisos para ver organizaciones externas.")
            print("     Contacta al administrador para autorizar el permiso 'externalContacts:externalOrganization:view'")
        else:
            print(f"  ❌ Error listando organizaciones externas: {e}")
        logger.exception("Detailed error:")
        return []
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        logger.exception("Detailed error:")
        return []


def save_to_json(data, filename):
    """Guardar datos en un archivo JSON."""
    try:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Datos guardados en: {filepath}")
        return filepath
    except Exception as e:
        print(f"\n⚠️  No se pudo guardar el archivo JSON: {e}")
        return None


def main():
    """Función principal."""
    print("="*70)
    print("LISTADO DE ORGANIZACIONES - GENESYS CLOUD")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Región: {REGION}")
    print("="*70)
    
    try:
        # Crear cliente
        print("\n🔌 Conectando a Genesys Cloud...")
        client = GenesysCloudClient(CLIENT_ID, CLIENT_SECRET, REGION)
        
        # Probar conexión
        result = client.test_connection()
        if result['status'] != 'success':
            print(f"\n❌ Error de conexión: {result['message']}")
            return 1
        
        print("✅ Conexión exitosa\n")
        
        # Recopilar toda la información
        all_data = {
            'timestamp': datetime.now().isoformat(),
            'region': REGION,
            'organizacion_principal': None,
            'organizaciones_externas': []
        }
        
        # Obtener información de la organización principal
        all_data['organizacion_principal'] = get_organization_details(client)
        
        # Listar organizaciones externas
        all_data['organizaciones_externas'] = list_external_organizations(client)
        
        # Resumen
        print_section("RESUMEN")
        if all_data['organizacion_principal']:
            print(f"  Organización Principal: {all_data['organizacion_principal']['name']}")
            print(f"    ID: {all_data['organizacion_principal']['id']}")
            print(f"    Dominio: {all_data['organizacion_principal']['domain']}")
            if all_data['organizacion_principal']['features']:
                print(f"    Características: {len(all_data['organizacion_principal']['features'])}")
        else:
            print("  Organización Principal: No disponible")
        
        print(f"  Organizaciones Externas: {len(all_data['organizaciones_externas'])}")
        
        # Guardar en JSON
        filename = f"organizaciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_to_json(all_data, filename)
        
        print("\n" + "="*70)
        print("✅ Proceso completado")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        logger.exception("Detailed error:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
