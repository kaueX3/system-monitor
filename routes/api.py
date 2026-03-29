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

@api_bp.route('/api/request_screenshot/<endpoint_id>', methods=['POST'])
@require_login
def request_screenshot(endpoint_id):
    if endpoint_id not in store.screenshot_requests:
        store.screenshot_requests[endpoint_id] = {
            'request_screenshot': True,
            'timestamp': datetime.now().isoformat()
        }
    return jsonify({'status': 'success', 'message': f'Screenshot solicitado para {endpoint_id}'})

@api_bp.route('/api/test')
def test_api():
    return jsonify({
        'status': 'online',
        'server': 'LEALDADE SYSTEM',
        'timestamp': datetime.now().isoformat(),
        'endpoints_count': len(store.endpoints)
    })
