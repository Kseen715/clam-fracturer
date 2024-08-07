from common import *

def make_amnezia():
    log_info('make_amnezia: Starting')
        
    data = read_csv(DB_FILE)
    # use ipv4 as hostname
    data['hostname'] = data['ipv4']
    # save only hostnames
    data = data[['hostname']]
    json_data = data.to_dict(orient='records')
    write_json(json_data, 'out/amnezia_vpn.json')
    log_happy('Amnezia VPN tunneling file created')
    log_info('make_amnezia: Finished')


if __name__ == '__main__':
    make_amnezia()