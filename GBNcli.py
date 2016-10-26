# coding=utf-8
import socket
from collections import namedtuple
import pickle
import time
import signal
import threading

srcfile = 'test.txt'
data_pkt = namedtuple('data_pkt', 'seq_num data')
MAX_WINDOW_wide = 5
all_pkt = []  # 所有的数据包状态　int数组，环形?已发送并确认设置为0,已发送未确认设置为１,未发送设置为2
window_low = 0
window_high = int(MAX_WINDOW_wide) #窗口不包括window_high  --- [window_low ~ window_high - 1]窗口位置
time_out = 5# 超时时间
allitem = []#　所有数据包
ackeditem = 0 #已确认的数据包
cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sr = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sr.bind(('',2360))

def preparetosend(src):
    global allitem,all_pkt
    i = 0
    with open(src) as f:
        for str in f:
            item = data_pkt(seq_num=i, data=str)
            m = pickle.dumps(item)
            allitem.append(m)
            all_pkt.append(2)  # 初始化都为未发送状态
            i += 1
    return

# 获取已经pickle过的持久化对象列表作为发送的数据包，并根据行数初始化all_pkt数组
def send_group():
    global serverport,serverhost
    global window_low,window_high
    #signal.alarm(0)
    #signal.setitimer(signal.ITIMER_REAL, time_out)
    for i in range(window_low, window_low + MAX_WINDOW_wide):  # 如果窗口内有新加入的item则发送该item
        if i >= len(all_pkt):
            break
        if all_pkt[i] == 2:
            send_item(allitem[i])
            all_pkt[i] = 1

def send_item(item):
    global serverport, serverhost
    cli.sendto(item, ('', 3377))

#超时处理函数，此时将获得一个SIG_ALm信号
def time_do(signum,frame):#重发
    global window_low, window_high
    signal.alarm(0)
    signal.setitimer(signal.ITIMER_REAL, time_out)
    for i in range(window_low,window_high):
        cli.sendto(allitem[i],('',3377))


def receive_ack():
    global window_low,ackeditem
    while 1:
        s = sr.recv(1024)
        s = pickle.loads(s)
        print s
        if s[0] == window_low:
            print '收到来自第' + str(s[0]) + '个数据包的ack'
            all_pkt[window_low] = 0  # 设置为发送并接收状态
            window_low += 1
            ackeditem += 1
            signal.alarm(0)
        else:
            pass

def main():
    global ackeditem, serverhost, serverport ,allitem,all_pkt,window_low
    preparetosend(srcfile)
    signal.signal(signal.SIGALRM,time_do)
    cli.bind(('',2233))
    cli.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cli.connect(('',3377))
    t = threading.Thread(target=receive_ack)
    t.setDaemon(True)
    t.start()
    while ackeditem != len(all_pkt):
        #i = window_low
        send_group()

if __name__ == '__main__':
    main()
