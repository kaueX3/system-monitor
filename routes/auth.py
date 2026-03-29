import functools
from datetime import datetime
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template

auth_bp = Blueprint('auth', __name__)

def require_login(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
            user_agent = request.headers.get('User-Agent', 'unknown')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"[SECURITY] Unauthorized access attempt from {client_ip} at {timestamp}")
            return render_template('warning.html', timestamp=timestamp, client_ip=client_ip, user_agent=user_agent[:100] + '...' if len(user_agent) > 100 else user_agent)
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['POST'])
def login():
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

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))
