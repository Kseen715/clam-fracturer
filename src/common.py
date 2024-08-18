import datetime, os, json
# from hashlib import sha256

import pandas as pd
import colorama

# ==============================================================================
# Logger class
# by Kseen715
# v1.5
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
        while msg.endswith('\n'):
            msg = msg[:-1]
        if do_inspect:
            frame = inspect.stack()[inspect_stack_offset]
            file_name = frame.filename
            line_number = frame.lineno
            msg = f"{msg} ({file_name}:{line_number})"
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
                                colorama.Fore.LIGHTMAGENTA_EX, \
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
    def warning(msg, do_inspect=False):
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
                Logger.info(f'{str_ip}')
                Logger.info(f'{_str_ip}')
                Logger.info(f'{"1" * mask}' + '0' * (32 - mask))
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
                Logger.info(f'{str_ip}')
                Logger.info(f'{_str_ip}')
                Logger.info(f'{"1" * mask}' + '0' * (128 - mask))
                return False
        return True
    
    return False