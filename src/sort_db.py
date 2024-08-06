from common import *
import ipaddress
import os
from os import listdir
from os.path import isfile, join


def drop_duplicates(data):
    log_info('drop_duplicates: Starting')
    # if there is ip address and CIDR that contains that address, remove solo ip address
    original_data = data.copy()
    
    cidr_data = data[data['ipv4'].str.contains('/')]
    not_cidr_data = data[~data['ipv4'].str.contains('/')]

    for index, row in cidr_data.iterrows():
        ip = ipaddress.ip_network(row['ipv4'])
        for i in ip.hosts():
            if str(i) in not_cidr_data['ipv4'].values:
                not_cidr_data = not_cidr_data[~(not_cidr_data['ipv4'].astype(str) == str(i))]
                log_info(f'Dropped {str(i)} because it is included in {row["ipv4"]}')
    data = pd.concat([not_cidr_data, cidr_data], ignore_index=True)
    if len(original_data) != len(data):
        log_happy(f"Dropped {len(original_data) - len(data)} duplicate IP addresses")
    log_info('drop_duplicates: Finished')
    return data


def sort_db():
    log_info('sort_db: Starting')
    data = read_csv(DB_FILE)
    data = data.sort_values(by=['hostname', 'ipv4', 'comment'])
    data = drop_duplicates(data)
    write_csv(data, DB_FILE)
    log_happy('Database sorted')
    log_info('sort_db: Finished')


def drop_duplicates_in_known(data):
    log_info("drop_duplicates_in_known: Starting")
    original_data = data.copy()

    cidr_data = data[data.iloc[:, 0].astype(str).str.contains('/')]
    not_cidr_data = data[~data.iloc[:, 0].astype(str).str.contains('/')]
    
    log_info(f"Initial CIDR data count: {len(cidr_data)}")
    log_info(f"Initial non-CIDR data count: {len(not_cidr_data)}")

    cidr_ips = set()
    for cidr in cidr_data.iloc[:, 0]:
        ip_network = ipaddress.ip_network(cidr)
        cidr_ips.update(str(ip) for ip in ip_network.hosts())

    not_cidr_data = not_cidr_data[~not_cidr_data.iloc[:, 0].astype(str).isin(cidr_ips)]

    dropped_ips = set(original_data.iloc[:, 0].astype(str)) - set(not_cidr_data.iloc[:, 0].astype(str)) - set(cidr_data.iloc[:, 0].astype(str))
    for ip in dropped_ips:
        log_info(f'Dropped {ip} because it is included in a CIDR range')

    data = pd.concat([not_cidr_data, cidr_data], ignore_index=True)
    if len(original_data) != len(data):
        log_happy(f"Dropped {len(original_data) - len(data)} duplicate IP addresses")
    
    log_info("drop_duplicates_in_known: Finished")
    return data


def sort_known():
    log_info("sort_known: Starting")
    onlyfiles = [f for f in listdir('in/known') if isfile(join('in/known', f))]
    log_info(f"Found {len(onlyfiles)} files in 'in/known' directory")

    for file in onlyfiles:
        log_info(f"Processing file: {file}")
        data = read_txt_lbl(f'in/known/{file}')
        data = pd.DataFrame(data, columns=[data[0].split(',')[0]])
        log_info(f"Read {len(data)} rows from {file}")
        
        data = drop_duplicates_in_known(data)
        data = data.sort_values(by=[data.columns[0]])
        write_csv(data, f'in/known/{file}', quoting=0)
        log_happy(f'{file} sorted')
    
    log_info("sort_known: Finished")


if __name__ == '__main__':
    sort_db()
    sort_known()