from common import *
import re
import os
# catch <div id="auto-sort-start"/> and <div id="auto-sort-end"/> in README.md
# sort the lines between them alphabetically


def sort_readme():
    log_info('sort_readme: Starting')
    if os.path.exists('./hashes/README.md.hash'):
        if not check_hash_binary(hash_file('README.md'), './hashes/README.md.hash'):
            log_warning('README.md has been modified')
        else:
            log_info('README.md has not been modified')
            return
    else:
        log_warning('No hash file found for README.md')
    
    with open('README.md', 'r') as f:
        readme = f.readlines()
    
    sorted_readme = []
    i = 0
    while i < len(readme):
        if readme[i] == '<div id="auto-sort-start"/>\n':
            sorted_readme.append(readme[i])
            i += 1
            start = i
            while i < len(readme) and readme[i] != '<div id="auto-sort-end"/>\n':
                i += 1
            end = i
            # Sort lines ignoring symbols
            lines_to_sort = readme[start:end]
            sorted_lines = sorted(lines_to_sort, key=lambda line: re.sub(r'[^a-zA-Z0-9\s]', '', line))
            sorted_readme.extend(sorted_lines)
        if i < len(readme):
            sorted_readme.append(readme[i])
        i += 1
    
    with open('README.md', 'w') as f:
        f.writelines(sorted_readme)
    
    log_happy('README.md sorted')
    save_hash_binary(hash_file('README.md'), './hashes/README.md.hash')
    log_info('sort_readme: Finished')


if __name__ == '__main__':
    sort_readme()