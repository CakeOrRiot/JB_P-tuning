import os
from pathlib import Path


def write_sonnet(num, lines):
    if len(lines)==0:
        return None
    sonnet_file_name = data_path / 'processed' / f'{num}'
    with open(sonnet_file_name, 'wt') as f:
        f.writelines(lines)


data_path = Path('data/')
raw_data_path = data_path / 'raw.txt'
sonnet_num = 0
with open(raw_data_path, 'rt') as f_raw:
    current_sonnet = []
    for i, line in enumerate(f_raw):

        if line == '\n':
            sonnet_num = int(f_raw.readline())
            f_raw.readline()
            write_sonnet(sonnet_num - 1, current_sonnet)
            current_sonnet = []
        else:
            current_sonnet.append(line)

write_sonnet(sonnet_num - 1, current_sonnet)
