import datetime, os, json
import ipaddress
# from hashlib import sha256

import pandas as pd
import colorama

# ==============================================================================
# Logger class
# by Kseen715
# v1.6
# ==============================================================================
import datetime, inspect

# To drop the following imports and whole requirements.txt file:
# ==============================================================================
# Part of colorama.py module
# ==============================================================================
# colorama's LICENSE:
"""
Copyright (c) 2010 Jonathan Hartley
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holders, nor those of its contributors
  may be used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
# 
# 
CSI = '\033['
# 
# 
def code_to_chars(code):
    return CSI + str(code) + 'm'
# 
# 
class colorama:
    class AnsiCodes(object):
        def __init__(self):
            # the subclasses declare class attributes which are numbers.
            # Upon instantiation we define instance attributes, which are the 
            # same as the class attributes but wrapped with the ANSI escape 
            # sequence
            for name in dir(self):
                if not name.startswith('_'):
                    value = getattr(self, name)
                    setattr(self, name, code_to_chars(value))
    # 
    # 
    class AnsiFore(AnsiCodes):
        BLACK           = 30
        RED             = 31
        GREEN           = 32
        YELLOW          = 33
        BLUE            = 34
        MAGENTA         = 35
        CYAN            = 36
        WHITE           = 37
        RESET           = 39
    # 
        # These are fairly well supported, but not part of the standard.
        LIGHTBLACK_EX   = 90
        LIGHTRED_EX     = 91
        LIGHTGREEN_EX   = 92
        LIGHTYELLOW_EX  = 93
        LIGHTBLUE_EX    = 94
        LIGHTMAGENTA_EX = 95
        LIGHTCYAN_EX    = 96
        LIGHTWHITE_EX   = 97
    # 
    # 
    class AnsiStyle(AnsiCodes):
        BRIGHT    = 1
        DIM       = 2
        NORMAL    = 22
        RESET_ALL = 0
    # 
    # 
    Fore   = AnsiFore()
    Style  = AnsiStyle()
# ==============================================================================
# End of colorama.py module
# ==============================================================================

LOG_LEVELS = {
        'NONE': 0,
        'ERROR': 1,
        'WARNING': 2,
        'SUCCESS': 3,
        'INFO': 4,
        'DEBUG': 5,
    }

# Log level for stdout/stderr. 
# Will be saved to the log file regardless of this setting.
LOG_LEVEL = 4

# Log file, stdout only if empty
LOG_FILE = './.logs/log.log'
LOG_FILE_MAX_SIZE = 1024 * 1024  # 1 MB
LOG_DEBUG_COLOR = colorama.Fore.LIGHTMAGENTA_EX

class Logger:
    @staticmethod
    def __custom_print__(msg: str, level: str, style: str = None, 
                         do_inspect: bool = False, 
                         inspect_stack_offset: int = 1, 
                         do_write_file: bool = True,
                         do_write_stdout: bool = True):
        """Log custom message

        Args:
            msg (str): Custom message
            level (int): Log level
            color (str): Color
        """
        msg = str(msg)
        while msg.endswith('\n'):
            msg = msg[:-1]
        if do_inspect:
            frame = inspect.stack()[inspect_stack_offset]
            file_name = frame.filename
            line_number = frame.lineno
            function_name = frame.function
            msg = f"{msg} ({file_name}:{line_number}:{function_name})"
        if LOG_FILE and do_write_file:
            if not os.path.exists(os.path.dirname(LOG_FILE)):
                os.makedirs(os.path.dirname(LOG_FILE))
            with open(LOG_FILE, 'a') as f:
                f.write(f'{datetime.datetime.now()} ' \
                        + f'[{level}] {msg}\n')
            if os.path.getsize(LOG_FILE) > LOG_FILE_MAX_SIZE * 0.9:
                with open(LOG_FILE, 'rb') as f:
                    f.seek(-LOG_FILE_MAX_SIZE, os.SEEK_END)
                    data = f.read()
                with open(LOG_FILE, 'wb') as f:
                    f.write(data)
        if do_write_stdout:
            print(f'{style}{datetime.datetime.now()} ' \
                + f'[{level}] {msg}{colorama.Style.RESET_ALL}')
        

    @staticmethod
    def __custom_input__(msg: str, level: str, style: str,
                         do_write_file: bool = True):
        """Log custom message

        Args:
            msg (str): Custom message
            color (str): Color
        """
        msg = str(msg)
        inpt = input(f'{style}{datetime.datetime.now()} ' \
                  + f'[{level}] {msg}{colorama.Style.RESET_ALL}')
        if LOG_FILE and do_write_file:
            if not os.path.exists(os.path.dirname(LOG_FILE)):
                os.makedirs(os.path.dirname(LOG_FILE))
            with open(LOG_FILE, 'a') as f:
                f.write(f'{style}{datetime.datetime.now()} ' \
                        + f'[{level}] {msg}{colorama.Style.RESET_ALL}' \
                        + inpt + '\n')
            if os.path.getsize(LOG_FILE) > LOG_FILE_MAX_SIZE * 0.9:
                with open(LOG_FILE, 'rb') as f:
                    f.seek(-LOG_FILE_MAX_SIZE, os.SEEK_END)
                    data = f.read()
                with open(LOG_FILE, 'wb') as f:
                    f.write(data)
        return inpt


    @staticmethod
    def debug(msg, do_inspect=True):
        """Log debug message

        Args:
            msg (str): Debug message
        """
        Logger.__custom_print__(msg, 'DEBUG', \
                                LOG_DEBUG_COLOR, \
                                do_inspect, 2, True, \
                                LOG_LEVEL >= LOG_LEVELS['DEBUG'])
            


    @staticmethod
    def info(msg, do_inspect=False):
        """Log info message

        Args:
            msg (str): Info message
        """
        Logger.__custom_print__(msg, 'INFO', \
                                colorama.Style.RESET_ALL, \
                                do_inspect, 2, True, \
                                LOG_LEVEL >= LOG_LEVELS['INFO'])


    @staticmethod
    def happy(msg, do_inspect=False):
        """Log happy message

        Args:
            msg (str): Happy message
        """
        Logger.__custom_print__(msg, 'SUCCESS', \
                                colorama.Fore.GREEN, \
                                do_inspect, 2, True, \
                                LOG_LEVEL >= LOG_LEVELS['SUCCESS'])


    @staticmethod
    def warning(msg, do_inspect=True):
        """Log warning message

        Args:
            msg (str): Warning message
        """
        Logger.__custom_print__(msg, 'WARNING', \
                                colorama.Fore.YELLOW, \
                                do_inspect, 2, True, \
                                LOG_LEVEL >= LOG_LEVELS['WARNING'])


    @staticmethod
    def error(msg, do_inspect=True):
        """Log error message

        Args:
            msg (str): Error message
        """
        Logger.__custom_print__(msg, 'ERROR', \
                                colorama.Fore.RED, \
                                do_inspect, 2, True, \
                                LOG_LEVEL >= LOG_LEVELS['ERROR'])


    @staticmethod
    def input(msg, do_inspect=False):
        """Log input message

        Args:
            msg (str): Input message
        """
        return Logger.__custom_input__(msg, 'INPUT', \
                                        colorama.Fore.CYAN, \
                                        do_inspect, 2)

# ==============================================================================
# End of Logger class
# ==============================================================================

DB_FILE = 'db.csv'

def read_csv(filename, include_first_line=False):
    """_summary_ Read data from csv file

    Args:
        filename (str): Name of the file to read data
        include_first_line (bool): Whether to include the first line as data

    Returns:
        pd.DataFrame: Data read from csv file
    """
    if include_first_line:
        return pd.read_csv(filename, header=0)
    return pd.read_csv(filename)


def read_txt_lbl(filename):
    """_summary_ Read data from txt file

    Args:
        filename (str): Name of the file to read data

    Returns:
        list: Data read from txt file
    """
    # delete \n and empty lines
    with open(filename, 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data if x.strip()]
    return data

def write_csv(data, filename, quoting=1):
    """_summary_ Save data to csv file

    Args:
        data (pd.DataFrame): Data to be saved
        filename (str): Name of the file to save data
    """
    # "ip","hostname","comment"
    data.to_csv(filename, index=False, quoting=quoting)


def write_txt(data, filename):
    """_summary_ Save data to txt file

    Args:
        data (list): Data to be saved
        filename (str): Name of the file to save data
    """
    with open(filename, 'w') as f:
        f.write('\n'.join(data))
        

def write_json(data, filename):
    """_summary_ Save data to json file

    Args:
        data (dict): Data to be saved
        filename (str): Name of the file to save data
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


