# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:28:18 2019

@author: 一文 --最远的你们是我最近的爱
"""

import requests

class Spider:
    
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            }    
    def get_html(self, url, encoding = None):
        
        r = requests.get(url, verify = False, timeout = 5,headers = self.headers)
        
        if encoding == None:
        
            r.encoding= r.apparent_encoding
        
        else:
            
            r.encoding = encoding
            
        return r.text
    
    def post_html(self, url, data, encoding = None):
        
        r = requests.post(url, headers = self.headers, data = data, verify = False)
        
        if encoding == None:
        
            r.encoding= r.apparent_encoding
        
        else:
            
            r.encoding = encoding
            
        return r.text
    
    def get_info(self, url, encoding = None, **regex):#位置参数要在关键字参数之前
        
        '''
        
        {'name':'.*?', 'year':''}
        
        '''
        
        html = self.get_html(url)
        
        for reg in regex:
            
            regex[reg] = re.findall(regex[reg], html)
            
        
        return regex
    
    def post_info(self, url, data, encoding = None, **regex):
        
        
        html = self.post_html(url, data, encoding = encoding)
        
        
        for reg in regex:
            
            regex[reg] = re.findall(regex[reg], html)
            
        
        return regex
        
        
    

    
  
    
    