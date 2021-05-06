import json
from Path import Paths
import subprocess
import os
import env
class Cfg:
    def __init__(self, base_cfg: dict, block_size: str, job: str, QD: str, io_type: str):
        self.base_cfg = base_cfg
        self.block_size = block_size
        self.job = job
        self.QD = QD
        self.io_type = io_type
        self.cmd = ""
        
    def __str__(self):
        return f'block_size: {self.block_size}, job: {self.job}, QD: {self.QD}, iotype: {self.io_type}'
    
    def _cfg_file_create(self):
        try:
            with self._cfg_file_path.open(mode='w') as cfgfile:
                for k in self.base_cfg.keys():
                    cfgfile.write(self.base_cfg[k])
                    cfgfile.write("\n")  
        except FileExistsError:
            pass
        finally:
            with self._cfg_file_path.open(mode='a') as f:
                f.write("[libpmem]\n")
                f.write(f'bs={self.block_size}\n' f'numjobs={self.job}\n' f'iodepth={self.QD}\n' f'rw={self.io_type}\n')
    
    def ioType(self, name: str):
        if name.startswith('rand'):
            return 'rand'
        else:
            return 'seq'
        raise ValueError
    def run(self):
        #print(self)
        self._cfg_file_create()
        #case._print_basecfg()
        return self.pre_cmd()

    @property
    def _cfg_file_path(self):
        return Paths.fiocfg_dir

    @property
    def _test_log_path(self):
        return Paths.log_dir
    
    def _print_basecfg(self):
        #print("################BASE CFG"################)
        for v in self.base_cfg.values():
            print(f'{v}')
    def pre_cmd(self):
        core = subprocess.getstatusoutput("lscpu |grep -i 'Core(s) per socket:' |awk '{print $NF}'")[1]
        socket = subprocess.getstatusoutput("lscpu |grep -i 'Socket(s):' |awk '{print $NF}'")[1]
        if socket == "2":
            thread1_start = subprocess.getstatusoutput("lscpu |grep -i 'NUMA node0 CPU(s):'|awk '{print $NF}'|cut -d ',' -f1|cut -d '-' -f1")[1]
            thread1_end = subprocess.getstatusoutput("lscpu |grep -i 'NUMA node0 CPU(s):'|awk '{print $NF}'|cut -d ',' -f1|cut -d '-' -f2")[1]
            thread2_start = subprocess.getstatusoutput("lscpu |grep -i 'NUMA node0 CPU(s):'|awk '{print $NF}'|cut -d ',' -f2|cut -d '-' -f1")[1]
            thread2_end = subprocess.getstatusoutput("lscpu |grep -i 'NUMA node0 CPU(s):'|awk '{print $NF}'|cut -d ',' -f2|cut -d '-' -f2")[1]
        else:
            thread1_start = subprocess.getstatusoutput("lscpu |grep -i 'NUMA node0 CPU(s):'|awk '{print $NF}'|cut -d ',' -f1|cut -d '-' -f1")[1]
            thread1_end = subprocess.getstatusoutput("lscpu |grep -i 'NUMA node0 CPU(s):'|awk '{print $NF}'|cut -d ',' -f1|cut -d '-' -f2")[1]

        if int(self.job) < int(core):
            path = f'{self.block_size}_{self.ioType(self.io_type)}_{self.io_type}_{self.job}job_QD{self.QD}.log'
            cmd = f'taskset -c 1-{self.job} fio test.txt >{self._test_log_path.joinpath(path)}'
            #print(cmd)
        else:
            if int(socket) == 1:
                path = f'{self.block_size}_{self.ioType(self.io_type)}_{self.io_type}_{self.job}job_QD{self.QD}.log'
                cmd = f'taskset -c 1-{self.job} fio test.txt >{self._test_log_path.joinpath(path)}'
                #print(cmd)     
            else:
                more = int(self.job）- int(thread1_end)
                end = int(thread2_start) + int(more) -1
                path = f'{self.block_size}_{self.ioType(self.io_type)}_{self.io_type}_{self.job}job_QD{self.QD}.log'
                cmd = f'taskset -c 1-{thread1_end},{thread2_start}-{str(end)} fio test.txt >{self._test_log_path.joinpath(path)}' 
                #print(cmd)                 
        return cmd
