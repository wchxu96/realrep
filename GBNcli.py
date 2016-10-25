# coding=utf-8
import socket
from collections import namedtuple
import pickle
import time
import signal

srcfile = 'test.txt'
data_pkt = namedtuple('data_pkt', 'seq_num', 'data')
MAX_WINDOW_wide = 5
cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostbyname()
port = 2333# client port
cli.bind((host, port))
serverhost = socket.gethostbyname()
serverport = 3377
all_pkt = []  # 所有的数据包状态　bool数组，环形?已发送设置为true,未发送设置为false
window_low = 0
window_high = int(MAX_WINDOW_wide) #窗口不包括window_high  --- [window_low ~ window_high - 1]窗口位置
time_out = 2#超时时间
allitem = []#　所有数据包
curitem = 0#当前要发送的数据包
ackeditem = 0 #已确认的数据包


def preparetosend(src):
    global allitem
    i = 0
    with open(src) as f:
        for str in f:
            item = data_pkt(seq_num=i, data=str)
            m = pickle.dumps(item)
            allitem.append(m)
            all_pkt.append(False)  # 初始化为全false
            i += 1
    return

# 获取已经pickle过的持久化对象列表作为发送的数据包，并根据行数初始化all_pkt数组
def send_item():
    global serverport,serverhost
    global window_low,window_high
    signal.alarm(0)
    signal.setitimer(signal.ITIMER_REAL, time_out)
    for i in range(window_low,window_high):
        cli.sendto(allitem[i],(serverhost,serverport))

#超时处理函数，此时将获得一个SIG_ALm信号
def time():#重发
    '''
    global window_low, window_high
    for i in range(window_low,window_high):
        signal.alarm(0)
        signal.setitimer(signal.ITIMER_REAL,time_out)
        cli.sendto(allitem[i],(host,port))
    '''




def main():
    preparetosend(srcfile)
    signal.signal(signal.SIGALRM,send_item)
    serverhost = socket.gethostbyname()
    serverport = 3377
    cli.connect((serverhost,serverport))
    while ackeditem != len(allitem) - 1:
        i = window_low
        send_item()






def set_timer():



if __name__ == '__main__':
    pass
