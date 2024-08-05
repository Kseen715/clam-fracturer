import ipaddress
from common import *

def maskt2ipv4():
    cidr_count = 0
    converted_ip_count = 0
    data = read_csv(db_file)
    # if ipv4 contains / then it is a masked ip range
    masked = data[data['ipv4'].str.contains('/')]
    # convert masked ip range to list of ip addresses
    ip_list = []
    for index, row in masked.iterrows():
        ip = ipaddress.ip_network(row['ipv4'])
        for i in ip.hosts():
            if row['comment']:
                comment = row['comment'] + " __CIDR_CONVERTED__"
            else:
                comment = "__CIDR_CONVERTED__"
            ip_list.append({'hostname': row['hostname'], 'ipv4': str(i), 'comment': comment})
        log_info(f'Converted {row["ipv4"]} to {ip.num_addresses} ip addresses')
        cidr_count += 1
        converted_ip_count += ip.num_addresses
    # remove masked ip range from data
    data = data[~data['ipv4'].str.contains('/')]
    # append ip list to data
    data = pd.concat([data, pd.DataFrame(ip_list)], ignore_index=True)
    write_csv(data, db_file)
    log_happy('Converted {} masked IP ranges to {} IP addresses'.format(cidr_count, converted_ip_count))

if __name__ == '__main__':
    maskt2ipv4()
