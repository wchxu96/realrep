import socket
from collections import namedtuple
import pickle


data_pkt = namedtuple('data_pkt','seq_num','data')
MAX_WINDOW_wide = 5


def preparetosend(src):
    allitem = []
    i = 1
    with open(src) as f:
        for str in f:
            item = data_pkt(seq_num=i,data=str)
            m = pickle.dumps(item)
            allitem.append(m)
            i += 1
    return allitem

if __name__ == '__main__':
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.gethostbyname()
    port = 2333
    cli.bind((host, port))