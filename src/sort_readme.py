from common import *
# catch <div id="auto-sort-start"/> and <div id="auto-sort-end"/> in README.md
# sort the lines between them alphabetically


def sort_readme():
    log_info('sort_readme: Starting')
    with open('README.md', 'r') as f:
        readme = f.readlines()
    start = readme.index('<div id="auto-sort-start"/>\n') + 1
    end = readme.index('<div id="auto-sort-end"/>\n')
    sorted_readme = readme[:start] + sorted(readme[start:end]) + readme[end:]
    with open('README.md', 'w') as f:
        f.writelines(sorted_readme)
    log_happy('README.md sorted')
    log_info('sort_readme: Finished')


if __name__ == '__main__':
    sort_readme()