class FastHash:
    """Manual hashing class, limited to 512 bits (64 bytes)"""
    
    def __init__(self):
        self._hash_value = [0] * 64  # Initialize a list of 64 zeros
        self._data = bytearray()

    def update(self, data):
        """Update the hash with new data"""
        self._data.extend(data)
        for i, byte in enumerate(data):
            self._hash_value[i % 64] = (self._hash_value[i % 64] + byte) % 256  # Simple hash update

    def digest(self):
        """Return the digest of the data passed to the update() method so far"""
        return bytes(self._hash_value)

    def hexdigest(self):
        """Return the hexadecimal digest of the data passed to the update() method so far"""
        return ''.join(f'{byte:02x}' for byte in self._hash_value)


def hash_file(filename):
    """Hash file

    Args:
        filename (str): Name of the file to hash

    Returns:
        bytes: Hash of the file in bytes
    """
    hasher = FastHash()
    with open(filename, 'rb') as f:
        hasher.update(f.read())
    return hasher.digest()
    

def hash_str(string):
    """Hash string

    Args:
        string (str): String to hash

    Returns:
        bytes: Hash of the string
    """
    hasher = FastHash()
    hasher.update(string.encode())
    return hasher.digest()


def save_hash_binary(new_hash_bytes, new_hash_filename):
    """_summary_ Save hash of binary data to file

    Args:
        data (bytes): Binary data to hash
        filename (str): Name of the file to save hash
    """
    # if folder for hashes does not exist, create it
    if not os.path.exists(os.path.dirname(new_hash_filename)):
        os.makedirs(os.path.dirname(new_hash_filename))
    with open(new_hash_filename, 'wb') as f:
        f.write(new_hash_bytes)
    Logger.info(f'Saved hash to {new_hash_filename}')

    
