from common import *

"""
[Interface]
...

[Peer]
...
"""

# AllowedIPs = 195.201.201.32/32, 192.173.68.0/24, 54.144.0.0/12, 54.192.0.0/12

def make_wireguard():
    log_info('make_wireguard: Starting')
    data = read_csv(DB_FILE)
    file_str = ""
    # add header
    file_str += "[Interface]\n"
    file_str += "...\n\n"
    file_str += "[Peer]\n"
    file_str += "...\n"
    # add allowed IPs
    allowed_ips = []
    for index, row in data.iterrows():
        allowed_ips.append(row['ipv4'])
    file_str += f"AllowedIPs = {', '.join(allowed_ips)}\n"
    # manaually write file

    with open('out/wireguard_incomplete.conf', 'w') as file:
        file.write(file_str)
    log_happy('Wireguard file created')
    log_info('make_wireguard: Finished')


if __name__ == '__main__':
    make_wireguard()