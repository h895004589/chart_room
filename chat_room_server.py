"""
    Chat room server
    env: python 3.6
    socket fork 练习
"""
from socket import *
import os, sys

ADDR = ('0.0.0.0', 8080)
# 存储用户信息
user = {}


# 创建网络链接
def main():
    # 套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input("管理员消息:")
            msg = "C 管理员消息" + msg
            s.sendto(msg.encode(),ADDR)
    else:
        # 请求处理
        do_request(s)

def do_request(s):
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode().split(' ')
        # 区分请求类型
        if msg[0] == 'L':
            do_login(s, msg[1], addr)
        elif msg[0] == 'C':
            text = " ".join(msg[2:])
            do_chat(s, msg[1], text)
        elif msg[0] == 'Q':
            if msg[1] not in user:
                s.sendto(b'EXIT',ADDR)
                continue
            do_quit(s, msg[1])
# 退出
def do_quit(s, name):
    msg = "%s退出了聊天室" % name
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])
        else:
            s.sendto(b'EXIT', user[i])
    del user[name]


def do_chat(s, name, text):
    msg = "%s : %s" % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])


def do_login(s, name, addr):
    if name in user or "管理员" in name:
        s.sendto("该用户已存在".encode(), addr)
        return
    s.sendto(b'ok', addr)

    # 通知其他人
    msg = "欢迎%s进入聊天室" % name
    for i in user:
        s.sendto(msg.encode(), user[i])

    # 将用户加入
    user[name] = addr


if __name__ == "__main__":
    main()
