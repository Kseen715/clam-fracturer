from common import *

def make_amnezia():
    data = read_csv(db_file)
    # use ipv4 as hostname
    data['hostname'] = data['ipv4']
    # save only hostnames
    data = data[['hostname']]
    json_data = data.to_dict(orient='records')
    write_json(json_data, 'out/amnezia_vpn.json')
    log_happy('Amnezia VPN tunneling file created')

if __name__ == '__main__':
    make_amnezia()