import time
import datetime
import os

def mwts2uts(mwts):
    ta = time.strptime(mwts, "%Y-%m-%dT%H:%M:%SZ")
    return int(time.mktime(ta))
def uts2mwts(uts):
    da = time.localtime(uts)
    return (time.strftime("%Y-%m-%dT%H:%M:%SZ", da))
def msec(mwts,sec):
    t1 = mwts2uts(mwts)
    t2 = t1 - sec
    return uts2mwts(t2)
def psec(mwts,sec):
    t1 = mwts2uts(mwts)
    t2 = t1 + sec
    return uts2mwts(t2)
def alog(msg):
    os.system('echo "' + msg + '" >> log.txt')