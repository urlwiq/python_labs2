import json
import os
from typing import List, Dict, Any

from lab03.base import Server
from lab03.models import WebServer, DatabaseServer, FileServer
from lab02.collection import ServerCollection


def server_to_dict(server: Server) -> Dict[str, Any]:
    data = {
        'type': server.__class__.__name__,
        'hostname': server.hostname,
        'ip_address': server.ip_address,
        'max_connections': server.max_connections,
        'status': server.status,
        'current_connections': server.current_connections
    }
    
    if hasattr(server, 'domain'):
        data['domain'] = server.domain
    if hasattr(server, 'ssl_enabled'):
        data['ssl_enabled'] = server.ssl_enabled
    if hasattr(server, 'db_type'):
        data['db_type'] = server.db_type
    if hasattr(server, 'storage_gb'):
        data['storage_gb'] = server.storage_gb
    if hasattr(server, 'protocol'):
        data['protocol'] = server.protocol
    
    return data


def dict_to_server(data: Dict[str, Any]) -> Server:
    server_type = data.get('type')
    
    if server_type == 'WebServer':
        return WebServer(
            hostname=data['hostname'],
            ip_address=data['ip_address'],
            domain=data.get('domain', 'unknown.com'),
            max_connections=data.get('max_connections', 100),
            status=data.get('status', 'inactive'),
            ssl_enabled=data.get('ssl_enabled', False)
        )
    elif server_type == 'DatabaseServer':
        return DatabaseServer(
            hostname=data['hostname'],
            ip_address=data['ip_address'],
            db_type=data.get('db_type', 'PostgreSQL'),
            storage_gb=data.get('storage_gb', 500),
            max_connections=data.get('max_connections', 200),
            status=data.get('status', 'inactive')
        )
    elif server_type == 'FileServer':
        return FileServer(
            hostname=data['hostname'],
            ip_address=data['ip_address'],
            protocol=data.get('protocol', 'FTP'),
            max_connections=data.get('max_connections', 150),
            status=data.get('status', 'inactive')
        )
    else:
        return Server(
            hostname=data['hostname'],
            ip_address=data['ip_address'],
            max_connections=data.get('max_connections', 100),
            status=data.get('status', 'inactive')
        )


def save(collection: ServerCollection, filepath: str) -> None:
    data = []
    for server in collection.get_all():
        data.append(server_to_dict(server))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load(filepath: str) -> ServerCollection:
    collection = ServerCollection()
    
    if not os.path.exists(filepath):
        return collection
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            server = dict_to_server(item)
            collection.add(server)
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    
    return collection