"""
chat room 客户端
发送请求，获取结果
"""

from socket import *
from multiprocessing import Process
import sys

# 服务器地址
ADDR = ('127.0.0.1',8000)

# 接收消息
def recv_msg(sock):
    while True:
        data,addr = sock.recvfrom(4096)
        print(data.decode())

# 发送消息
def send_msg(sock,name):
    while True:
        content = input("发言:")
        if content == "quit":
            msg = "Q " + name
            sock.sendto(msg.encode(),ADDR)
            sys.exit("您已退出聊天室") # 父进程退出
        msg = "C %s %s"%(name,content)
        sock.sendto(msg.encode(),ADDR) # 发送消息给服务器


# 进入聊天室
def login(sock):
    while True:
        name = input("Name:")
        msg = "L " + name # 根据协议，整理发送的消息格式 L name
        sock.sendto(msg.encode(),ADDR)
        result,add = sock.recvfrom(128)
        if result.decode() == "OK":
            print("进入聊天室")
            return name
        else:
            print("该用户已存在")

def main():
    sock = socket(AF_INET,SOCK_DGRAM)
    name = login(sock) # name 进入聊天室

    # 创建子进程
    p = Process(target=recv_msg,args=(sock,))
    p.daemon = True # 父进程退出时子进程也退出
    p.start()
    send_msg(sock,name) # 发送消息



if __name__ == '__main__':
    main()