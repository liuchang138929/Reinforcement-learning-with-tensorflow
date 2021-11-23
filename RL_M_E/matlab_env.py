import numpy as np
import time
import socket

from ctypes import *

from numpy.core.fromnumeric import shape


class m_e(object):
    def __init__(self):
        super(m_e, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.n_features = 12
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)  # ipv4,udp
        self.sock.bind(('192.168.123.163', 65533))  # UDP服务器端口和IP绑定

    def reset(self):
        data = [0, 1]
        s = str(data)  # 将数据转化为String
        # 将数据转为bytes发送给matlab的client
        self.sock.sendto(bytes(s, encoding="utf8"), ('192.168.123.163', 65530))
        buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(14):
            buf[i], addr = self.sock.recvfrom(65530)

        for i in range(14):
            temp[i] = self.convert(buf[i])
        s_ = temp[0:12]
        return np.array(s_)

    def step(self, action):
        data = [action, 0]
        s = str(data)  # 将数据转化为String
        # 将数据转为bytes发送给matlab的client
        self.sock.sendto(bytes(s, encoding="utf8"), ('192.168.123.163', 65530))
        buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(14):
            buf[i], addr = self.sock.recvfrom(65530)

        for i in range(14):
            temp[i] = self.convert(buf[i])
        s_ = temp[0:12]
        reward = temp[12]
        done = temp[13]
        return np.array(s_), reward, done

    def convert(self, s):
        i = int(s, 16)                   # convert from hex to a Python int
        cp = pointer(c_int(i))           # make this into a c integer
        # cast the int pointer to a float pointer
        fp = cast(cp, POINTER(c_float))
        return fp.contents.value         # dereference the pointer, get the float