def read_file_binary(filename):
    """_summary_ Read binary data from file

    Args:
        filename (str): Name of the file to read data

    Returns:
        bytes: Binary data read from file
    """
    with open(filename, 'rb') as f:
        return f.read()
    
def check_hash_binary(new_hash_bytes, old_hash_filename):
    """_summary_ Check hash of binary data

    Args:
        data (bytes): Binary data to hash
        filename (str): Name of the file to check hash

    Returns:
        bool: Whether the hash matches
    """
    return new_hash_bytes == read_file_binary(old_hash_filename)


def is_cidr_valid(cidr: str):
    """_summary_ Check if CIDR is valid

    Args:
        cidr (str): CIDR to check

    Returns:
        bool: Whether the CIDR is valid
    """
    if '.' in cidr:
        if '/' not in cidr:
            return False
        ip, mask = cidr.split('/')
        mask = int(mask) # how much bits can be non-zero, from start
        ip = [int(x) for x in ip.split('.')]

        if len(ip) != 4:
            return False
        # check if all bits after mask are zero
        _str_ip = ''.join(f'{x:08b}' for x in ip)
        # drop first mask bits
        str_ip = _str_ip[mask:]
        # check if there are any non-zero bits
        for bit in str_ip:
            if bit != '0':
                return False
        return True
    elif ':' in cidr:
        if '/' not in cidr:
            return False
        ip, mask = cidr.split('/')
        mask = int(mask)
        ip = ip.split(':')
        # remove empty strings
        ip = [x for x in ip if x]

        if len(ip) != 8:
            # expand with zeros
            ip = [x if x else '0000' for x in ip]
        ip = [int(x, 16) for x in ip]
        _str_ip = ''.join(f'{x:016b}' for x in ip)
        # drop first mask bits
        str_ip = _str_ip[mask:]
        # check if there are any non-zero bits
        for bit in str_ip:
            if bit != '0':
                return False
        return True
    
    return False


