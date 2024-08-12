from common import *
import ipaddress
import os
from os import listdir
from os.path import isfile, join
import pandas as pd


def drop_duplicates(data):
    log_info('drop_duplicates: Starting')
    # if there is ip address and CIDR that contains that address, remove solo ip address
    original_data = data.copy()
    
    cidr_data = data[data['ipv4'].str.contains('/')]
    not_cidr_data = data[~data['ipv4'].str.contains('/')]
    for index, row in cidr_data.iterrows():
        try:
            ip_net = ipaddress.ip_network(row['ipv4'], strict=False)
            not_cidr_data.loc[:, 'ipv4'] = not_cidr_data['ipv4'].apply(lambda x: None if ipaddress.ip_address(x) in ip_net else x)
            not_cidr_data = not_cidr_data.dropna(subset=['ipv4'])
        except ValueError as e:
            log_warning(f"Invalid CIDR notation {row['ipv4']}: {e}")
            # remove invalid CIDR
            cidr_data = cidr_data[~(cidr_data['ipv4'] == row['ipv4'])]
            log_info(f'Dropped {row["ipv4"]} because it is invalid CIDR notation')
    
    data = pd.concat([not_cidr_data, cidr_data], ignore_index=True)
    if len(original_data) != len(data):
        log_happy(f"Dropped {len(original_data) - len(data)} duplicate IP addresses")
    log_info('drop_duplicates: Finished')
    return data


def sort_db():
    log_info('sort_db: Starting')
    # save_hash_binary(hash_file(DB_FILE), './hashes/' + DB_FILE + '.hash')
    if os.path.exists('./hashes/' + DB_FILE + '.hash'):
        if not check_hash_binary(hash_file(DB_FILE), './hashes/' + DB_FILE + '.hash'):
            log_warning('Database file has been modified')
        else:
            log_info('Database file has not been modified')
            return
    else:
        log_warning('No hash file found for database')
    data = read_csv(DB_FILE)
    data = data.sort_values(by=['hostname', 'ipv4', 'comment'])
    data = data.drop_duplicates(subset=['ipv4'])
    data = drop_duplicates(data)
    write_csv(data, DB_FILE)
    log_happy('Database sorted')
    save_hash_binary(hash_file(DB_FILE), './hashes/' + DB_FILE + '.hash')
    log_info('sort_db: Finished')
    


def drop_duplicates_in_known(data):
    log_info("drop_duplicates_in_known: Starting")
    original_data = data.copy()

    cidr_data = data[data.iloc[:, 0].astype(str).str.contains('/')]
    not_cidr_data = data[~data.iloc[:, 0].astype(str).str.contains('/')]

    log_info(f"Initial CIDR data count: {len(cidr_data)}")
    log_info(f"Initial non-CIDR data count: {len(not_cidr_data)}")
    if len(not_cidr_data) == 0:
        log_info("No non-CIDR data found")
    else:
        for cidr in cidr_data.iloc[:, 0]:
            try:
                ip_network = ipaddress.ip_network(cidr, strict=False)
                not_cidr_data['ipv4'] = not_cidr_data.iloc[:, 0].apply(lambda x: None if ipaddress.ip_address(x) in ip_network else x)
                not_cidr_data = not_cidr_data.dropna(subset=[not_cidr_data.columns[0]])
            except ValueError as e:
                log_warning(f"Invalid CIDR notation {cidr}: {e}")
                # remove invalid CIDR
                cidr_data = cidr_data[~(cidr_data.iloc[:, 0].astype(str) == cidr)]
                log_info(f'Dropped {cidr} because it is invalid CIDR notation')

    data = pd.concat([not_cidr_data, cidr_data], ignore_index=True)
    if len(original_data) != len(data):
        log_happy(f"Dropped {len(original_data) - len(data)} duplicate IP addresses")

    log_info("drop_duplicates_in_known: Finished")
    return data


def sort_known():
    log_info("sort_known: Starting")
    onlyfiles = [f for f in listdir('in/known') if isfile(join('in/known', f))]
    log_info(f"Found {len(onlyfiles)} files in 'in/known' directory")
    fname = 'fake_name'
    for file in onlyfiles:
        log_info(f"Processing file: {file}")
        if os.path.exists(f'./hashes/{file}.hash'):
            if not check_hash_binary(hash_file(f'in/known/{file}'), f'./hashes/{file}.hash'):
                log_warning(f'{file} has been modified')
            else:
                log_info(f'{file} has not been modified')
                continue
        else:
            log_warning(f'No hash file found for {file}')

        data = read_txt_lbl(f'in/known/{file}')
        # add first line with column name
        # data = [fname] + data
        # print(data)

        # exit(0)
        data = pd.DataFrame(data, columns=[data[0].split(',')[0]])
        log_info(f"Read {len(data)} rows from {file}")
        
        data = drop_duplicates_in_known(data)
        data = data.sort_values(by=[data.columns[0]])

        # drop all line with fname
        data = data[data[data.columns[0]] != fname]
        write_txt(data.iloc[:, 0].tolist(), f'in/known/{file}')
        save_hash_binary(hash_file(f'in/known/{file}'), f'./hashes/{file}.hash')
        log_happy(f'{file} sorted')
    
    log_info("sort_known: Finished")


if __name__ == '__main__':
    sort_known()
    sort_db()