from flask import Blueprint, render_template
from .auth import require_login

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('login.html')

@views_bp.route('/dashboard')
@require_login
def dashboard():
    return render_template('index.html')
