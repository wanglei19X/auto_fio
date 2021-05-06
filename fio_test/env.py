import subprocess
import sys
import os
class Env:
    def __init__(self, pmem_path: str):
        self.pmempath = pmem_path
    
    def __str__(self):
        return f'pmempath: {self.pmempath}'

    def check_env(self):
        flag = "true"
        err = ""
        engine = subprocess.getstatusoutput("ldconfig -p | grep libpmem")[1]
        if engine == "":
            flag = "flase"
            err = "Not Find libpmem engine, PLS checkout! "
        numa = subprocess.getstatusoutput("rpm -qa |grep -i numactl")[1]
        if numa == "":
            flag = "flase"
            err += "Not Find numactl, PLS checkout! "
        PMDK = subprocess.getstatusoutput("ls /usr/include/ |grep -i pmem")[1]
        if PMDK == "":
            flag = "flase"
            err += "Not Find libpmem lib, PLS checkout! "
        return flag, err
        
    def check_pmempath(self):
        devnum = subprocess.getstatusoutput(f'mountpoint -qd {self.pmempath}')[1]
        if devnum == "":
            print(f'{self.pmempath} not find and try to mount')
            pmem = self.pmempath.split("/")[-1]
            devfile = subprocess.getstatusoutput(f'ls /dev/ |grep -i {pmem}')[1]
            if devfile == "":
                sys.exit("Not Find dev file!")
            else:
                mountstatu = subprocess.getstatusoutput(f'mount -o dax /dev/{pmem} {self.pmempath}')[0]
                if mountstatu != 0:
                    sys.exit("try mount /dev/pmem* fail!")

                      