def cidr_size(cidr: str) -> int:
    """_summary_ Get CIDR size

    Args:
        cidr (str): CIDR to get size

    Returns:
        int: Size of the CIDR
    """
    if '.' in cidr:
        ip, mask = cidr.split('/')
        mask = int(mask)
        return 2 ** (32 - mask)
    elif ':' in cidr:
        ip, mask = cidr.split('/')
        mask = int(mask)
        return 2 ** (128 - mask)
    return 0


def ip_full(ip: str) -> str:
    """_summary_ Get full IP

    Args:
        ip (str): IP to get full

    Returns:
        str: Full IP
    """
    if '.' in ip:
        try:
            ip = ipaddress.IPv4Address(ip)
            return str(ip.exploded)
        except ipaddress.AddressValueError:
            Logger.warning(f'Invalid IPv4 address: {ip}')
            return ''
    elif ':' in ip:
        try:
            ip = ipaddress.IPv6Address(ip)
            return str(ip.exploded)
        except ipaddress.AddressValueError:
            Logger.warning(f'Invalid IPv6 address: {ip}')
            return ''
    Logger.warning(f'Invalid IP address: {ip}')
    return ''




def ip_short(ip: str) -> str:
    """_summary_ Get short IP
    aka remove only-zero octets

    Args:
        ip (str): IP to get short

    Returns:
        str: Short IP
    """
    if '.' in ip:
        try:
            ipv4 = ipaddress.IPv4Address(ip)
            return str(ipv4.compressed)
        except ipaddress.AddressValueError:
            Logger.warning(f'Invalid IPv4 address: {ip}')
            return ''
    elif ':' in ip:
        try:
            ipv6 = ipaddress.IPv6Address(ip)
            return str(ipv6.compressed)
        except ipaddress.AddressValueError:
            Logger.warning(f'Invalid IPv6 address: {ip}')
            return ''
    Logger.warning(f'Invalid IP address: {ip}')
    return ''
    

def cidr_full(cidr: str) -> str:
    """_summary_ Get full CIDR

    Args:
        cidr (str): CIDR to get full

    Returns:
        str: Full CIDR
    """
    if '.' in cidr:
        ip, mask = cidr.split('/')
        mask = int(mask)
        ip = ip_full(ip)
        return f'{ip}/{mask}'
    elif ':' in cidr:
        ip, mask = cidr.split('/')
        mask = int(mask)
        ip = ip_full(ip)
        return f'{ip}/{mask}'
    Logger.warning(f'Invalid CIDR: {cidr}')
    return ''


def cidr_short(cidr: str) -> str:
    """_summary_ Get short CIDR
    aka remove only-zero octets

    Args:
        cidr (str): CIDR to get short

    Returns:
        str: Short CIDR
    """
    if '.' in cidr:
        ip, mask = cidr.split('/')
        ip = ip_short(ip)
        return f'{ip}/{mask}'
    elif ':' in cidr:
        ip, mask = cidr.split('/')
        ip = ip_short(ip)
        return f'{ip}/{mask}'
    Logger.warning(f'Invalid CIDR: {cidr}')
    return ''


def ip_dec(ip: str) -> int:
    """_summary_ Convert IP to decimal

    Args:
        ip (str): IP to convert

    Returns:
        int: Decimal IP
    """
    ip = ip_full(ip)
    if '.' in ip:
        ip = ip.split('.')
        ip = [int(x) for x in ip]
        return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]
    elif ':' in ip:
        ip = ip.split(':')
        ip = [int(x, 16) for x in ip]
        return ip[0] << 112 | ip[1] << 96 | ip[2] << 80 | ip[3] << 64 | \
            ip[4] << 48 | ip[5] << 32 | ip[6] << 16 | ip[7]
    return 0


