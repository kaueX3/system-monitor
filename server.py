import os
from flask import Flask, request
import config

from routes.auth import auth_bp
from routes.views import views_bp
from routes.api import api_bp
from routes.collector import collector_bp

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# CORS e Segurança
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    
    # Proteções rigorosas contra cache (Evita que o navegador mostre o /dashboard pelo histórico)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Proteções adicionais
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

import store

# Middleware de logs global
@app.before_request
def log_request():
    if request.endpoint and 'static' not in request.endpoint:
        print(f"[REQUEST] {request.method} {request.path} - IP: {request.environ.get('REMOTE_ADDR', 'unknown')}")

@app.errorhandler(404)
def not_found(e):
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    store.add_log('WARNING', 'HTTP', f"Tentativa de acesso a rota inexistente: {request.path} (IP: {ip})")
    return "Not Found", 404

# Registrar todos os rotas modulares (blueprints)
app.register_blueprint(auth_bp)
app.register_blueprint(views_bp)
app.register_blueprint(api_bp)
app.register_blueprint(collector_bp)

if __name__ == '__main__':
    print("🚀 Iniciando System Monitor MODULAR para Railway...")
    print("📡 Servidor refatorado com Arquitetura Limpa (MVC/Blueprints)")
    print("🌐 URL: https://web-production-49d37.up.railway.app")
    print()
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', config.PORT)))
