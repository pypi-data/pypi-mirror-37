#coding=utf-8
from __future__ import division
from __future__ import print_function
import time
from collections import OrderedDict
import subprocess

class hoster:
    #host =  user:passwd@127.0.0.1:22
    def __init__(self,host = None):
        self.hostinfo = host
        self.ssh = None
        self.cpu_stat_head = ['user','nice','system','idle','iowait','irq','softirq','stealstolen','guest']
        return
    def __del__(self):
        if (self.hostinfo != None and self.ssh != None):
            self.ssh.close()

    def __connect(self):
        if (self.hostinfo != None and self.ssh == None):
            self.port = 22
            self.user,self.host = tuple(self.hostinfo.split('@'))
            self.user,self.passwd = tuple(self.user.split(':'))
            if (len(self.host.split(':')) == 2):
                t = self.host.split(':')
                self.host = t[0]
                self.port = int(t[1])

            import paramiko
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host,self.port,self.user,self.passwd)
            #self.sftp_client = self.ssh.open_sftp()          

    def __get_out(self,cmd):
        self.__connect()
        ret = []
        if (self.ssh != None):
            stdin, stdout, stderr = self.ssh.exec_command('%s' %cmd)
            while True:
                line = stdout.readline()
                if len(line) <= 0:
                    break
                ret.append(line)
        else:
            p = subprocess.Popen(cmd.split(' '), stdout = subprocess.PIPE)
            data = p.stdout.read()
            ret = data.split("\n")
            if (ret[-1] == ''):
                ret.pop()
        return ret       

    def __cpu_one(self):
        ret = []
        #user nice system idle iowait irq softirq stealstolen guest
        ctx = self.__get_out('cat /proc/stat')
        for line in ctx:
            l = line.split()
            if len(l) < 5:
                continue
            if (l[0].startswith('cpu')):
                t = [l[0]]
                t.extend([int(x) for x in l[1:]])
                ret.append(t)
        return ret
    #cpu使用百分比
    def cpu(self):
        info1 = self.__cpu_one()[0]
        print(info1)
        tot1 = info1[1] + info1[2] + info1[3] + info1[4] + info1[5] + info1[6] + info1[7] + info1[8]
        use1 = info1[1] + info1[2] + info1[3]
        time.sleep(2)
        info2 = self.__cpu_one()[0]
        tot2 = info2[1] + info2[2] + info2[3] + info2[4] + info2[5] + info2[6] + info2[7] + info2[8]
        use2 = info2[1] + info2[2] + info2[3]
        return round((use2-use1) * 1.0/(tot2-tot1) * 100,2)
    #系统负载1,5,15分钟
    def loadavg(self):
        ctx = self.__get_out('cat /proc/loadavg')
        ret = {}
        if (len(ctx) > 0):
            avg = ctx[0].split()
            ret['1'] = float(avg[0])
            ret['5'] = float(avg[1])
            ret['15'] = float(avg[2])
        return ret

    def mem(self):
        meminfo = {}
        #user nice system idle iowait irq softirq stealstolen guest
        ctx = self.__get_out('cat /proc/meminfo')
        for line in ctx:
            if (len(line.split(':')) == 2):
                v = line.split(':')[1].strip().split(' ')
                if (len(v) == 2 and v[1] == 'kB'):
                     meminfo[line.split(':')[0]] = int(v[0]) * 1024
                elif (len(v) == 2 and v[1] == 'mB'):
                    meminfo[line.split(':')[0]] = int(v[0]) * 1024 * 1024
                else:
                    meminfo[line.split(':')[0]] = int(v[0])
        return meminfo
    #网卡数据
    def net(self,interface = 'eth0'):
        ret = []
        ctx = self.__get_out('cat /proc/net/dev')
        for inter in  ctx:
            if interface in inter:
                stat = float(inter.split()[1])
                ret[0:] = [stat]
                stat = float(inter.split()[9])
                ret[1:] = [stat]
        return ret

    #磁盘
    def disk(self):
        ret = {}
        ctx = self.__get_out('df -h')
        cnt = 0
        for line in ctx:
            cnt = cnt + 1
            if (cnt == 1):
                continue
            l = line.split()
            if len(l) == 0 or (len(l) > 1 and l[1] == 'Size'):
                continue
            ret[l[0]] = l
        return ret

    #文件节点
    def dfi(self):
        dfi = {}
        ctx = self.__get_out('df -i')
        cnt = 0
        for line in ctx:
            cnt = cnt + 1
            if (cnt == 1):
                continue
            l = line.split()
            if len(l) == 0 or (len(l) > 1 and l[1] == 'Size'):
                continue
            dfi[l[5]] = l[4]
        #print dfi
        return dfi
    


    #cpu处理器型号
    def cputype(self):
        ctx = self.__get_out('cat /proc/cpuinfo')
        nprocs = 0
        cpuinfo = {}
        procinfo = {}
        for line in ctx:
            if not line.strip():
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs = nprocs + 1
                procinfo = {}
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = '' 
        return cpuinfo
    
    
if __name__ == '__main__':
    h = hoster('appuser:MaxusTest2020_@10.130.10.43:22')
    print(h.cputype())
    print(h.cpu())
    print(h.mem())
    print(h.disk())
    print(h.loadavg())
    print(h.dfi())



