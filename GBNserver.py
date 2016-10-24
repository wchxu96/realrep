import socket
from collections import namedtuple
import pickle
import random
import sys

# class GBNServer:
'''
client --> server
'abcdefghijklmnopqrstuvwxyz'
1.prepare: add head to each character


'''
# data_pkt = namedtuple('data_pkt','seq_num')
data_pkt = namedtuple('data_pkt', 'seq_num', 'data')
# ack_pkt = namedtuple('ack_pkt','seq_num','yes')
ack_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostbyname()
port = 2333 # client
expected_seq_num = 0  # the number expected to get


def send_ack(seq_num):
    ack_message = [seq_num, 'y']
    ack_socket.sendto(pickle.dumps(ack_message), (host, port))


def main():
    global expected_seq_num
    port = 3377
    prob_loss = 0.4
    socketserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketserver.bind(socket.gethostbyname(), port)
    lost_seq_num = []
    while 1:
        data, address = socketserver.recvfrom(100000)
        data = pickle.loads(data)
        get_seq_num = data[0]
        rand = random.random()
        if rand <= prob_loss:
            print 'Packet loss, sequence number' + str(get_seq_num)
            pass
        elif get_seq_num == expected_seq_num + 1:
            send_ack(get_seq_num)
            expected_seq_num += 1
            with open('result.txt', 'ab') as f:
                f.write(data[1])
                f.write('\n')
        elif get_seq_num > expected_seq_num + 1:
            send_ack(expected_seq_num)

if __name__ == '__main__':
    main()
