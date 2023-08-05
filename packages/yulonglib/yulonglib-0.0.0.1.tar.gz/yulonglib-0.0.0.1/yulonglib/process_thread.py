from multiprocessing import Process
import threading
import random

class Process_thread():

    def __init__(self,pnum,myclass,lists):
        self.lists=lists
        self.myclass=myclass
        self.pnum=pnum

    def thread_run(self,arg1,arg2):
        MYCLASS=self.myclass(arg1,arg2)
        MYCLASS.run()

    def multi_run(self,mylist):
        tlist=[]
        if len(mylist)==1:
            self.thread_run(mylist[0][0],mylist[0][1])
        else:
            for x in mylist:
                t = threading.Thread(target=self.thread_run,name=random.randint(1,100), args=x)
                t.start()
                tlist.append(t)
            for t in tlist:
                t.join()

    def run(self):
        pool=[]
        tnum=len(self.lists)/self.pnum
        for list1 in self.lists:
            p = Process(target=self.multi_run, args=(list1,))
            p.start()
            pool.append(p)
        for p in pool:
            p.join()
