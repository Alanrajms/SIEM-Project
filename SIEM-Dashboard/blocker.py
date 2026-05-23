import re
import os

def extract_ip(log):

    ip_pattern = r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}'
    match = re.search(ip_pattern, log)

    if match:
        return match.group()

    return None

def block_ip(ip):

    print(f"[!] Blocking IP: {ip}")

    # WINDOWS FIREWALL BLOCK
    command = f'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block remoteip={ip}'

    os.system(command)