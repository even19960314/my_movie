# -*- coding: utf-8 -*-
"""
Created on Thu May 30 08:47:23 2019

@author: 一文 --最远的你们是我最近的爱
"""


import threading
import sys
import json


from redis import StrictRedis
import pymysql as mysql





class FilmAction():
    
   
    
    def __init__(self, film_object):
        
        self.film_object = film_object
        
        self.r = StrictRedis(host='localhost',decode_responses=True,port = 6379)
        
        self.conn=mysql.connect('127.0.0.1','root','','bjfilm')
        
        self.cursor = self.conn.cursor()
        
        self.cursor_lock = threading.Lock()
        
        self.test_db()
        
        self.iter_show_page_url = self.film_object.get_all_show_page_url_yield()
        
        
    ######特征函数#######
    
    def test_db(self):
              
        creart_sql = '''\
        
            CREATE TABLE IF NOT EXISTS film_infos(
            
                    id INTEGER PRIMARY KEY auto_increment,
                    
                    name TEXT,
                    
                    url  varchar(255) UNIQUE,
                    
                    update_time  TEXT,
                    
                    types  TEXT,
                    
                    status TEXT NULL
            
            )
        
        '''
        
        
        self.cursor_lock.acquire()
        
        self.cursor.execute(creart_sql)
        
        self.conn.commit()
        
        self.cursor_lock.release()
      
            
    def work(self):
        
        insert_sql = '''
        
            INSERT INTO film_infos
            
            (name ,url , update_time ,types)
            
            VALUES
            
            (%s ,%s ,%s ,%s)'''
        
        
        while True:
         
            try:
            
                show_page_url = next(self.iter_show_page_url)
                
            except StopIteration:
                
                return
            
            try:
            
                info = self.film_object.get_show_page_info(show_page_url)['film_list']
                
            except:
                
                self.redis.set(show_page_url, str(sys.exc_info()))
                
                print('出错啦', show_page_url)
                
            else:
                
      
                insert_list = [(i['name'], i['url'], i['up_date_time'], i['types']) for i in info]
                
                self.cursor_lock.acquire()
                    
                try:
                    
                    self.cursor.executemany(insert_sql, insert_list)
                    
                except mysql.err.IntegrityError:
                    
                    print(show_page_url, '已经存在')
                    
                    self.cursor_lock.release()
                    
                else:
                    
                    self.conn.commit()
                    
                    print(show_page_url)
                      
                    self.cursor_lock.release()
                
                
            
    def my_thread(self):
        
        for i in range(5):
        
            t = threading.Thread(target = self.work)
            
            t.start()
            
            
    def search_detail(self, keyword, page = None):
        
        if page == None:
            
            page = 0
        
        search_info = self.film_object.film_search(keyword)['search_list'][page * 5 : (page+1)*5]
        
        detail_search_list = []
        
        def run(url):
            
            detail_search_list.append(self.film_object.get_film_info(url))
        
        
        threads = []
        
        for i in range(5):
            
            try:
            
                url = search_info.pop()['url']
                
            except IndexError:
                
                print('search_detail, 任务队列完成')
                
                break
                
            else:
            
                t = threading.Thread(target = run, args = (url,))
                
                threads.append(t)
                
                t.start()
                
        for t in threads:
                
            t.join()
            
        self.r.set(keyword, json.dumps({'info' :detail_search_list}))
        
        return {'info' :detail_search_list}
    
    
    def search_detail_redis(self, keyword):
        
        if self.r.exists(keyword):
            
            return json.loads(self.r.get(keyword))
        
        else: 
            
            return self.search_detail()
            
            
if __name__ == '__main__':
    
    from trait.bj import Filmbj
    
    x = FilmAction(Filmbj())
    
    x.my_thread()
    
    