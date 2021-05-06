from pathlib import Path
import os


class Paths:
    fiocfg_dir = Path('test.txt')
    path = os.getcwd()
    log_dir = Path(f'{path}/log')
