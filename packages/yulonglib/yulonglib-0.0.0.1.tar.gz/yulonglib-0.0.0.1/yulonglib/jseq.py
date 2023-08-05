#-*-coding:utf-8-*-
import requests
import copy

class Jseq():

    def __init__(self,url,cookies):

        self.url=url
        self.cookies  =cookies
        self.s = requests.session()

    def get_json(self,result,tags):

        for i in tags[:-1]:
            result=result[i]
        return result.get(tags[-1])

    def j_root(self,results,tags,rootlist):
        #没有一层层return的递归

        if tags:
            if isinstance(results,dict):
                result=results.get(tags.pop(0))
                self.j_root(result,tags,rootlist)
            elif isinstance(results,list):
                if results and isinstance(results[0],dict):
                    tag=tags.pop(0)
                    for result in results:
                        if isinstance(result,dict):
                            r=result.get(tag)
                            self.j_root(r,tags,rootlist)
                elif results and isinstance(results[0],list):
                    for result in results:
                        self.j_root(r,tags,rootlist)
        else:
            rootlist+=results


    def l_dict(self,rootlist,tagsk,tagsv):
        mydict={}
        for result in rootlist:
            k=self.get_json(result,tagsk)
            mydict[k]={}
            for tagv in tagsv:
                mydict[k]["|".join(map(str,tagv))]=self.get_json(result,tagv)
        return mydict

    def j_dict(self,start,end,tagsr,tagsk,*tagsv):
        tagsv = map(lambda tagv:tagv if isinstance(tagv,tuple) else (tagv,) ,tagsv)
        if not isinstance(tagsr,tuple):
            tagsr=(tagsr,)
        tagsr=list(tagsr)
        if not isinstance(tagsk,tuple):
            tagsk=(tagsk,)

        err=[]
        rootlist=[]
        if start==end==0:
            url=self.url
            resp=self.s.get(url,cookies=self.cookies)
            if not resp:
                return {},err
            jsondata = resp.json()
            self.j_root(jsondata,tagsr,rootlist)
            mydict=self.l_dict(rootlist,tagsk,tagsv)
            return mydict,err
        for i in range(start,end+1):
            url=self.url+str(i)
            resp=self.s.get(url,cookies=self.cookies)
            if not resp:
                continue
            jsondata = resp.json()
            mytagsr=copy.deepcopy(tagsr)
            self.j_root(jsondata,mytagsr,rootlist)
        mydict=self.l_dict(rootlist,tagsk,tagsv)
        return mydict,err
 
    def l_filter(self,rootlist,func,*tagsks): 
        mylist=[ i for i in rootlist if func(*[self.get_json(i,tagsk) for tagsk in tagsks]) ]
        return mylist

    def j_filter(self,start,end,func,tagsr,*tagsk):

        if not isinstance(tagsr,tuple):
            tagsr=(tagsr,)
        tagsr=list(tagsr)
        tagsk = map(lambda tagk:tagk if isinstance(tagk,tuple) else (tagk,) ,tagsk)

        err=[]
        rootlist=[]
        if start==end==0:
            url=self.url
            resp=self.s.get(url,cookies=self.cookies)
            if not resp:
                return {},err
            jsondata = resp.json()
            self.j_root(jsondata,tagsr,rootlist)
            mylist=self.l_filter(rootlist,func,*tagsk)
            return mydict,err
        for i in range(start,end+1):
            url=self.url+str(i)
            resp=self.s.get(url,cookies=self.cookies)
            if not resp:
                continue
            jsondata = resp.json()
            mytagsr=copy.deepcopy(tagsr)
            self.j_root(jsondata,mytagsr,rootlist)
        mydict=self.l_filter(rootlist,func,*tagsk)
        return mydict,err
 
    def l_list(self,rootlist,*tagsk): 
        mylist=[ self.get_json(i,tagsk) for i in rootlist ]
        return mylist

    def j_list(self,start,end,tagsr,*tagsk):

        if not isinstance(tagsr,tuple):
            tagsr=(tagsr,)
        tagsr=list(tagsr)

        err=[]
        rootlist=[]
        if start==end==0:
            url=self.url
            resp=self.s.get(url,cookies=self.cookies)
            if not resp:
                return [],err
            jsondata = resp.json()
            self.j_root(jsondata,tagsr,rootlist)
            mylist=self.l_list(rootlist,*tagsk)
            return mylist,err
        for i in range(start,end+1):
            url=self.url+str(i)
            resp=self.s.get(url,cookies=self.cookies)
            if not resp:
                continue
            jsondata = resp.json()
            mytagsr=copy.deepcopy(tagsr)
            self.j_root(jsondata,mytagsr,rootlist)
        mylist=self.l_list(rootlist,*tagsk)

        return mylist,err

