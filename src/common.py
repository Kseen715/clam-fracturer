import pandas as pd
import json
import colorama
import datetime


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