def __ip_dec_unsafe(ip: str) -> int:
    """_summary_ Convert IP to decimal

    Args:
        ip (str): IP to convert

    Returns:
        int: Decimal IP
    """
    if '.' in ip:
        ip = ip.split('.')
        ip = [int(x) for x in ip]
        return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]
    else:
        ip = ip.split(':')
        ip = [int(x, 16) for x in ip]
        return ip[0] << 112 | ip[1] << 96 | ip[2] << 80 | ip[3] << 64 | \
            ip[4] << 48 | ip[5] << 32 | ip[6] << 16 | ip[7]


def __ip_dec_unsafe_from_bits(ip_bits: str) -> int:
    """_summary_ Convert IP to decimal

    Args:
        ip_bits (str): IP to convert

    Returns:
        int: Decimal IP
    """
    return int(ip_bits, 2)


def cidr_range(cidr: str) -> str:
    """_summary_ Get CIDR range
    xxx.xxx.xxx.xxx/xx -> xxx.xxx.xxx.xxx - xxx.xxx.xxx.xxx
    xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xx -> 
        xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx - 
            xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx

    Args:
        cidr (str): CIDR to get range

    Returns:
        str: Range of the CIDR
    """
    cidr = cidr_full(cidr)
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        return f"{network.network_address} - {network.broadcast_address}"
    except ipaddress.AddressValueError:
        Logger.warning(f'Invalid CIDR: {cidr}')
        return ''


def compute_cidr_dist(cidr_left: str, cidr_right: str) -> int:
    """_summary_ Compute distance between two CIDRs

    Args:
        cidr_left (str): Left CIDR
        cidr_right (str): Right CIDR

    Returns:
        int: Distance between the two CIDRs
    """
    if ('.' in cidr_left and ':' in cidr_right) or \
        (':' in cidr_left and '.' in cidr_right): 
        Logger.warning('IP version mismatch')
    left_network = ipaddress.IPv4Network(cidr_left)
    right_network = ipaddress.IPv4Network(cidr_right)
    if left_network > right_network:
        left_network, right_network = right_network, left_network
    left_network = left_network.network_address
    right_network = right_network.broadcast_address
    return __ip_dec_unsafe(str(right_network)) - __ip_dec_unsafe(str(left_network)) + 1


