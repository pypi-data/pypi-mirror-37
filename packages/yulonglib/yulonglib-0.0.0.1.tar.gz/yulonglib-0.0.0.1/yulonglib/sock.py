import socket

class Sock():

    def bind(self,addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,204800)
        self.sock.bind(addr)
        self.sock.listen(30)
        return self.sock

    def connect(self,addr):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF,204800)
        self.sock.settimeout(0.4)
        try:
            self.sock.connect(addr)
        except OverflowError:
            self.sock.connect((addr[0],addr[1]%65536))
        return self.sock
            
