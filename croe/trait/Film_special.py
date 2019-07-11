# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:42:01 2019

@author: 杨兴伟
"""

#import re
#
#import requests

__author__ = '杨兴伟'

from spider import Spider

class Film_special:
    
    '''
    
    def split_info(self, info_str):
        
        数据清洗
        
    def film_search(self, keyword, encoding=None):
        
        搜索关键字及内容
        
    def get_show_page_info(self, url):
        
        获取某页的所有film列表
        
    def get_all_show_page_url(self):
        
        获取网站每页的url
        
    def get_all_show_page_url_yield(self):
        
        使用yield迭代
        
    def get_film_info(self, url, encoding = None):
        
        详情页film信息
         
    '''
    
    domain = 'http://www.kukuzy.com'
    
    def split_info(self, info_str):
        
        if ',' in info_str:
            
            info_str = info_str.split(',')
            
        elif '/' in info_str:
            
            info_str = info_str.split('/')
            
        elif ' ' in info_str:
            
            info_str = info_str.split(' ')
            
        else:
            
            info_str = [info_str]
            
        return [i.strip() for i in info_str if i!='']   
    
    #搜索页关键字及搜索后的内容
    def film_search(self, keyword, encoding=None):
        
        data = {
                
                'wd': keyword,
                
                'submit': 'search'
                
                }
        
        
        regex = dict(
                
                info = '\
<span class="tt"></span><span class="xing_vb4"> <a href="(.*?)" target="_blank">(.*?)<font color="#FF0000">(.*?)</font>\s+?\
<img class="new" src="/template/kuku/images/huo.gif"></span><span class="xing_vb51">(.*?)</span><span class="xing_vb54">(.*?)</span> <span class="xing_vb52">(.*?)</span> <span class="xing_vb53"><font color="#f60">(.*?)</font></span>  <span.*?>(.*?)</span></a></li>'


                )
        
        post_url = 'http://www.kukuzy.com/?m=vod-index.html'
        
        info = Spider().post_info(post_url, data, encoding, **regex)['info']
        
#        print(info)
        
        index_url = self.domain
        
        info = [{'url':index_url+url, 'name':name, 'screen_massg':screen_massg, 'types':types, 'years':years, 'area':area, 'douban_score':douban_score, 'update_time':update_time} for url, name, screen_massg, types, years, area, douban_score, update_time in info]
        
        return {'search_list':info, 'search_word':keyword, 'host':self.domain}
    
    #获取某页的所有film列表字段
    def get_show_page_info(self, url):
        
        url = 'http://www.kukuzy.com/?m=vod-index-pg-2.html'
        
        regex = dict(
                
                info = '\
<li><span class="tt"></span><span class="xing_vb4"> <a href="(.*?)" target="_blank">(.*?)<font color="#FF0000">(.*?)</font>\s+?\
<img class="new" src="/template/kuku/images/huo.gif"></span><span class="xing_vb51">(.*?)</span><span class="xing_vb54">(.*?)</span> <span class="xing_vb52">(.*?)</span> <span class="xing_vb53"><font color="#f60">(.*?)</font></span>  <span.*?>(.*?)</span></a></li>'
                )
        
        info = Spider().get_info(url, encoding = 'utf-8', **regex)['info']
        
        info = [dict(url = i[0], name = i[1], screen_massg = i[2], types = i[3], years = i[4], area = i[5], douban_score = i[6], update_time = i[7]) for i in info]
    
        return {'film_list':info}
    
    #获取网站每页的url
    def get_all_show_page_url(self):
        
        ba_url = 'http://www.kukuzy.com/?m=vod-index-pg-{}.html'
        
        self.queue = [ba_url.format(str(i)) for i in range(1,485)]
        
        return self.queue
    
    def get_all_show_page_url_yield(self):
        
        url = 'http://www.kukuzy.com/?m=vod-index-pg-{}.html'
        
        for i in range(1, 485):
            
            yield url.format(i)
    
    #详情页
    def get_film_info(self, url, encoding = None):
        
        regex = dict(
                
                pr_info = '\
<h2>(.*?)</h2>\s+?\
<span>(.*?)</span>\s+?\
<label>(.*?)</label>',

                imgurl = '<img class="lazy" src="(.*?)" alt=".*?" />',
                       
                info = '\
<li>别名：<span>(.*?)</span></li>\s+?\
<li>导演：<span>(.*?)</span></li>\s+?\
<li>主演：<span>(.*?)</span></li>\s+?\
<li>连载：<span>(.*?)</span></li>\s+?\
<!-- <li>全集：<span>0</span></li> -->\s+?\
<li>类型：<span>(.*?)</span></li>\s+?\
<li>地区：<span>(.*?)</span></li>\s+?\
<li>语言：<span>(.*?)</span></li>\s+?\
<li>上映：<span>(.*?)</span></li>\s+?\
<li>更新：<span>(.*?)</span></li>',

                jianjie = '<div class="vodplayinfo">(.*?)</div>', 
                
                film_url = '<input type="checkbox" name="copy_sel" value="(.*?)" checked="" />'

                )
        
        thr_info = Spider().get_info(url, encoding, **regex)
        
        film_info = {
                
                'name': thr_info['pr_info'][0][0],
                
                'screen_massg' : thr_info['pr_info'][0][1],
                
                'douban_score' : thr_info['pr_info'][0][2],
                
                'imgurl' : thr_info['imgurl'],
                
                'athour_name' : thr_info['info'][0][0],
                
                'directors' : self.split_info(thr_info['info'][0][1]),
                
                'actors' : self.split_info(thr_info['info'][0][2]),
                
                'lianzai' : thr_info['info'][0][3],
                
                'type' : self.split_info(thr_info['info'][0][4]),
                
                'atea' : self.split_info(thr_info['info'][0][5]),
                
                'language' : self.split_info(thr_info['info'][0][6]),
                
                'show_date' : thr_info['info'][0][7],
                
                'updata_time' : thr_info['info'][0][8],
                
                'jianjie' : thr_info['jianjie'],
                
                'film_url' : thr_info['film_url']
                
                
                
                }
        
        return film_info
        
        
        
                
        
            
        
if __name__ == '__main__':
    
    url= 'http://www.kukuzy.com/?m=vod-index-pg-2.html'
    
#    url2 = 'http://www.kukuzy.com/?m=vod-detail-id-165399.html'
    
    x = Film_special()
    
    info = x.film_search('筑梦情缘') 
#    info2 = x.get_show_page_info(url)  
#    info3 = x.get_film_info(url2)
        
        
        
        
        