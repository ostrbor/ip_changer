import re, os
from urllib.request import urlopen

PG_MAIN = '/etc/init.d/postgresql'
PG_CONF = '/etc/postgresql/9.4/main/pg_hba.conf'
URL = 'http://checkip.dyndns.com/'
IP_RE = r'\d+(\.\d+){3}'
LOCALHOST_MARK = '127'


def get_my_ip(repeat=3, timeout=5):
    for i in range(repeat):
        try:
            url_file = urlopen(URL, timeout=timeout)
            break
        except:
            continue
    if not data: return None
    content = url_file.read()
    ip = re.search(IP_RE, str(content)) # if data is bytes error ocur
    return ip.group()

def replace_ip(my_ip):
    with open(PG_CONF) as f:
        lines = f.readlines()
        for num, line in enumerate(lines):
            if not line.startswith('host'): continue
            if my_ip in line: return None
            ip = re.search(IP_RE, line).group()
            if not ip.startswith(LOCALHOST_MARK):
                line = line.replace(ip, my_ip)
                lines[num] = line
                break
    return ''.join(lines)

def restart():
    os.system(PG_MAIN + ' restart')

if __name__ == '__main__':
    my_ip = get_my_ip()
    if my_ip:
        new_content = replace_ip(my_ip)
        if new_content:
            with open(PG_CONF, 'w') as f:
                f.write(new_content)
                restart()
    else:
        print("Can't get ip address. Check for URL validity.")
