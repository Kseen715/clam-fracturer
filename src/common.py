import pandas as pd
import json
import colorama
import datetime
# from hashlib import sha256


DB_FILE = 'db.csv'


LOG_LEVELS = {
    'NONE': 0,
    'ERROR': 1,
    'WARNING': 2,
    'SUCCESS': 3,
    'INFO': 4,
}


LOG_LEVEL = LOG_LEVELS['INFO']


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


def log_happy(msg):
    """_summary_ Log happy message

    Args:
        msg (str): Happy message
    """
    if LOG_LEVEL >= LOG_LEVELS['SUCCESS']:
        print(f'{colorama.Fore.GREEN}{datetime.datetime.now()} [SUCCESS] {msg}{colorama.Style.RESET_ALL}')


def log_info(msg):
    """_summary_ Log info message

    Args:
        msg (str): Info message
    """
    if LOG_LEVEL >= LOG_LEVELS['INFO']:
        print(f'{colorama.Style.RESET_ALL}{datetime.datetime.now()} [INFO] {msg}{colorama.Style.RESET_ALL}')


def log_warning(msg):
    """_summary_ Log warning message

    Args:
        msg (str): Warning message
    """
    if LOG_LEVEL >= LOG_LEVELS['WARNING']:
        print(f'{colorama.Fore.YELLOW}{datetime.datetime.now()} [WARNING] {msg}{colorama.Style.RESET_ALL}')


def log_error(msg):
    """_summary_ Log error message

    Args:
        msg (str): Error message
    """
    if LOG_LEVEL >= LOG_LEVELS['ERROR']:
        print(f'{colorama.Fore.RED}{datetime.datetime.now()} [ERROR] {msg}{colorama.Style.RESET_ALL}')


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
    with open(filename, 'rb', encoding='utf-8') as f:
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
    with open(new_hash_filename, 'wb', encoding='utf-8') as f:
        f.write(new_hash_bytes)
    log_info(f'Saved hash to {new_hash_filename}')

    
def read_file_binary(filename):
    """_summary_ Read binary data from file

    Args:
        filename (str): Name of the file to read data

    Returns:
        bytes: Binary data read from file
    """
    with open(filename, 'rb', encoding='utf-8') as f:
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