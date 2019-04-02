'''
http server v1.0
接收浏览器请求，返回网页
'''

from socket import *

# 处理客户端请求
def handleClient(connfd):
    print('Request from',connfd.getpeername())  # 打印客户端地址
    request = connfd.recv(4096)  # 接收到的http请求
    # print(request)
    # 没有内容，函数退出
    if not request:
        return
    # 提取请求行
    request_lines = request.splitlines()
    print(request_lines[0])
    try:
        f = open('../PythonNet/day03/abc.html')
    except OSError:
        response = 'HTTP/1.1 404 Not Found\r\n'
        response += '\r\n'
        response += '=== Sorry not found ==='
    else:
        response = 'HTTP/1.1 404 Not Found\r\n'
        response += '\r\n'
        response += f.read()
    finally:
        # 将内容(response)发送给浏览器
        connfd.send(response.encode())


# 创建套接字
def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(('0.0.0.0',7777))
    sockfd.listen(3)
    print('listen the port 7777......')
    while True:
        connfd,addr = sockfd.accept()
        handleClient(connfd) # 处理客户端请求
        connfd.close()

main()    