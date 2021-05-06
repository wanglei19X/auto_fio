import subprocess
from Path import Paths
class Chenklog:
    def __init__(self, logname :str):
        self.name = logname
    
    def __str__(self):
        return f'logname: {self.name}'

    @property
    def logcheck(self):
        flag = "true"
        try:
            with open(f'{Paths.log_dir}/{self.name}', "r") as f:
                pass
        except FileNotFoundError:
            flag = "flase"  
            return flag
        filesize = subprocess.getstatusoutput(f'ls -l {Paths.log_dir} |grep -i {self.name}')[1]
        filesize = list(filesize.split(" ")[4])        
        if len(filesize) < 4:
            flag = "flase"
            return flag
        fileline = subprocess.getstatusoutput(f'cat {Paths.log_dir}/{self.name} |wc -l')[1]
        if int(fileline) < 25:
            flag = "flase"
            return flag
        return flag

