import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import *
import ipaddress
import argparse

import requests
from bs4 import BeautifulSoup

# fake user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def convert_ipv4_range_into_cidr(r_left, r_right):
    # return string of CIDR notation, can be more than range
    # convert range to CIDR
    ip_left = ipaddress.IPv4Address(r_left)
    ip_right = ipaddress.IPv4Address(r_right)
    if ip_left > ip_right:
        ip_left, ip_right = ip_right, ip_left
    ip_range = list(ipaddress.summarize_address_range(ip_left, ip_right))
    return str(ip_range[0])


def parse_ip_address_of(url: str, filename: str = None):
    Logger.info('parse_ip_address_of: Starting')
    Logger.info('URL: ' + url)
    # Send a GET request to fetch the raw HTML content
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    result = []

    # find every class "col-md-5 col-sm-5"
    for row in soup.find_all('div', class_='col-md-5 col-sm-5'):
        # after every <b> tag there is a CIDR, IP range, Block size
        # data is between </b> and <br>
        temp_list = []
        for b in row.find_all('b'):
            temp_list.append(b.next_sibling.strip())

        data_dict = {
            'cidr': temp_list[0] if temp_list[0].find('N/A') == -1 else convert_ipv4_range_into_cidr(temp_list[1].split(' - ')[0], temp_list[1].split(' - ')[1]),
            'ip_range': temp_list[1],
            'block_size': temp_list[2]
        }
        result.append(data_dict['cidr'])
        Logger.info('Found CIDR: ' + data_dict['cidr'])
    Logger.happy('Found ' + str(len(result)) + ' CIDR notations for ' + url)
    if filename:
        write_txt(result, filename)
        Logger.info('Saved to ' + filename)
    Logger.info('parse_ip_address_of: Finished')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse IP addresses of a company from networksdb.io')
    parser.add_argument('url', type=str, help='URL of the company')
    parser.add_argument('--output', type=str, help='Output file')
    args = parser.parse_args()
    parse_ip_address_of(args.url, args.output)

        