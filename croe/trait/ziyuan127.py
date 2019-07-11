# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:01:32 2019

@author: 史红飞
"""
from spider import Spider

import re

class Film:
    
    '''
    def get_film_info(self, url, encoding = None): 
        
        传入一个电影详情链接，清洗该链接数据
        
    def film_search(self, keyword, encoding = None):
        
        传入一个关键字，返回关键字的在网站的搜索结果
        
    def get_show_page_info(self,url):
        
        传入一个show_page_url返回所有电影信息
        
    def get_all_show_page_url(self):
        
        获取网站所有的show_page_url
        
    def get_all_show_page_url_yield(self):
        
        获取网站所有的show_page_url的迭代器
     def get_all_page(self,url):
         
         动态获取网站的页数
    
    
    '''
    
    domain = 'http://www.172zy.net/'
    
    
    def split_info(self, info_str):#一个用在清洗数据的方法
        
        if '/' in info_str:#表示导演用/分割开来
            
            info_str = info_str.split('/')
            
        elif ',' in info_str:
            
            info_str = info_str.split(',')
            
        elif ' ' in info_str:
            
            info_str = info_str.split(' ')
            
        else:
            
            info_str = [info_str]
            
        return [i.strip() for i in info_str if i != '']
        
        
    
    def get_film_info(self, url, encoding = None):
        
                
        regex = dict(
                
                introduce = '<div class="vodplayinfo">(.*?)</div>', ##剧情介绍
                
                name = '<h2>(.*?)</h2>\s+?<span>(.*?)</span>\s+?<label>(.*?)</label>',
                
                info = '\
<li>别名：<span>(.*?)</span></li>\s+?\
<li>导演：<span>(.*?)</span></li>\s+?\
<li>主演：<span>(.*?)</span></li>\s+?\
<li>连载：<span>(.*?)</span></li>\s+?\
<!-- <li>全集：<span>(.*?)</span></li> -->\s+?\
<li>类型：<span>(.*?) </span></li>\s+?\
<li>地区：<span>(.*?)</span></li>\s+?\
<li>语言：<span>(.*?)</span></li>\s+?\
<li>上映：<span>(.*?)</span></li>\s+?\
<li>更新：<span>(.*?)</span></li>',
    
                show_list = 'checked="" />(.*?)</li>'
                
                )
        
        info = Spider().get_info(url, encoding = encoding, **regex)
        
        director = self.split_info(info['info'][0][1])
            
        actor = self.split_info(info['info'][0][2])
        
        serialize = self.split_info(info['info'][0][3])
        
        types = self.split_info(info['info'][0][4])
        
        area = self.split_info(info['info'][0][5])
        
        language = self.split_info(info['info'][0][6])
        
        m3u8_list = [url.split('$')  for url in info['show_list'] if url.endswith('.m3u8')][1:]
        
        zy_list = [url.split('$')  for url in info['show_list'] if not url.endswith('.m3u8')][:-1]
        
    
        film_info = dict(
                
                name = info['name'][0][0],##影名
                
                name_info = info['name'][0][1],##更新到几集
                
                grade = info['name'][0][2],##评分
                
                athour_name = info['info'][0][0],##别名
                
                director = director,##导演
                
                actor = actor,##主演
                
                serialize = serialize,##连载
                
                types = types,##类型
                
                area = area,##地区
                
                language = language,##语言
                
                show_time = info['info'][0][7],##上映时间
                
                up_date = info['info'][0][8],##更新时间
                
                m3u8_list = m3u8_list,
                
                zy_list = zy_list,
                
                )
        
        
        return film_info
    
    
    def film_search(self, keyword, encoding = None):
        
        post_url = 'http://www.172zy.net/index.php?m=vod-search'
        

        data = {
                'wd': keyword,
                'submit': 'search',
                
                }
        
        regex = dict(

            info='<li><span class="tt"></span><span class="xing_vb4"><img class="new" src=".*?"> <a href="(.*?)" target="_blank">(.*?) <font color="#FF0000">(.*?)</font>   <img class="new" src=".*?"></span><span class="xing_vb51">(.*?)</span><span class="xing_vb54">(.*?)</span> <span class="xing_vb52">(.*?)</span> <span class="xing_vb53"><font color="#f60">(.*?)</font></span>  <span class="xing_vb6">(.*?)</span></a></li>'

                )
        
        info = Spider().post_info(post_url, data, encoding, **regex)['info']
                        
        joint_url = self.domain
        
        info = [{'url':joint_url + url[1:], 'name':name, 'update_total':update_total, 'types':types, 'area': area,'show_time':show_time,'grade':grade,'update_time':update_time} for url, name, update_total, types, area, show_time, grade, update_time in info]
        
        return {'search_list': info, 'search_word': keyword, 'host': self.domain}
    
    
    def get_show_page_info(self,url):
        
  
        regex = dict(
                
                info = '<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb6">(.*?)</span></li>'
                
                
                )
        
        info = Spider().get_info(url,encoding = 'utf-8',**regex)['info']
        
        joint_url = self.domain
        
        info = [{'url':joint_url + url[1:], 'name':name, 'types':types, 'update_time': update_time} for url, name, types, update_time in info]
        
        return {'film_list': info}
        

    def get_all_show_page_url(self):
        
        '''
        return:获取 http://www.156zy.co/ 网站所有 show_page_url
        
        '''
        
        url = 'http://www.172zy.net/?m=vod-index-pg-{}.html'
        

        self.queue = [url.format(i) for i in range(1,538)]
           
        return self.queue

    
    
    def get_all_show_page_url_yield(self):

        url = 'http://www.172zy.net/?m=vod-index-pg-{}.html'

        for i in range(1,538):

            yield url.format(i)
    
    def get_all_page(self,url):
        
        rst = Spider().get_html(url)
        
        page = int(str(re.findall('<li><div class="pages" style="margin-bottom:10px;">共.*?条数据&nbsp;当前:1/(.*?)页&nbsp;<em>',rst,re.S))[2:-2])
        
        return page
        
if __name__ == '__main__':
    
    url = 'http://www.172zy.net/?m=vod-index-pg-1.html'
    
    x = Film()
    
#    page = x.get_all_page(url)
    
#    info = x.get_film_info('http://www.172zy.net/?m=vod-detail-id-60113.html')
    
#    info = x.film_search('岳母大人')
    
    
    #传入一个show_page_url返回所有电影信息
#    info = x.get_show_page_info('http://www.172zy.net/?m=vod-index-pg-2.html')

    #获取网站所有的show_page_url
#    info = x.get_all_show_page_url(page)
    
    #info = x.get_all_show_page_url_yield()
        
        



