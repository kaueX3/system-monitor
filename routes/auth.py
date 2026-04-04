import functools
from datetime import datetime
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
import store

auth_bp = Blueprint('auth', __name__)

def require_login(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('views.index'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    
    if store.is_banned(client_ip):
        store.add_log('SECURITY', 'AUTH', f"IP {client_ip} tentou acessar em período de BAN (Honeypot).")
        return jsonify({'success': False, 'error': 'Muitas tentativas. Acesso bloqueado por 10 minutos.'}), 403
    
    if username == 'lealdade' and password == 'lealdade':
        session.clear() # Limpa qualquer lixo de sessão anterior
        session['logged_in'] = True
        session['username'] = username
        
        # Limpa o histórico de falhas do vencedor
        if client_ip in store.failed_logins:
            store.failed_logins[client_ip]['count'] = 0
            
        store.add_log('SECURITY', 'AUTH', f"Login bem-sucedido (IP: {client_ip})")
        return jsonify({'success': True, 'redirect': '/dashboard'})
    else:
        is_now_banned = store.record_failure(client_ip)
        store.add_log('WARNING', 'AUTH', f"Tentativa falha de login, credenciais: '{username}' (IP: {client_ip})")
        
        if is_now_banned:
             return jsonify({'success': False, 'error': 'Bloqueado. Excesso de tentativas.'}), 403
        
        return jsonify({'success': False, 'error': 'Credenciais inválidas'}), 401

@auth_bp.route('/logout')
def logout():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    session.clear()
    store.add_log('INFO', 'AUTH', f"Logout efetuado (IP: {client_ip})")
    return redirect(url_for('views.index'))
