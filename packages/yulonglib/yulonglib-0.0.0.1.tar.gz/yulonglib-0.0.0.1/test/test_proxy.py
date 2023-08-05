#!-*-encoding:utf-8-*-
import socket
import select
import struct
import memcache
import hashlib

class deal_sock():

    def __init__(self):
        self.mc = memcache.Client(["127.0.0.1:11111"],debug=1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 4425))
        self.sock.listen(50)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ins = [self.sock, ] #我自己，和连我的小弟们
        self.ous = []            #连我的小弟们

        # socket -> data to send
        self.data_requests = {}
        self.data_response = {}
        self.data_cachekey = {}
        # socket -> client address, which is (host, port) tuple
        self.adrs = {}
        self.ifcaches={}

        self.sock_high=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock_high.connect(('10.73.12.43', 20012))
        self.sock_high.connect(('127.0.0.1', 4424))
        self.sock_high.settimeout(0.3)

        self.high = [self.sock_high,] #我大哥,y
        self.ins_high = [] 
        self.ous_high = [] 

        self.adrs[self.sock_high]=('127.0.0.1',4424)

    def deal_in(self,x):
        if x is self.sock:
            # 监听套接字上发生input事件，说明有新的连接
            newSock, addr = self.sock.accept()
            print("Connected from: ", addr)
            self.ins.append(newSock)
            self.adrs[newSock] = addr
        else:
            # 连接套接字上发生 input 事件说明有数据可读，或者是client端断开连接
            newData  = x.recv(8192)
            if newData:
                hash_md5 = hashlib.md5(newData[40:])
                url5=hash_md5.hexdigest()
                memdata=self.mc.get(url5)
                if memdata:
                    print 'hit cache'
                    self.data_response[x] = memdata
                    if x not in self.ous:
                        self.ous.append(x) #事件就绪
                else:
                    # 有新的数据到来，此时将准备转发到server的请求入队
                    print("%d bytes from %s" %(len(newData), self.adrs[x]))
                    self.data_requests[x] = self.data_requests.get(x, "") + newData
                    self.data_cachekey[x] = url5
                    if x not in self.ous_high:
                        self.ous_high.append(x) #事件就绪
            else:
                # 连接套接字上发生 input 事件，如果不是有新数据可读，说明是client断开连接
                print("Disconnected from: ", self.adrs[x])
                del self.adrs[x]
                try:
                    self.ous.remove(x)
                except ValueError: 
                    pass
                x.close()
                print 'closed!!!!!'
                self.ins.remove(x)

    def deal_out_high(self,x):
        y=self.sock_high
        tosend = self.data_requests.get(x)
        if tosend:
            # 有 output 事件，说明此时可写
            nsent = y.send(tosend)  #注意这里不是x负责send
            print("%d bytes to %s" %(nsent, self.adrs[y]))
            tosend = tosend[nsent:]
        if tosend:
            print("%d bytes remain for %s" %(len(tosend), self.adrs[y]))
            self.data_requests[x] = tosend
        else:
            print 'else deal_out_high'
            try:
                del self.data_requests[x]
            except KeyError:
                pass
            self.ous_high.remove(x) 
            print("high --No data currently remain for:", self.adrs[y])
        if x not in self.ins_high:
            self.ins_high.append(x) #inhigh事件就绪
        if x not in self.ous: #准备就绪返回给小弟们了
            self.ous.append(x)
    
    def deal_in_high(self,x):
        # 连接套接字上发生 input 事件说明有数据可读，或者是client端断开连接
        y=self.sock_high
        newData = y.recv(8192)
        #a0,a1,a2,a3,a4,a5,a6,a7,a8,a9=struct.unpack("IIIIIIIIII",newData[:40])
        a9=0
        self.data_response[x] = self.data_response.get(x, "") + newData 
        print("%d bytes from %s" %(a9+40, self.adrs[y]))
        a=1
        for i in range(((a9+40)/8192)+1):
            try:
                a+=1
                print a
                newData  = y.recv(8192) #注意这里不是x负责recv,而且要循环接受
                if newData:
                    # 有新的数据到来，此时将准备转发到server的请求入队
                    self.data_response[x] = self.data_response.get(x, "") + newData 
                    #注意这里不是data_requests,它在上一个函数就被del了
            except:
                break
        self.ins_high.remove(x) 
        self.mc.set(self.data_cachekey.get(x,""),self.data_response.get(x,""))

    def deal_out(self,x):
        print "deal_out"
        tosend = self.data_response.get(x) #我根本不知道是否来自缓存
        if tosend:
            # 有 output 事件，说明此时可写
            x.sendall(tosend)
            print("%d bytes to %s" %(len(tosend), self.adrs[x]))
            try:
                del self.data_response[x]
            except KeyError:
                pass
            #如果在deal_in_high的时候就干掉的话，第二个select执行不了，会影响这里
            self.ous.remove(x)
            print("No data currently remain for:", self.adrs[x])
    
    def run(self):
        try:
            print("Select Server Start Working!")
            while True:
                i,oh,e  = select.select(self.ins, self.ous_high, [])
                for x in i: # 处理发生 input 事件的套接字
                    self.deal_in(x)
                for x in oh: # 处理发生 output 事件的套接字
                    self.deal_out_high(x)
                ih,o,eh = (self.ins_high, self.ous, [])
                for x in ih: # 处理发生 input 事件的套接字
                    self.deal_in_high(x)
                for x in o: # 处理发生 output 事件的套接字
                    self.deal_out(x)
        except Exception as e:
            print e
        finally:
            self.sock.close()
            self.sock_high.close()
            print 'closed!!!!!'

DEAL_SOCK=deal_sock()
DEAL_SOCK.run()
        