def __compute_cidr_dist_unsafe(cidr_left: str, cidr_right: str) -> int:
    """_summary_ Compute distance between two CIDRs

    Args:
        cidr_left (str): Left CIDR
        cidr_right (str): Right CIDR

    Returns:
        int: Distance between the two CIDRs
    """
    ip1, mask1 = cidr_left.split('/')
    ip2, mask2 = cidr_right.split('/')
    if '.' in ip1:
        ip_bits1 = ''.join(f'{int(x):08b}' for x in ip1.split('.'))
        ip_bits2 = ''.join(f'{int(x):08b}' for x in ip2.split('.'))
        # crop ip_bits1 by mask and add zeros
        ip_bits1 = ip_bits1[:int(mask1)] + '0' * (32 - int(mask1))
        # crop ip_bits2 by mask and add ones
        ip_bits2 = ip_bits2[:int(mask2)] + '1' * (32 - int(mask2))
        # convert back
        return abs(__ip_dec_unsafe_from_bits(ip_bits2) - __ip_dec_unsafe_from_bits(ip_bits1)) + 1
    else:
        ip_bits1 = ''.join(f'{int(x, 16):016b}' for x in ip1.split(':'))
        ip_bits2 = ''.join(f'{int(x, 16):016b}' for x in ip2.split(':'))
        # crop ip_bits1 by mask and add zeros
        ip_bits1 = ip_bits1[:int(mask1)] + '0' * (128 - int(mask1))
        # crop ip_bits2 by mask and add ones
        ip_bits2 = ip_bits2[:int(mask2)] + '1' * (128 - int(mask2))
        # convert back
        return abs(__ip_dec_unsafe_from_bits(ip_bits2) - __ip_dec_unsafe_from_bits(ip_bits1)) + 1
    
    # if '.' in ip1:
    #     ip_bits1 = ''.join(f'{int(x):08b}' for x in ip1.split('.'))
    #     ip_bits2 = ''.join(f'{int(x):08b}' for x in ip2.split('.'))
    #     # crop ip_bits1 by mask and add zeros
    #     ip_bits1 = ip_bits1[:int(mask1)] + '0' * (32 - int(mask1))
    #     # crop ip_bits2 by mask and add ones
    #     ip_bits2 = ip_bits2[:int(mask2)] + '1' * (32 - int(mask2))
    #     # convert back
    #     ip1 = '.'.join(str(int(ip_bits1[i:i+8], 2)) for i in range(0, 32, 8))
    #     ip2 = '.'.join(str(int(ip_bits2[i:i+8], 2)) for i in range(0, 32, 8))
    #     return abs(__ip_dec_unsafe(ip2) - __ip_dec_unsafe(ip1)) + 1
    # else:
    #     ip_bits1 = ''.join(f'{int(x, 16):016b}' for x in ip1.split(':'))
    #     ip_bits2 = ''.join(f'{int(x, 16):016b}' for x in ip2.split(':'))
    #     # crop ip_bits1 by mask and add zeros
    #     ip_bits1 = ip_bits1[:int(mask1)] + '0' * (128 - int(mask1))
    #     # crop ip_bits2 by mask and add ones
    #     ip_bits2 = ip_bits2[:int(mask2)] + '1' * (128 - int(mask2))
    #     # convert back
    #     ip1 = ':'.join(hex(int(ip_bits1[i:i+16], 2))[2:] for i in range(0, 128, 16))
    #     ip2 = ':'.join(hex(int(ip_bits2[i:i+16], 2))[2:] for i in range(0, 128, 16))
    #     return abs(__ip_dec_unsafe(ip2) - __ip_dec_unsafe(ip1)) + 1
    # left_network = ipaddress.IPv4Network(cidr_left)
    # right_network = ipaddress.IPv4Network(cidr_right)
    # left_network = left_network.network_address
    # right_network = right_network.broadcast_address
    # return abs(__ip_dec_unsafe(str(right_network)) - __ip_dec_unsafe(str(left_network))) + 1


def cidr_clamp(cidr_left: str, cidr_right: str) -> str:
    """_summary_ Clamp two CIDRs into singe one, result may include additional IPs

    Args:
        cidr_left (str): Left CIDR
        cidr_right (str): Right CIDR

    Returns:
        str: Clamped CIDR
    """
    if ('.' in cidr_left and ':' in cidr_right) or \
        (':' in cidr_left and '.' in cidr_right): 
        Logger.warning('IP version mismatch')
    left_network = ipaddress.IPv4Network(cidr_left)
    right_network = ipaddress.IPv4Network(cidr_right)
    if left_network > right_network:
        left_network, right_network = right_network, left_network
    cidr_left = left_network.exploded
    cidr_right = right_network.exploded
    # grab left netowrk and slap right mask on it
    new_cidr = f'{left_network.network_address}/{right_network.prefixlen}'
    # check if right network is in new_cidr
    ip, mask = new_cidr.split('/')
    ip_bits = ''.join(f'{int(x):08b}' for x in ip.split('.'))
    real_ip_bits = ip_bits[:int(mask)] + '0' * (32 - int(mask))
    # convert back to ip
    new_cidr = '.'.join(str(int(real_ip_bits[i:i+8], 2)) for i in range(0, 32, 8))
    new_cidr = f'{new_cidr}/{mask}'
    
    i = -1
    while not ipaddress.IPv4Network(new_cidr).overlaps(right_network):
        # if not, add +1 to the mask
        new_cidr = f'{left_network.network_address}/{left_network.prefixlen + i}'
        i -= 1
        # set host bits to 0
        # get bist as string
        ip, mask = new_cidr.split('/')
        ip_bits = ''.join(f'{int(x):08b}' for x in ip.split('.'))
        real_ip_bits = ip_bits[:int(mask)] + '0' * (32 - int(mask))
        # convert back to ip
        new_cidr = '.'.join(str(int(real_ip_bits[i:i+8], 2)) for i in range(0, 32, 8))
        new_cidr = f'{new_cidr}/{mask}'

    Logger.debug(f'Clamped {cidr_left} and {cidr_right} into {new_cidr} (dist: {compute_cidr_dist(cidr_left, cidr_right)})')

    return new_cidr

    # if '.' in cidr:
    #     if '/' not in cidr:
    #         return False
    #     ip, mask = cidr.split('/')
    #     mask = int(mask) # how much bits can be non-zero, from start
    #     ip = [int(x) for x in ip.split('.')]

    #     if len(ip) != 4:
    #         return False
    #     # check if all bits after mask are zero
    #     _str_ip = ''.join(f'{x:08b}' for x in ip)
    #     # drop first mask bits
    #     str_ip = _str_ip[mask:]
    #     # check if there are any non-zero bits
    #     for bit in str_ip:
    #         if bit != '0':
    #             return False

