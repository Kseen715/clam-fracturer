from common import *

"""
[Interface]
...

[Peer]
...
"""

# AllowedIPs = 195.201.201.32/32, 192.173.68.0/24, 54.144.0.0/12, 54.192.0.0/12
# TODO: android client can process ~256 peers, so we need to compact the list via some smart shit
def make_wireguard():
    Logger.info('make_wireguard: Starting')

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
    Logger.happy('Wireguard file created')
    Logger.info('make_wireguard: Finished')


def make_wireguard_small():
    Logger.info('make_wireguard_small: Starting')

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

    v4, v6 = split_v4_v6(allowed_ips)
    v4 = [ip_to_cidr(ip) for ip in v4]
    v4 = simplify_cidr_list(v4, 128)
    v6 = [ip_to_cidr(ip) for ip in v6]
    v6 = simplify_cidr_list(v6, 128)

    allowed_ips = v4 + v6

    file_str += f"AllowedIPs = {', '.join(allowed_ips)}\n"
    # manaually write file

    with open('out/wireguard_small_incomplete.conf', 'w') as file:
        file.write(file_str)
    Logger.happy('Wireguard small file created')
    Logger.info('make_wireguard_small: Finished')


if __name__ == '__main__':
    LOG_LEVEL = 5
    make_wireguard()
    make_wireguard_small()