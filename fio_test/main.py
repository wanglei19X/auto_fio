from FIO import Cfg
from env import Env
import json
import sys
import os
import time
import subprocess
from log_check import Chenklog
from messages import Messages
from logsave import Logsave
def main():
    mess = Messages()
    env = Env("/mnt/pmem0")
    logtime = subprocess.getstatusoutput('date +"%Y-%m-%d-%h-%s"')[1]
    log = Logsave(logtime)

    env.check_pmempath()
    flag, error = env.check_env()
    if flag == "false":
        print(error)
        sys.exit()
    with open("test_plan.json", "r") as config:
        basecfg = json.load(config)
        base_cfg = basecfg["FIO_BASE"]
        bs = basecfg["block_size"]
        job = basecfg["job"]
        qd = basecfg["QD"]
        iotype_list = basecfg["io_type"]
    cfg_list = []
    for iotype in iotype_list:
        for blocksize in bs:
            for joblist in job:
                for qdlist in qd:
                    cfg = Cfg(base_cfg, blocksize, joblist, qdlist, iotype)
                    cfg_list.append(cfg)
    for case in cfg_list:
        i = 0
        while i < 2:
            cmd = case.run()
            print(cmd)
            os.system(cmd)
            logch = Chenklog(cmd.split("/")[-1])
            status = logch.logcheck
            if status == "true":
                break
            else:
                i = i+1
        localtime = time.asctime(time.localtime(time.time()))
        log.save(case.block_size, cmd, localtime)
        if i == 0:
            pass
        elif i == 1:
            mess.savemessages(localtime, "first error and sencond try", "warning", case)
        elif i == 2:
            mess.savemessages(localtime, "this case run error pls chenk", "error", case)
    log.endsave()
if __name__ == '__main__':
    main()