def is_ip_in_cidr(ip: str, cidr: str) -> bool:
    """_summary_ Check if IP is in CIDR

    Args:
        ip (str): IP to check
        cidr (str): CIDR to check

    Returns:
        bool: Whether IP is in CIDR
    """
    ip = ip_full(ip)
    cidr = cidr_full(cidr)
    try:
        ip = ipaddress.ip_address(ip)
        cidr = ipaddress.ip_network(cidr, strict=False)
        return ip in cidr
    except ipaddress.AddressValueError:
        Logger.warning(f'Invalid IP or CIDR: {ip} or {cidr}')
        return False
    

def compute_cidr_dist_table(cidr_list: list):
    """Compute distance table between CIDRs

    Args:
        cidr_list (list): List of CIDRs

    Returns:
        list: Distance table between CIDRs
    """
    n = len(cidr_list)
    table = [[-1] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = None
            if i == j:
                dist = -1
            else:
                dist = __compute_cidr_dist_unsafe(cidr_list[i], cidr_list[j])
            table[i][j] = dist
            table[j][i] = dist
    return table


def simplify_cidr_list(cidr_list: list, max_list_size: int) -> list:
    """_summary_ Simplify CIDR list

    Args:
        cidr_list (list): List of CIDRs to simplify

    Returns:
        list: Simplified list of CIDRs
    """
    Logger.info('simplify_cidr_list: Starting')
    current_list_size = len(cidr_list)
    Logger.info(f'Simplifying CIDR list of size {current_list_size} to {max_list_size}')
    while current_list_size > max_list_size:
        Logger.info(f'Size: {current_list_size} -> {max_list_size}')
        # TODO: tal can accept only ip, not full cidr.
        # TODO: tal can accept ip in binary format, not str, that could 
        #      speed up the process dramatically
        tal = compute_cidr_dist_table(cidr_list)
        min_dist = 1 << 32
        min_i = -1
        min_j = -1
        for i in range(len(tal)):
            for j in range(i + 1, len(tal)):
                if tal[i][j] < min_dist:
                    min_dist = tal[i][j]
                    min_i = i
                    min_j = j
        new_cidr = cidr_clamp(cidr_list[min_i], cidr_list[min_j])
        cidr_list[min_i] = new_cidr
        cidr_list.pop(min_j)
        current_list_size -= 1
    Logger.info('simplify_cidr_list: Finished')
    return cidr_list   

def ip_to_cidr(ip: str) -> str:
    """_summary_ Convert IP to CIDR

    Args:
        ip (str): IP to convert

    Returns:
        str: CIDR
    """
    if '/' in ip:
        return ip
    ip = ip_full(ip)
    if '.' in ip:
        ip = ip.split('.')
        ip = [int(x) for x in ip]
        mask = 32
        for i in range(4):
            if ip[i] == 0:
                mask -= 8
            else:
                break
        return f'{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}/{mask}'
    elif ':' in ip:
        ip = ip.split(':')
        ip = [int(x, 16) for x in ip]
        mask = 128
        for i in range(8):
            if ip[i] == 0:
                mask -= 16
            else:
                break
        return f'{ip[0]:x}:{ip[1]:x}:{ip[2]:x}:{ip[3]:x}:{ip[4]:x}:{ip[5]:x}:{ip[6]:x}:{ip[7]:x}/{mask}'
    return ''


def split_v4_v6(cidr_list: list) -> tuple:
    """_summary_ Split CIDR list into IPv4 and IPv6

    Args:
        cidr_list (list): List of CIDRs

    Returns:
        tuple: Tuple of IPv4 and IPv6 CIDRs
    """
    v4 = []
    v6 = []
    for cidr in cidr_list:
        if '.' in cidr:
            v4.append(cidr)
        elif ':' in cidr:
            v6.append(cidr)
    return v4, v6


if __name__ == '__main__':
    LOG_LEVEL = 5
    LOG_DEBUG_COLOR = colorama.Fore.LIGHTCYAN_EX

    Logger.debug('common.py: Testing')
    Logger.debug(cidr_size('192.162.1.1/16'))
    Logger.debug(cidr_size('192.162.1.1/24'))
    Logger.debug(ip_full('192.162.1.1'))
    Logger.debug('ip_full: ' + ip_full('fc02::8f8a:bfab:eb50:5031'))
    Logger.debug('ip_short: ' + ip_short(ip_full('fc02::8f8a:bfab:eb50:5031')))
    Logger.debug('cidr_full: ' + cidr_full('fc02::8f8a:bfab:eb50:5031/7'))
    Logger.debug('cidr_short: ' + cidr_short(cidr_full('fc02::8f8a:bfab:eb50:5031/7')))
    Logger.debug('ip_dec: ' + str(ip_dec('192.162.1.1'))) # 3231842561
    Logger.debug('ip_dec: ' + str(ip_dec('fc02::8f8a:bfab:eb50:5031'))) # 334975839531515869637359730422623260721
    Logger.debug(cidr_size('192.162.1.1/30'))
    Logger.debug(cidr_range('192.162.1.1/30'))
    Logger.debug(cidr_size('fc02::8f8a:bfab:eb50:5031/11'))
    Logger.debug(cidr_range('fc02::8f8a:bfab:eb50:5031/11'))
    Logger.debug(compute_cidr_dist('216.58.192.0/20', '216.58.208.0/21'))
    # Logger.debug(dec_ip('fc02::8f8a:bfab:eb50:5031'))
    # test is_cidr_valid
    Logger.debug(cidr_size('216.58.192.0/20'))
    Logger.debug(cidr_size('216.58.208.0/21'))
    range_l = cidr_range('216.58.192.0/20').split(' - ')
    range_r = cidr_range('216.58.208.0/21').split(' - ')
    Logger.debug(range_l)
    Logger.debug(range_r)
    new_range = cidr_range(cidr_clamp('216.58.192.0/20', '216.58.208.0/21')).split(' - ')
    Logger.debug(cidr_clamp('216.58.192.0/20', '216.58.208.0/21'))
    Logger.debug(new_range)
    Logger.debug(cidr_size(cidr_clamp('216.58.192.0/20', '216.58.208.0/21')))
    ll = ['216.58.192.0/20', '216.58.208.0/21', '216.58.217.0/24', '216.58.220.0/22', '220.181.174.0/24', '23.101.24.0/24', '23.202.231.0/24', '23.217.138.0/24', '23.225.141.0/24', '23.234.30.0/24', '23.236.48.0/20', '23.251.128.0/19', '31.13.106.0/24', '31.13.112.0/24', '31.13.64.0/24', '31.13.67.0/24', '31.13.68.0/22', '31.13.73.0/24', '31.13.75.0/24', '31.13.76.0/24', '31.13.80.0/21']
    ll = [x for x in ll if is_cidr_valid(x)]
    Logger.debug((len(ll), ll))
    ll = simplify_cidr_list(ll, 4)
    Logger.debug((len(ll), ll))