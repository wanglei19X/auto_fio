import subprocess
import time
from Path import Paths
import os
class Logsave:
    def __init__(self, logname:str):
        self.logna = logname
    
    def save(self, bs:str, cmd:str, time:str):
        with open(f'{Paths.log_dir}/{bs}_comand.log', "a+") as f:
            f.write(f'{time}: {cmd}\n')
            f.write("\n")
    def endsave(self):
        os.system(f'mkdir {Paths.log_dir}/{self.logna}')
        os.system(f'mv {Paths.log_dir}/*.log {Paths.log_dir}/{self.logna}')

