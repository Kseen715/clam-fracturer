from common import *
import argparse


def drop_by_ip(ip):
    data = read_csv(DB_FILE)
    data = [x for x in data if x[0] != ip]
    write_csv(data, DB_FILE)
    log_happy(f"Deleted {ip}")


def drop_by_hostname(hostname):
    data = read_csv(DB_FILE)
    data = [x for x in data if x[1] != hostname]
    write_csv(data, DB_FILE)
    log_happy(f"Deleted {hostname}")


def insert_entry(ip, hostname, comment):
    log_info(f"Inserting \"{ip}\",\"{hostname}\",\"{comment}\"")
    if not ip or not hostname:
        log_warning("IP and hostname are required")
        return
    if not comment:
        comment = ""
    data = read_csv(DB_FILE)
    new_data = pd.DataFrame([[ip, hostname, comment]], columns=["ipv4", "hostname", "comment"])
    data = pd.concat([data, new_data], ignore_index=True)
    write_csv(data, DB_FILE)
    log_happy(f"Inserted \"{ip}\",\"{hostname}\",\"{comment}\"")


def insert_ip_list(filename, hostname, comment):
    if not hostname:
        log_warning("Hostname is required")
        return
    if not comment:
        comment = ""
    if not filename:
        log_warning("Filename is required")
        return
    data = read_csv(DB_FILE)
    new_data = pd.read_csv(filename, header=None, names=["ipv4"])
    new_data["hostname"] = hostname
    new_data["comment"] = comment
    log_info(f"Inserting {len(new_data)} IPs from {filename} with hostname \"{hostname}\" and comment \"{comment}\"")
    data = pd.concat([data, new_data], ignore_index=True)
    write_csv(data, DB_FILE)
    log_happy(f"Inserted IPs from {filename}")


CONSOLE_DROP_PARAMETERS = {
    'ipv4': 'IP address to drop',
    'hostname': 'Hostname to drop (all IPs)',
    'comment': 'Comment to drop (all IPs)',
    'comment-part': 'Find all comments containing this string',
}


def drop(parameters, arguments):
    # drop all entries with given parameters, use AND logic
    if 'comment' in parameters and 'comment-part' in parameters:
        log_warning("Cannot use both --comment and --comment-part")
        return
    data_pick = read_csv(DB_FILE)
    if 'ipv4' in parameters:
        data_pick = data_pick[data_pick['ipv4'] == arguments['ipv4']]
    if 'hostname' in parameters:
        data_pick = data_pick[data_pick['hostname'] == arguments['hostname']]
    if 'comment' in parameters:
        data_pick = data_pick[data_pick['comment'] == arguments['comment']]
    if 'comment-part' in parameters:
        data_pick = data_pick[data_pick['comment'].fillna('').str.contains(arguments['comment-part'])]
    data_drop = read_csv(DB_FILE)
    log_info(f"Dropping {len(data_pick)} entries")
    ans = None
    if len(data_pick) != 0:
        ans = input(f"{colorama.Fore.RED}ARE YOU SURE "\
            + f"you want to DROP {len(data_pick)} entries? [y/N]{colorama.Style.RESET_ALL}")
    if ans.lower() != 'y':
        log_info("Aborted")
        return
    data_drop = data_drop[~data_drop.isin(data_pick)].dropna()
    write_csv(data_drop, DB_FILE)
    log_happy(f"Dropped {len(data_pick)} entries")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f'{colorama.Fore.LIGHTCYAN_EX}CLAM-FRACTURER'+\
                                     f'{colorama.Fore.CYAN} database console{colorama.Style.RESET_ALL}')
    parser.add_argument('--insert-entry', nargs=3, help='Insert entry into database', metavar=('<ipv4>', '<hostname>', '<comment>'))
    parser.add_argument('--insert-ip-list', nargs=3, help='Insert list of IPs from file into database', metavar=('<filename>', '<hostname>', '<comment>'))
    parser.add_argument('--drop', nargs='*', help='Drop entry from database ' \
                        + f'{colorama.Fore.LIGHTBLACK_EX} ' \
                        + str(CONSOLE_DROP_PARAMETERS) \
                        + f'{colorama.Style.RESET_ALL}', \
                        metavar=('[<parameter> <value>]'))

    args = parser.parse_args()

    if args.drop:
        drop_parameters = {}
        drop_arguments = {}
        if len(args.drop) == 0:
            log_warning("No parameters to drop")
            exit(1)
        if len(args.drop) % 2 != 0:
            log_warning("Each parameter must be followed by its value")
            exit(1)
        for i in range(0, len(args.drop), 2):
            param = args.drop[i]
            value = args.drop[i + 1]
            if param in CONSOLE_DROP_PARAMETERS:
                drop_parameters[param] = CONSOLE_DROP_PARAMETERS[param]
                drop_arguments[param] = value
        log_info(f"Dropping by {drop_arguments}")
        drop(drop_parameters, drop_arguments)
    elif args.insert_entry:
        insert_entry(*args.insert_entry)
    elif args.insert_ip_list:
        insert_ip_list(*args.insert_ip_list)
    else:
        parser.print_help()
        exit(1)