from socket import *
import sys
from threading import Thread
from config import *
import json
from time import sleep

ADDR = (HOST,PORT)

# 将请求发送给frame,获取数据
def connect_frame(**env):
    s = socket()
    while True:
        try:
            s.connect(frame_address)
        except Exception as e:
            print(e)
            sleep(3)
        else:
            break
    # 将请求发送给webframe
    s.send(json.dumps(env).encode())
    data = s.recv(4096*20).decode()
    return data
    

# 封装HTTPServer类，实现基本功能
class HTTPServer(object):
    def __init__(self,address):
        self.address = address
        self.create_socket()
        self.bind()
    
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
    
    def bind(self):
        self.ip = self.address[0]
        self.port = self.address[1]
        self.sockfd.bind(self.address)

    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d ...'%self.port)
        while True:
            try:
                connfd,addr = self.sockfd.accept()
                print('connect from',addr)
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('退出 http server 服务')
            except Exception as e:
                print(e)
                continue
            client = Thread(target = self.handle,args = (connfd,))
            client.setDaemon(True)
            client.start()
    def handle(self,connfd):
        request = connfd.recv(4096)
        if not request:
            connfd.close()
            return
        request_lines = request.splitlines()
        # 得到请求行
        request_line = request_lines[0].decode()
        print('请求:',request_line)

        # 组织请求内容
        tmp = request_line.split(' ')
        method = tmp[0]
        path_info = tmp[1]
        # 连接frame 获取数据返回
        data = connect_frame(method = method,path_info = path_info)
        self.response(connfd,data)
    
    # 将数据组织响应格式发送给浏览器
    def response(self,connfd,data):
        # data ==>'{'status':'200','content':'xxxx'}'
        data = json.loads(data)
        status = data['status'] #  响应码
        content = data['content']  #　数据内容
        if status == '200':
            response_headlers = 'HTTP/1.1 200 OK\r\n'
        elif status == '404':
            response_headlers = 'HTTP/1.1 404 Not Found\r\n'
        response_headlers += '\r\n'
        response_body = content
        response = response_headlers + response_body
        connfd.send(response.encode())
        connfd.close() 

httpd = HTTPServer(ADDR)
httpd.serve_forever() # 启动服务