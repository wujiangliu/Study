#! /usr/bin/env python3
#coding=utf-8
'''
AID httpserver v3.0
WebFrame 部分
用于模拟网站的后端工作
'''

from socket import *
import json
from select import select
from settings import *
from urls import *
from views import *

frame_address = (frame_ip,frame_port)

# 创建应用类用于处理请求
class Application(object):
    def __init__(self):
        self.ip = frame_address[0]
        self.port = frame_address[1]
        self.create_socket()
    
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
        self.sockfd.bind(frame_address)

    def start(self):
        self.sockfd.listen(5)
        print('Listen the port %d ...'%self.port)
        rlist = [self.sockfd]
        wlist = []
        xlist = []
        while True:
            rs,ws,xs = select(rlist,wlist,xlist)
            for r in rs:
                if r is self.sockfd:
                    connfd,addr = r.accept()
                    rlist.append(connfd)
                else:
                    # 接收json格式请求
                    request = r.recv(1024).decode()
                    if not request:
                        rlist.remove(r)
                        continue
                    self.handle(r,request)
    def handle(self,connfd,request):
        request = json.loads(request)
        print(request)
        method = request['method']
        path_info = request['path_info']

        if method == 'GET':
            if path_info == '/' or path_info[-5:] == '.html':
                data = self.get_html(path_info)
            else:
                data = self.get_data(path_info)
        elif method == 'POST':
            pass
        connfd.send(json.dumps(data).encode())

    def get_html(self,path_info):
        data = {}
        if path_info == '/':
            get_file = STATIC_DIR + '/index.html'
        else:
            get_file = STATIC_DIR + path_info
        try:
            f = open(get_file)
        except IOError:
            data['status'] = '404'
            data['content'] = 'Sorry not found the page'
        else:
            data['status'] = '200'
            data['content'] = f.read()
        return data
    
    def get_data(self,path_info):
        data = {}
        for url,fun in urls:
            if path_info == url:
                content = fun()
                data['status'] = '200'
                data['content'] = content
                print(data)
                return data
        data['status'] = '404'
        data['content'] = 'Sorry not found the content'
        return data


app = Application()
app.start() # 启动后端框架服务