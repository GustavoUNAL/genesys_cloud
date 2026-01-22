#!/usr/bin/env python3
"""
Script para listar todos los usuarios de la organización en Genesys Cloud.

Este script obtiene información detallada sobre:
- Información básica (nombre, email, estado)
- División y roles asignados
- Ubicación y manager
- Fechas de creación y modificación
- Licencias y características

Usage:
    python scripts/list_users.py
    or
    ./run.sh scripts/list_users.py
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


def get_user_details(user):
    """Extraer información detallada de un usuario."""
    user_info = {
        'id': user.id,
        'name': getattr(user, 'name', 'N/A'),
        'email': getattr(user, 'email', 'N/A'),
        'state': getattr(user, 'state', 'N/A'),
        'division': None,
        'roles': [],
        'locations': [],
        'manager': None,
        'title': getattr(user, 'title', None),
        'department': getattr(user, 'department', None),
        'acd_auto_answer': getattr(user, 'acd_auto_answer', None),
        'version': getattr(user, 'version', None),
        'date_created': None,
        'date_modified': None
    }
    
    # División
    if hasattr(user, 'division') and user.division:
        user_info['division'] = {
            'id': user.division.id if hasattr(user.division, 'id') else None,
            'name': user.division.name if hasattr(user.division, 'name') else None
        }
    
    # Roles
    if hasattr(user, 'roles') and user.roles:
        user_info['roles'] = [
            {
                'id': role.id if hasattr(role, 'id') else None,
                'name': role.name if hasattr(role, 'name') else None
            }
            for role in user.roles
        ]
    
    # Ubicaciones
    if hasattr(user, 'locations') and user.locations:
        user_info['locations'] = [
            {
                'id': loc.id if hasattr(loc, 'id') else None,
                'name': loc.name if hasattr(loc, 'name') else None
            }
            for loc in user.locations
        ]
    
    # Manager
    if hasattr(user, 'manager') and user.manager:
        user_info['manager'] = {
            'id': user.manager.id if hasattr(user.manager, 'id') else None,
            'name': user.manager.name if hasattr(user.manager, 'name') else None
        }
    
    # Fechas
    if hasattr(user, 'date_created'):
        user_info['date_created'] = str(user.date_created) if user.date_created else None
    if hasattr(user, 'date_modified'):
        user_info['date_modified'] = str(user.date_modified) if user.date_modified else None
    
    return user_info


def list_all_users(client):
    """Listar todos los usuarios de la organización."""
    print_section("USUARIOS DE LA ORGANIZACIÓN")
    
    try:
        users_api = client.get_users_api()
        
        # Obtener todos los usuarios (puede requerir paginación)
        page_size = 100
        page_number = 1
        all_users = []
        
        print("  Obteniendo usuarios (esto puede tomar un momento)...\n")
        
        while True:
            try:
                users = users_api.get_users(
                    page_size=page_size,
                    page_number=page_number,
                    expand=['division', 'roles', 'locations', 'manager']
                )
                
                if not users.entities or len(users.entities) == 0:
                    break
                
                all_users.extend(users.entities)
                
                # Mostrar progreso
                print(f"  Procesados: {len(all_users)} usuarios...", end='\r')
                
                # Verificar si hay más páginas
                if len(users.entities) < page_size:
                    break
                
                page_number += 1
                
            except ApiException as e:
                if e.status == 403:
                    print(f"\n  ❌ Error 403: No tienes permisos para ver usuarios.")
                    print("     Contacta al administrador para autorizar el permiso 'directory:user:view'")
                    return []
                else:
                    raise
        
        print(f"\n  Total usuarios encontrados: {len(all_users)}\n")
        
        if len(all_users) == 0:
            print("  No se encontraron usuarios.")
            return []
        
        # Procesar información de cada usuario
        users_list = []
        active_count = 0
        inactive_count = 0
        
        for i, user in enumerate(all_users, 1):
            user_info = get_user_details(user)
            users_list.append(user_info)
            
            # Contar estados
            if user_info['state'] == 'active':
                active_count += 1
            elif user_info['state'] == 'inactive':
                inactive_count += 1
            
            # Mostrar información del usuario
            state_icon = "✅" if user_info['state'] == 'active' else "❌"
            print(f"  {i}. {state_icon} {user_info['name']}")
            print(f"     Email: {user_info['email']}")
            print(f"     Estado: {user_info['state']}")
            
            if user_info['division']:
                print(f"     División: {user_info['division'].get('name', 'N/A')}")
            
            if user_info['roles']:
                roles_names = [r.get('name', 'N/A') or 'N/A' for r in user_info['roles']]
                print(f"     Roles: {', '.join(roles_names)}")
            
            if user_info['title']:
                print(f"     Título: {user_info['title']}")
            
            if user_info['department']:
                print(f"     Departamento: {user_info['department']}")
            
            if user_info['manager']:
                print(f"     Manager: {user_info['manager'].get('name', 'N/A')}")
            
            if user_info['locations']:
                loc_names = [loc.get('name', 'N/A') or 'N/A' for loc in user_info['locations']]
                print(f"     Ubicaciones: {', '.join(loc_names)}")
            
            print()
        
        # Estadísticas
        print_section("ESTADÍSTICAS")
        print(f"  Total usuarios: {len(all_users)}")
        print(f"  Usuarios activos: {active_count}")
        print(f"  Usuarios inactivos: {inactive_count}")
        print(f"  Usuarios con roles: {sum(1 for u in users_list if u['roles'])}")
        print(f"  Usuarios con manager: {sum(1 for u in users_list if u['manager'])}")
        
        return users_list
        
    except ApiException as e:
        if e.status == 403:
            print(f"  ❌ Error 403: No tienes permisos para ver usuarios.")
            print("     Contacta al administrador para autorizar el permiso 'directory:user:view'")
        else:
            print(f"  ❌ Error listando usuarios: {e}")
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
    print("LISTADO DE USUARIOS - GENESYS CLOUD")
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
        
        # Listar usuarios
        users_data = list_all_users(client)
        
        # Preparar datos para guardar
        all_data = {
            'timestamp': datetime.now().isoformat(),
            'region': REGION,
            'total_users': len(users_data),
            'users': users_data
        }
        
        # Guardar en JSON
        if users_data:
            filename = f"usuarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
