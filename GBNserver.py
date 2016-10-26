# coding=utf-8
import socket
from collections import namedtuple
import pickle
import random
import threading
import sys

# class GBNServer:
'''
client --> server
'abcdefghijklmnopqrstuvwxyz'
1.prepare: add head to each character


'''
# data_pkt = namedtuple('data_pkt','seq_num')
data_pkt = namedtuple('data_pkt', 'seq_num data')
# ack_pkt = namedtuple('ack_pkt','seq_num','yes')
'''port = 3377
prob_loss = 0.4
socketserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketserver.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
socketserver.bind(('', port))
'''
expected_seq_num = 0  # the number expected to get
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 2359))  # 发送ack的端口


def send_ack(seq_num):
    ack_message = [seq_num, 'y']
    clihost = ''
    cliport = 2333
    s.sendto(pickle.dumps(ack_message), (clihost, cliport))


def main():
    global expected_seq_num
    lost_seq_num = []
    port = 3377
    prob_loss = 0.3
    socketserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketserver.bind(('', port))
    while 1:
        # data_pkt = namedtuple('data_pkt', 'seq_num data')
        # ack_pkt = namedtuple('ack_pkt','seq_num','yes')
        data, address = socketserver.recvfrom(100000)
        data = pickle.loads(data)
        get_seq_num = data[0]
        rand = random.random()
        if rand <= prob_loss:
            print 'Packet loss, sequence number' + '\t' + str(get_seq_num)
            pass
        elif get_seq_num == expected_seq_num:
            print '已按序正确收到' + str(expected_seq_num) + '数据包'
            print data[1]
            send_ack(get_seq_num)
            expected_seq_num += 1
            with open('result.txt', 'w') as f:
                f.write(data[1])
                f.write('\n')
        elif get_seq_num > expected_seq_num:
            if expected_seq_num == 0:
                pass
            else:
                print '已按序正确收到' + str(expected_seq_num - 1) + '数据包' + '\n'
                send_ack(expected_seq_num - 1, socketserver)


if __name__ == '__main__':
    main()
