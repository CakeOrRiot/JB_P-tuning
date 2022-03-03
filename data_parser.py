import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd


def write_sonnet(path, num, lines):
    if len(lines) == 0:
        return None
    sonnet_file_name = path / 'processed' / f'{num}'
    with open(sonnet_file_name, 'wt') as f:
        f.writelines(lines)


def process_raw(path):
    raw_data_path = path / 'raw.txt'
    sonnet_num = 0
    with open(raw_data_path, 'rt') as f_raw:
        current_sonnet = []
        for i, line in enumerate(f_raw):

            if line == '\n':
                sonnet_num = int(f_raw.readline())
                f_raw.readline()
                write_sonnet(path, sonnet_num - 1, current_sonnet)
                current_sonnet = []
            else:
                current_sonnet.append(line)

    write_sonnet(path, sonnet_num - 1, current_sonnet)


def train_test_split(path):
    processed_data_path = path / 'processed'
    total_samples = len(
        [name for name in os.listdir(processed_data_path) if os.path.isfile(processed_data_path / name)])
    train_samples = int(0.8 * total_samples)
    test_samples = int((total_samples - train_samples) * 0.5)
    validate_samples = total_samples - train_samples - test_samples
    idx = np.arange(1, total_samples + 1)
    np.random.shuffle(idx)
    train = idx[:train_samples]
    test = idx[train_samples:test_samples + train_samples]
    validate = idx[train_samples + test_samples:]

    shutil.rmtree(path / 'train')
    shutil.rmtree(path / 'test')
    shutil.rmtree(path / 'validate')
    os.mkdir(path / 'train')
    os.mkdir(path / 'test')
    os.mkdir(path / 'validate')
    for i in range(1, total_samples + 1):
        file_name = f'{i}'
        if i in train:
            shutil.copyfile(processed_data_path / file_name, processed_data_path / '..' / 'train' / file_name)
        elif i in test:
            shutil.copyfile(processed_data_path / file_name, processed_data_path / '..' / 'test' / file_name)
        else:
            shutil.copyfile(processed_data_path / file_name, processed_data_path / '..' / 'validate' / file_name)

    return train, test, validate


def truncate(file, to_trunc=20):
    with open(file) as f:
        content = f.readlines()
        tokens = ''.join(content).split()
        return ' '.join(tokens[:-to_trunc]), ' '.join(tokens[-to_trunc:])


def create_csv(path, name):
    items = []
    for file_name in os.listdir(path):
        start, end = truncate(path / file_name)
        items.append([start, end])
    df = pd.DataFrame(items, columns=['start', 'end'])
    df.to_csv(path / '..' / f'{name}.csv')


if __name__ == '__main__':
    np.random.seed(102)
    path = Path('data/')
    process_raw(path)
    train_test_split(path)
    create_csv(path / 'train', 'train')
    create_csv(path / 'test', 'test')
    create_csv(path / 'validate', 'validate')
