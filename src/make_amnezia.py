from common import *

def make_amnezia():
    Logger.info('make_amnezia: Starting')
        
    data = read_csv(DB_FILE)
    # use ipv4 as hostname
    data['hostname'] = data['ipv4']
    # save only hostnames
    data = data[['hostname']]
    json_data = data.to_dict(orient='records')
    write_json(json_data, 'out/amnezia_vpn.json')
    Logger.happy('Amnezia VPN tunneling file created')
    Logger.info('make_amnezia: Finished')


if __name__ == '__main__':
    make_amnezia()