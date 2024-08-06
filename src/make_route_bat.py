from common import *
import ipaddress

"""
make file as in example

route ADD 31.13.24.0 MASK 255.255.248.0 0.0.0.0
route ADD 31.13.64.0 MASK 255.255.192.0 0.0.0.0
route ADD 45.64.40.0 MASK 255.255.252.0 0.0.0.0
route ADD 66.220.144.0 MASK 255.255.240.0 0.0.0.0
route ADD 69.63.176.0 MASK 255.255.240.0 0.0.0.0
route ADD 69.171.224.0 MASK 255.255.224.0 0.0.0.0
route ADD 74.119.76.0 MASK 255.255.252.0 0.0.0.0
route ADD 103.4.96.0 MASK 255.255.252.0 0.0.0.0
route ADD 129.134.0.0 MASK 255.255.0.0 0.0.0.0
route ADD 157.240.0.0 MASK 255.255.128.0 0.0.0.0
route ADD 173.252.64.0 MASK 255.255.192.0 0.0.0.0
route ADD 179.60.192.0 MASK 255.255.252.0 0.0.0.0
route ADD 185.60.216.0 MASK 255.255.252.0 0.0.0.0
route ADD 157.240.238.4 MASK 255.255.255.255 0.0.0.0
route ADD 157.240.253.35 MASK 255.255.255.255 0.0.0.0
route ADD 157.240.251.18 MASK 255.255.255.255 0.0.0.0
route ADD 157.240.251.9 MASK 255.255.255.255 0.0.0.0
route ADD 157.240.251.5 MASK 255.255.255.255 0.0.0.0
route ADD 157.240.238.37 MASK 255.255.255.255 0.0.0.0

if ipv4 contains / then it is a masked ip range, create correct mask fot that
if ipv4 not contain / then it is a single ip address, just add it to route
"""

def make_route_bat():
    log_info('make_route_bat: Starting')
    data = read_csv(DB_FILE)
    # if ipv4 contains / then it is a masked ip range
    masked = data[data['ipv4'].str.contains('/')]
    # mask it as in example
    masked_ip_list = []
    for index, row in masked.iterrows():
        try:
            ip = ipaddress.ip_network(row['ipv4'], strict=False)
            masked_ip_list.append(f'route ADD {ip.network_address} MASK {ip.netmask} {ip.hostmask}')
            # log_info(f'Converted {row["ipv4"]} to {ip.network_address} MASK {ip.netmask} {ip.hostmask}')
        except ValueError as e:
            log_warning(f"Invalid CIDR notation {row['ipv4']}: {e}")
            # remove invalid CIDR
            data = data[~(data['ipv4'] == row['ipv4'])]
            log_info(f'Dropped {row["ipv4"]} because it is invalid CIDR notation')

    # remove masked ip range from data
    data = data[~data['ipv4'].str.contains('/')]
    # append remaining ips with MASK 255.255.255.255 0.0.0.0
    for index, row in data.iterrows():
        masked_ip_list.append(f'route ADD {row["ipv4"]} MASK 255.255.255.255 0.0.0.0')
        # log_info(f'Added {row["ipv4"]} MASK 255.255.255.255 0.0.0.0')

    write_txt(masked_ip_list, 'out/route_add.bat')
    log_happy('Route file created')
    log_info('make_route_bat: Finished')


if __name__ == '__main__':
    make_route_bat()

                        
