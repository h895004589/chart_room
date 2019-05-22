from socket import *
import os, sys

ADDR = ('127.0.0.1', 8080)


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入姓名: ")
        msg = "L " + name
        s.sendto(msg.encode(), ADDR)
        data, addr = s.recvfrom(1024)
        if data.decode() == 'ok':
            print("欢迎来到聊天室")
            break

    pid = os.fork()

    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(s,name)
    else:
        recive_msg(s)


def send_msg(s,name):
    while True:
        text = input("要发送的消息:")
        if text == 'quit':
            msg = "Q " + name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")

        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(), ADDR)

def recive_msg(s):
    while True:
        data,addr = s.recvfrom(1024)
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode())

if __name__ == "__main__":
    main()
