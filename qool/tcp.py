# -*- coding: utf-8 -*-
'''
TCP tools

Todo:
    implement Server
'''

import socket


def exception(func):
    '''
    error handler
    '''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            print('exiting')
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
        print(client.recvuntil('Input:'))
        client.send('b'*41)
        client.interactive()

    Note:
        recv is unstable when receiving '' consectively

    Todo:
        interactive mode seems to work wrongly, when it has to receive more than one time
    '''

    def __init__(self, sock=None, target=None, timeout = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 ,TCP
        else:
            self.sock = sock

        if target is not None:
            self.connect(target, timeout)

    @exception
    def connect(self, target, timeout = None):
        '''
        connect to target

        Parameters:
            target(tuple(str,int)) : (host, port)
            timeout(int) : second (default = 1)
        '''

        if timeout is None:
            timeout = 1
        self.sock.settimeout(timeout)
        host, port = target
        self.sock.connect((host, port))

    @exception
    def recv(self, n = None):
        '''
        if n is given:
            receive n bytes data
        else:
            receive till the end

        Parameters:
            n(int) : bytes

        Returns:
            response (str) : data received from target
        '''

        response = ''

        try:
            if n is None:
                while 1:
                    data = self.sock.recv(4096).decode('utf-8')
                    if not data:
                        break
                    response += data
            else:
                response = self.sock.recv(n).decode('utf-8')
        except socket.timeout:
            pass

        return response

    def recvline(self):
        '''
        receive until \\n

        Returns
            response (str) : data received from target
        '''

        response = ''
        while 1:
            data = self.recv(1)
            if not data:
                break
            response += data
            if data == '\n':
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
            data = self.recv(1)
            response += data
            # print(data)
            if data == '':
                break
            elif msg is not None and response[-len(msg):] == msg:
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
        self.sock.sendall(msg)

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

        print('-'*30,'INTERACTIVE MODE', '-'*30)
        while 1:
            print(self.recv())
            s = input()
            self.sendline(s)
