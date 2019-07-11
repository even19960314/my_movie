# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 07:55:56 2019

@author: 一文 --最远的你们是我最近的爱
"""
import importlib
import sys
import redis
import time
import json
import pymongo
from croe.script_trait import TraitAPI
from multiprocessing.dummy import Pool

sys.path.append('trait')
trait_info = TraitAPI().trait_info()



class Film_spider():
    
    def __init__(self):
        
        pool = redis.ConnectionPool(host = '127.0.0.1', port = 6379, decode_responses = True)
        
        self.r = redis.StrictRedis(connection_pool=pool)
        
        self.client = pymongo.MongoClient('127.0.0.1', 27017)
        
    def get_all_class(self):
                
        class_list = []
        
        for i in trait_info:
        
            trait = importlib.import_module(i.replace('E:\\myProgram\\film\\my_film\\croe\\trait\\', '').replace('.py', ''))
        
            class_list.append(getattr(trait, trait_info[i]))
            
        return class_list
            
    def film_search_urls(self,args):
        
        all_infos = []        
                                        
        try:
        
            infos = args[0]().film_search(args[1])
                    
            all_infos.append(infos)
            
            print(args[0].domain,'完成')
            
        except Exception:
            
            print(args[0].domain,'失败')
        
        return all_infos
                


    def pro(self,keyword):
        
        class_list = self.get_all_class()
        
        args_list = []
        
        for i in class_list:
            
            args = (i,keyword)
            
            args_list.append(args)
            
        p = Pool(20)
        
        return p.map(self.film_search_urls,args_list)
    
        
    

    
    
    def film_all_info(self,url):
                
        all_infos = []

        class_list = self.get_all_class()
        
        for i in class_list:
            
            if url.split('?')[0] == i().domain:
                
                try:
                    
                    infos = i().get_film_info(url)
                    
                    infos['url'] = url
                
                    print(url)
                
                    all_infos.append(infos)
                    
                except Exception:
                    
                    print('err')
        
        return all_infos
        
    def film_search_api(self,keyword):    
        
        p = Pool(20)
        
        info = self.pro(keyword)
        
        info = [i for i in info if len(i)!=0]
        
        ls = [i[0]['search_list'] for i in info]
        
        urls = [j['url'] for i in ls for j in i]
                
        return p.map(self.film_all_info,urls)

    
    def get_all_urls(self):
        
        urls = []
        
        class_list = self.get_all_class()
            
        for i in class_list:
            
            iter_show_page_url = i().get_all_show_page_url_yield() 
            
            while True :
            
                try:
                
                    show_page_url = next(iter_show_page_url)
                
                    urls.append(show_page_url)
                    
                except StopIteration:
                    
                    print('迭代完毕')
                    
                    break
            
        return urls
    
    def building_one_index(self):
        
        urls = self.get_all_urls()
        
        for url in urls:
            
            self.r.rpush('urls',url)
            
        

    def get_film_url(self,url):
                
        class_list = self.get_all_class()

        for i in class_list:
            
            if url.split('?')[0] == i().domain:
            
                try:
                
                    info = i().get_show_page_info(url)
                    
                    self.client.film.film_info.insert_many(info['film_list'])
                
                    for k in info['film_list']:
                
                        url = k['url']
                       
                        self.r.rpush('film_urls',url)
                    
                        print(url)
                
                except Exception:
                    
                    self.r.rpush('error_urls',url)
    
    def building_film_index(self):
                
        p = Pool(20)
        
        urls = self.get_all_urls()
                       
        p.map(lambda i:self.get_film_url(i),urls)
        
        
    
    def get_all_indexs(self):
        
       return self.r.lrange('urls',0,-1)
   
    def get_all_film_info(self,url):
                
        class_list = self.get_all_class()
                        
        for i in class_list:
            
            if url.split('?')[0] == i().domain:
        
                try:
                
                    info = i().get_film_info(url)
        
                    self.client.film.film_all_info.insert_many([info])
            
                    print(url)
                    
                except Exception:
                    
                    self.r.rpush('err_urls',url)

    
    def muilt_pro(self):
        
        p = Pool(20)
        
        urls = self.r.lrange('film_urls',0,-1)
                       
        p.map(lambda i:self.get_all_film_info(i),urls)
    
    def run(self,keyword):
        
        if self.r.exists(keyword):
            
            print(keyword, '搜索结果在redis里有')
            
            return json.loads(self.r.get(keyword))
        
        infos = self.film_search_api(keyword)
    
        infos = [i for i in infos if len(i)!=0]
            
        infos = [i for i in infos if keyword in i[0]['name']]
        
        infos = {'search_detail' :{keyword:infos}}
        
        ls = []
    
        for i in infos['search_detail'][keyword]:
        
            ls.append(i[0])
            
        infos = {'search_detail':{keyword:ls}}
        
        self.r.set(keyword, json.dumps(infos,ensure_ascii = False), ex = 6*60*60)

        return infos
    
    def play(self,url):
                
        if self.r.exists(url):
            
            print(url, '该影片在redis里有')
            
            return json.loads(self.r.get(url))
        
        class_list = self.get_all_class()
        
        for i in class_list:
            
            if url.split('?')[0] == i().domain:
                
                try:
                    
                    infos = i().get_film_info(url)
                    
                    infos['url'] = url
                
                    print(url)
                    
                    self.r.set(url, json.dumps(infos,ensure_ascii = False), ex = 6*60*60)
                
                except Exception:
                    
                    infos = ''
                    
                    print('err')
        
        return infos
    
if __name__ == '__main__':
    
    x = Film_spider()
    
    start=time.time()
    
    infos = x.play('http://www.156zy.co/?m=vod-detail-id-34368.html')
    
#    infos = x.run('谍影重重')
    
#    infos = x.pro('谍影重重5')
    
    print('耗时:',time.time()-start)
    

    
    
        
        
        
    