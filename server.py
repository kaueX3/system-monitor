#!/usr/bin/env python3
"""
System Monitor Dashboard - Servidor Railway Final
"""

import os
import json
import base64
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# CORS manual para Railway
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
        'total_screenshots': len(endpoint_screenshots),
        'last_update': datetime.now().strftime('%H:%M:%S')
    })

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Monitor - Railway</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: #0a0a0f;
            min-height: 100vh;
            color: #e0e0e0;
            padding: 40px 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 50px;
        }
        .header h1 {
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: rgba(17, 17, 27, 0.7);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 16px;
            padding: 30px;
            text-align: center;
        }
        .stat-value {
            font-size: 3rem;
            font-weight: 700;
            color: #a855f7;
        }
        .stat-label {
            color: #6b7280;
            font-size: 0.9rem;
            text-transform: uppercase;
        }
        .screen-section {
            background: rgba(17, 17, 27, 0.6);
            border: 1px solid rgba(124, 58, 237, 0.15);
            border-radius: 20px;
            padding: 30px;
        }
        .screen-controls {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
        }
        .screen-select {
            flex: 1;
            padding: 14px 18px;
            background: rgba(10, 10, 15, 0.8);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 12px;
            color: #e0e0e0;
            font-size: 0.95rem;
        }
        .screenshot-btn {
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
        }
        .screenshot-btn:disabled {
            background: #4b5563;
            cursor: not-allowed;
        }
        .screen-display {
            background: rgba(10, 10, 15, 0.9);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .live-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(239, 68, 68, 0.15);
            color: #ef4444;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 20px;
        }
        .live-dot {
            width: 8px;
            height: 8px;
            background: #ef4444;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .screen-image {
            max-width: 100%;
            max-height: 70vh;
            border-radius: 12px;
            border: 1px solid rgba(124, 58, 237, 0.3);
        }
        .empty-state {
            color: #4b5563;
            font-size: 1rem;
        }
        .success-message {
            color: #22c55e;
            margin-bottom: 20px;
        }
        @media (max-width: 768px) {
            .stats-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>System Monitor Railway</h1>
            <p>Screenshot Manual</p>
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
                <div class="stat-value" id="totalScreenshots">0</div>
                <div class="stat-label">Screenshots</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="lastUpdate">--</div>
                <div class="stat-label">Última Atualização</div>
            </div>
        </div>
        <div class="screen-section">
            <h2 style="margin-bottom: 20px; color: #f3f4f6;">Screenshot Manual</h2>
            <div class="screen-controls">
                <select id="endpointSelect" class="screen-select" onchange="selectEndpoint()">
                    <option value="">Selecione um endpoint...</option>
                </select>
                <button id="screenshotBtn" class="screenshot-btn" onclick="requestScreenshot()" disabled>
                    📸 Capturar
                </button>
            </div>
            <div class="screen-display" id="screenContent">
                <div class="empty-state">Selecione um endpoint para visualizar</div>
            </div>
        </div>
    </div>
    <script>
        let currentEndpoint = null;
        
        async function loadStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();
                document.getElementById('totalEndpoints').textContent = data.total_endpoints || 0;
                document.getElementById('onlineEndpoints').textContent = data.online_endpoints || 0;
                document.getElementById('totalScreenshots').textContent = data.total_screenshots || 0;
                document.getElementById('lastUpdate').textContent = data.last_update || '--';
            } catch(e) {}
        }
        
        async function loadEndpoints() {
            try {
                const res = await fetch('/api/endpoints');
                const endpoints = await res.json();
                const select = document.getElementById('endpointSelect');
                
                let selectHtml = '<option value="">Selecione um endpoint...</option>';
                endpoints.forEach(e => {
                    selectHtml += `<option value="${e.id}">${e.hostname} (${e.user})</option>`;
                });
                
                select.innerHTML = selectHtml;
            } catch(e) {}
        }
        
        async function selectEndpoint() {
            const endpointId = document.getElementById('endpointSelect').value;
            const btn = document.getElementById('screenshotBtn');
            
            if (!endpointId) {
                document.getElementById('screenContent').innerHTML = '<div class="empty-state">Selecione um endpoint</div>';
                btn.disabled = true;
                return;
            }
            
            btn.disabled = false;
            currentEndpoint = endpointId;
            
            // Verifica se já tem screenshot
            await loadScreen();
        }
        
        async function requestScreenshot() {
            if (!currentEndpoint) return;
            
            const btn = document.getElementById('screenshotBtn');
            btn.disabled = true;
            btn.textContent = '📸 Capturando...';
            
            try {
                const res = await fetch(`/api/request_screenshot/${currentEndpoint}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const data = await res.json();
                
                if (data.status === 'success') {
                    document.getElementById('screenContent').innerHTML = `
                        <div class="success-message">✅ Screenshot solicitado! Aguarde...</div>
                        <div class="live-indicator"><span class="live-dot"></span>PROCESSANDO</div>
                    `;
                    
                    // Verifica a cada 1 segundo por 15 segundos
                    let attempts = 0;
                    const checkInterval = setInterval(async () => {
                        attempts++;
                        await loadScreen();
                        
                        if (attempts >= 15 || document.querySelector('.screen-image')) {
                            clearInterval(checkInterval);
                            btn.disabled = false;
                            btn.textContent = '📸 Capturar';
                        }
                    }, 1000);
                }
            } catch (error) {
                document.getElementById('screenContent').innerHTML = `<div style="color: #ef4444;">❌ Erro: ${error.message}</div>`;
                btn.disabled = false;
                btn.textContent = '📸 Capturar';
            }
        }
        
        async function loadScreen() {
            if (!currentEndpoint) return;
            
            try {
                const res = await fetch(`/api/screenshot/${currentEndpoint}`);
                const data = await res.json();
                if (data.image) {
                    document.getElementById('screenContent').innerHTML = `
                        <div class="live-indicator"><span class="live-dot"></span>LIVE</div>
                        <img class="screen-image" src="data:image/png;base64,${data.image}" alt="Screenshot">
                    `;
                }
            } catch(e) {}
        }
        
        // Inicialização
        loadStats();
        loadEndpoints();
        
        // Atualiza a cada 5 segundos
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
    print(f"🚀 Servidor Railway iniciando na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
