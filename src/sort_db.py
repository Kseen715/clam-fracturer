from common import *
import ipaddress

def drop_duplicates(data):
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
    return data

def sort_db():
    data = read_csv(db_file)
    data = data.sort_values(by=['hostname'])
    data = drop_duplicates(data)
    write_csv(data, db_file)
    log_happy('Database sorted')

if __name__ == '__main__':
    sort_db()