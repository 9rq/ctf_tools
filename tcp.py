# -*- coding: utf-8 -*-
'''
TCP tools

Todo:
    implement Server
'''

import socket
import time
import threading


def exception(func):
    '''
    error handler
    '''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            args[0].sock.close()
            exit(0)
    return wrapper


class Client():
    '''
    TCP client

    Attributes:
        sock (socket) :  tcp socket from socket module

    Example:
        client = Client(target = ('xxx.com', 5555))
        print(client.recvline())
        print(client.recvuntil('Input'))
        client.send('b'*41)
        client.interactive()

    Note:
        recv is unstable when receiving '' consectively
    '''

    def __init__(self, sock=None, target=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 ,TCP
        else:
            self.sock = sock

        if target is not None:
            self.connect(target)

    @exception
    def connect(self, target):
        '''
        connect to target

        Parameters:
            target(tuple(str,int)) : (host, port)
        '''
        host, port = target
        self.sock.connect((host, port))

    @exception
    def recv(self):
        '''
        receive till the end

        Returns:
            response (str) : data received from target
        '''

        recv_len = 1
        response = ''
        while recv_len:
            data = self.sock.recv(4096)
            recv_len = len(data)
            response += data.decode('utf-8')
            if recv_len < 4096:
                break
        return response

    @exception
    def recvline(self):
        '''
        receive until \\n

        Returns
            response (str) : data received from target
        '''

        response = ''
        while 1:
            data = self.sock.recv(1)
            if data == b'':
                break
            response += data.decode('utf-8')
            if data == b'\n':
                break
        return response

    def recvuntil(self, msg=None):
        '''
        continue receiving from target until receive msg or \b''

        Parameters:
            msg(str) : message

        Returns:
            response(str) : data received from target
        '''

        response = ''
        while 1:
            data = self.recv()
            response += data
            if data == '':
                break
            elif msg is not None and msg in data:
                break
        return response

    @exception
    def send(self, msg):
        '''
        send msg to target

        Parameters:
            msg(str) : message
        '''

        if type(msg) == str:
            msg = msg.encode('utf-8')
        self.sock.send(msg)

    def sendline(self, msg):
        '''
        send msg with \\n

        Parameters:
            msg(str) : message
        '''

        if type(msg) == str:
            msg = msg.encode('utf-8')
        self.send(msg + b'\n')

    @exception
    def interactive(self):
        '''
        shell mode
        '''
        def receive():
            while 1:
                response = self.recv()
                if response != '':
                    print(response)
        receive_handler = threading.Thread(target=receive)
        receive_handler.setDaemon(True)
        receive_handler.start()

        while 1:
            time.sleep(0.1)
            s = input('$ ')
            self.sendline(s)
