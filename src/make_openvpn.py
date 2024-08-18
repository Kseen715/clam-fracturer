from common import *
import ipaddress

# file openvpn_route.ovpn:
"""
route-nopull
route <ipv4> <mask>
route <ipv4> <mask>
...

"""

def make_openvpn():
    Logger.info('make_openvpn: Starting')

    data = read_csv(DB_FILE)
    # if ipv4 contains / then it is a masked ip range
    masked = data[data['ipv4'].str.contains('/')]
    # mask it as in example
    masked_ip_list = []
    masked_ip_list.append('route-nopull')
    for index, row in masked.iterrows():
        try:
            ip = ipaddress.ip_network(row['ipv4'], strict=False)
            masked_ip_list.append(f'route {ip.network_address} {ip.netmask}')
            # Logger.info(f'Converted {row["ipv4"]} to {ip.network_address} {ip.netmask}')
        except ValueError as e:
            Logger.warning(f"Invalid CIDR notation {row['ipv4']}: {e}")
            # remove invalid CIDR
            data = data[~(data['ipv4'] == row['ipv4'])]
            Logger.info(f'Dropped {row["ipv4"]} because it is invalid CIDR notation')

    # remove masked ip range from data
    data = data[~data['ipv4'].str.contains('/')]
    # append remaining ips with MASK
    for index, row in data.iterrows():
        masked_ip_list.append(f'route {row["ipv4"]} 255.255.255.255')
        # Logger.info(f'Added {row["ipv4"]}
    write_txt(masked_ip_list, 'out/openvpn_route.ovpn')
    Logger.happy('OpenVPN file created')
    Logger.info('make_openvpn: Finished')


if __name__ == '__main__':
    make_openvpn()

