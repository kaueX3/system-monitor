import functools
from datetime import datetime
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template

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
