#!/usr/bin/env python3
"""
Script utilitário para carregar variáveis de ambiente do arquivo .env
Uso: python config.py para testar as configurações
"""

import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configurações da aplicação
LOCAL_IP = os.getenv('LOCAL_IP', 'localhost')
PORT = int(os.getenv('PORT', 8000))
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

# URL para rede local
NETWORK_URL = f"http://{LOCAL_IP}:{PORT}"

def get_config():
    """Retorna um dicionário com todas as configurações"""
    return {
        'local_ip': LOCAL_IP,
        'port': PORT,
        'api_base_url': API_BASE_URL,
        'network_url': NETWORK_URL
    }

def print_config():
    """Imprime as configurações atuais"""
    config = get_config()
    print("🔧 Configurações da API Biblioteca IoT:")
    print(f"  📱 IP Local: {config['local_ip']}")
    print(f"  🔌 Porta: {config['port']}")
    print(f"  🏠 URL Local: {config['api_base_url']}")
    print(f"  🌐 URL Rede: {config['network_url']}")
    print(f"  📚 Swagger UI: {config['network_url']}/docs")

if __name__ == "__main__":
    print_config()
