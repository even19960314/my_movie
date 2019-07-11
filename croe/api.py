# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:28:58 2019

@author: 一文 --最远的你们是我最近的爱
"""


import sys
sys.path.append('trait')#添加文件夹到变量空间
import redis
import importlib
import queue
import threading
import json
import requests
from urllib3.exceptions import NewConnectionError
from script_trait import trait_info


trait_info = trait_info()

class FilmApi:
    
    def __init__(self):
    
        
        pool = redis.ConnectionPool(host = '127.0.0.1', port = 6379, decode_responses = True)
        
        self.r = redis.StrictRedis(connection_pool=pool)
        
        self.q = queue.Queue(5)#创建一个队列对象，queue.LifoQueue,创建一个堆栈，还有一个优先级队列
        
        self.search_info = {}
    
    def film_search(self, keyword):
        
        #trait = __import__('FilmSubo8988')
        
        class_list = []#生成一个所有类的列表
        
        for i in trait_info:
        
            trait = importlib.import_module(i.replace('trait\\', '').replace('.py', ''))

            #trait = __import__(i.replace('trait\\', '').replace('.py', ''))#和上面的方法效果一样
        
            class_list.append(getattr(trait, trait_info[i]))#getattr方法相当于trait.xxx,但getattr传的方法是一个字符串
            
        
            
        return [i().film_search(keyword) for i in class_list]


    def producer(self):
        
        for i in trait_info:
        
            trait = importlib.import_module(i.replace('trait\\', '').replace('.py', ''))
            
            self.q.put(getattr(trait, trait_info[i]))
            
    def consumer(self, keyword):
        
        while True:
            
            task = self.q.get()
            
            if task == None:
                    
                break
            
            task_class = task()
            
            try:
            
                info = task_class.film_search(keyword)
                
            except NewConnectionError:
                
                self.q.task_done()
                
                print(task_class.domain, '失败')
                
            except requests.exceptions.ConnectionError:
                
                self.q.task_done()
                
                print(task_class.domain, '失败')
            
            except Exception:
                                
                self.q.task_done()
                
                print(task_class.domain, '失败')
                
            else:
            
                self.search_info[task_class.domain] = info
                
                print(task_class.domain, '完成')
                
                self.q.task_done()
                
    def my_thread(self, keyword):
        
        #self.consumer(keyword)
        
        if self.r.exists(keyword):
            
            print(keyword, '搜索结果在redis里有')
            
            return json.loads(self.r.get(keyword))
        

        threads = []
        
        for i in range(len(trait_info)):
        
            t = threading.Thread(target = self.consumer, args = (keyword,))
            
            t.start()
            
            threads.append(t)
            
        
        self.producer()
        
        self.q.join()
        
        for i in range(len(trait_info)):
            
            self.q.put(None)
            
            
        for t in threads:
            
            t.join()
            
            
        self.r.set(keyword, json.dumps(self.search_info,ensure_ascii = False), ex = 6*60*60)
            
            
        
        return self.search_info
        
        
            
        
        
if __name__ == '__main__':
    
    x= FilmApi()
    #info = x.my_thread('西游记')

    
    
    


    
    
