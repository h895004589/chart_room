from socket import *
import os, sys

ADDR = ('0.0.0.0', 8080)
user_dir = {}


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)
    do_request(s)


def do_request(s):
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode().split(' ')
        if msg[0] == 'L':
            do_login(s, msg[1], addr)
        elif msg[0] == 'C':
            text = " ".join(msg[2:])
            do_chat(s, msg[1], text)
        elif msg[0] == 'Q':
            do_quit(s,msg[2])

def do_quit(s,name):
    msg = "%s退出了聊天室" % name
    for i in user_dir:
        if i != name:
            s.sendto(msg.encode(), user_dir[i])
        else:
            s.sendto(b'EXIT', user_dir[i])
    del user_dir[name]


def do_chat(s, name, text):
    msg = "%s : %s" % (name, text)
    print(msg)
    for i in user_dir:
        if i != name:
            s.sendto(msg.encode(), user_dir[i])


def do_login(s, name, addr):
    if name in user_dir:
        s.sendto("用户名已存在: ", addr)
        return
    s.sendto(b'ok', addr)

    msg = "欢迎%s来到聊天室" % name
    for i in user_dir:
        s.sendto(msg.encode(), user_dir[i])

    user_dir[name] = addr


if __name__ == "__main__":
    main()
