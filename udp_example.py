import socket
import time
import numpy as np

from ctypes import *


def convert(s):
    i = int(s, 16)                   # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value         # dereference the pointer, get the float


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4,udp
sock.bind(('192.168.123.163', 65533))  # UDP服务器端口和IP绑定


buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(14):
    buf[i], addr = sock.recvfrom(65530)
print(buf)
for i in range(14):
    print(buf[i])
    temp[i] = convert(buf[i])

print(temp)

# data = [5, 12]
# s = str(data)  # 将数据转化为String
# # 将数据转为bytes发送给matlab的client
# sock.sendto(bytes(s, encoding="utf8"), ('192.168.123.163', 65530))


# count = 0
# while True:
#     time.sleep(1)  # 为了方便调试，这里是每隔一秒发送一次
#     data = [5, 6, 7, count]
#     s = str(data)  # 将数据转化为String
#     sock.sendto(bytes(s, encoding="utf8"), addr)  # 将数据转为bytes发送给matlab的client
#     print('服务器端已发送')
#     print(s)
#     print('正在等待接收客户端信息...')
#     buf, addr = sock.recvfrom(40960)
#     msg = buf.split()
#     print([np.double(i) for i in msg])
#     print(addr)
#     count += 1
sock.close()
