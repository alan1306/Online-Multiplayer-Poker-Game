import socket
import _pickle as pickle
class Network:
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server='192.168.56.1'
        self.port=5555
        self.addr=(self.server,self.port)
    def connect(self,name):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode(name))
            value=self.client.recv(8)
            return int(value.decode())
        except:
            print("not able to connect")

