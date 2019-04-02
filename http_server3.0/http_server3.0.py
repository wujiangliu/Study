from socket import *
import sys
from threading import Thread
from config import *

ADDR = (HOST,PORT)

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

httpd = HTTPServer(ADDR)
http.serve_forever() # 启动服务