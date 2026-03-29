import os
from flask import Flask, request
import config

from routes.auth import auth_bp
from routes.views import views_bp
from routes.api import api_bp
from routes.collector import collector_bp

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# CORS manual
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

# Middleware de logs global
@app.before_request
def log_request():
    if request.endpoint and 'static' not in request.endpoint:
        print(f"[REQUEST] {request.method} {request.path} - IP: {request.environ.get('REMOTE_ADDR', 'unknown')}")

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
