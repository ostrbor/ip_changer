import re
from urllib.request import urlopen

PG_CONF = '/etc/postgresql/9.4/main/pg_hba.conf'
URL = 'http://checkip.dyndns.com/'
IP_RE = r'\d+(\.\d+){3}'


def get_my_ip():
    data = urlopen(URL).read()
    ip = re.search(IP_RE, str(data)) # if data is bytes error ocur
    return ip.group()

def replace_ip(my_ip):
    with open(PG_CONF) as f:
        lines = f.readlines()
        for num, line in enumerate(lines):
            if not line.startswith('host'): continue
            ip = re.search(IP_RE, line).group()
            if not ip.startswith('127'):
                line = line.replace(ip, my_ip)
                lines[num] = line
                break
    return ''.join(lines)

if __name__ == '__main__':
    my_ip = get_my_ip()
    new_content = replace_ip(my_ip)
    with open(PG_CONF, 'w') as f:
        f.write(new_content)
