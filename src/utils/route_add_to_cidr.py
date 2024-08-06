from common import *
import ipaddress
import argparse

"""
Convert route add command to CIDR notation

route ADD 69.171.224.0 MASK 255.255.224.0 0.0.0.0 -> 
"""

def convert_route_add_to_cidr(filename):
    log_info('convert_route_add_to_cidr: Starting')
    # read route add commands
    route_add = None
    with open(filename, 'r') as f:
        route_add = f.readlines()

    # convert to CIDR notation
    cidr_list = []
    for route in route_add:
        route = route.split()
        ip = ipaddress.ip_network(f"{route[2]}/{route[4]}", strict=False)
        cidr_list.append(str(ip))
        log_info(f'Converted {route[2]} MASK {route[4]} to {str(ip)}')
    write_txt(cidr_list, 'in/cidr.txt')
    log_happy('CIDR file created')
    log_info('convert_route_add_to_cidr: Finished')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert route add command to CIDR notation')
    parser.add_argument('filename', type=str, help='Filename with route add commands')
    args = parser.parse_args()
    convert_route_add_to_cidr(args.filename)
