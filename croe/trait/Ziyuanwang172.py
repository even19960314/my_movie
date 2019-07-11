# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:46:04 2019

@author: 史红飞
"""
__author__ = '史红飞'
from spider import Spider
import re

class Ziyuanwang172:
    
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
        
            
        url='http://www.172zy.net/?m=vod-detail-id-58510.html'
        regex = dict(
                             
                intro = '<div class="vodplayinfo">(.*?)</div>',
                
                name = '<h2>(.*?)</h2>\s+?<span>(.*?)</span>\s+?<label>(.*?)</label>',
                
                
                
#                info = '\
#<li>别名：<span>(.*?)</span></li>\s+?\
#<li>导演：<span>(.*?)</span></li>\s+?\
#<li>主演：<span>(.*?)</span></li>\s+?\
#<li>连载：<span>(.*?)</span></li>\s+?\
#<li>类型：<span>(.*?)</span></li>\s+?\
#<li>地区：<span>(.*?)</span></li>\s+?\
#<li>语言：<span>(.*?)</span></li>\s+?\
#<li>上映：<span>(.*?)</span></li>\s+?\
#<li>更新：<span>(.*?)</span></li>',
                athour_name ='<li>别名：<span>(.*?)</span></li>',
                director ='<li>导演：<span>(.*?)</span></li>',
                actor ='<li>主演：<span>(.*?)</span></li>',
                state ='<li>连载：<span>(.*?)</span></li>',
                types ='<li>类型：<span>(.*?)</span></li>',
                area ='<li>地区：<span>(.*?)</span></li>',
                language ='<li>语言：<span>(.*?)</span></li>',
                show_time ='<li>上映：<span>(.*?)</span></li>',
                up_date ='<li>更新：<span>(.*?)</span></li>',

                show_list = 'checked="" />(.*?)</li>',
                
                
                imgurl = '<img class="lazy" src="(.*?)" alt=".*?" />'


                )
        
        info = Spider().get_info(url, encoding = encoding, **regex)
  
        director = self.split_info(info['director'][0]) #导演
            
        actor = self.split_info(info['actor'][0]) #主演
        
        state = self.split_info(info['state'][0]) #状态
        
        types = self.split_info(info['types'][0]) #类型
        
        area = self.split_info(info['area'][0])  #区域
        
        language = self.split_info(info['language'][0]) #语言
        
        m3u8_list = [url.split('$')  for url in info['show_list'] if url.endswith('.m3u8')]
        
        yun_list = [url.split('$')  for url in info['show_list'] if not url.endswith('.m3u8')]
        
    
        film_info = dict(
                
                name = info['name'][0][0],
                
                name_info = info['name'][0][1],
                
                grade = info['name'][0][2],
                 
                athour_name = info['athour_name'][0],
                
                director = director,
                
                actor = actor,
                
                state = state,
                
                types = types,
                
                area = area,
                
                language = language,
                
                imgurl = info['imgurl'][0],
                
                show_time = info['show_time'][0],
                
                up_date = info['up_date'][0],
                
                m3u8_list = m3u8_list,
                
                yun_list = yun_list,
                
                day_plays = '',
                
                total_score_number = '',
                
                lens = '',
                
                total_score = '',
                
                
                
                )
        
        
        return film_info
    
    def film_search(self, keyword, encoding = None):
        
        post_url = 'http://www.172zy.net/index.php?m=vod-search'
                   
        
        data = {
                'wd': keyword,
                'submit': 'search',
                
                }
        
        regex = dict(
                                                                                                                                                                                                                                                                                                                                
                info = '<li><span class="tt"></span><span class="xing_vb4"><img class="new" src="/template/172zy/images/Henry_new.gif"> <a href="(.*?)" target="_blank">(.*?)<font color="#FF0000">(.*?)</font>   <img class="new" src="/template/172zy/images/Henry_huo.gif"></span><span class="xing_vb51">(.*?)</span><span class="xing_vb54">(.*?)</span> <span class="xing_vb52">(.*?)</span> <span class="xing_vb53"><font color="#f60">(.*?)</font></span>  <span class="xing_vb[67]">(.*?)</span></a></li>'
                )
        
        info = Spider().post_info(post_url, data, encoding, **regex)['info']
        
#        print(info)
        
        joint_url = self.domain
        
        info = [{'url':joint_url + url[1:], 'name':name, 'update_total':update_total, 'types':types, 'area': area,'show_time':show_time,'grade':grade,'update_time':update_time} for url, name, update_total, types, area, show_time, grade, update_time in info]
        
        return {'search_list': info, 'search_word': keyword, 'host': self.domain}
    
    def get_show_page_info(self,url):
        
        '''
        url:'https://www.subo8988.com/?m=vod-type-id-13.html'
        
        return:
            
            {
            
            #type_name:'香港剧'
            film_list:[
                    
            
            {
                    url: 'https://www.subo8988.com/?m=vod-detail-id-25401.html'
                    name: '宝宝来了[国语版] 20集全/已完结'
                    types: '香港剧'
                    update_time:'2019-05-27'
                
            
            }
            
            ...
            
            
            
            ]
            
            
            }
        
        '''
        regex = dict(
                
                info = '\
<li><span class="tt"></span><span class="xing_vb4"> <a href="(.*?)" target="_blank">(.*?)<font color="#FF0000">(.*?)</font>\s+?\
<img class="new" src="/template/172zy/images/Henry_huo.gif"></span><span class="xing_vb51">(.*?)</span><span class="xing_vb54">(.*?)</span>.*?<span class="xing_vb52">(.*?)</span>.*?<span class="xing_vb53"><font color="#f60">(.*?)</font></span>.*?<span class="xing_vb[67]">(.*?)</span></a></li>'


                
                
                )
        
        info = Spider().get_info(url,encoding = 'utf-8',  **regex)['info']
        
        ls = 'http://www.172zy.net'
        
        info = [dict(url = ls + i[0], name = i[1].split('&nbsp;')[0], update_total = i[2], types = i[3], show_time = i[4], area = i[5], pingfen=i[6], update_time = i[7]) for i in info]
        
        
        
        return {'film_list': info}
        
#        regex=dict(
#                href='\s+?\
#<li><span class="tt"></span><span class="xing_vb4"> <a href="(.*?)" target="_blank">(.*?) <font color="#FF0000">(.*?)</font>.*?',
#                img='<span class="xing_vb51">(.*?)</span><span class="xing_vb54">(.*?)</span> <span class="xing_vb52">(.*?)</span> <span class="xing_vb53"><font color="#f60">(.*?)</font></span>  <span class="xing_vb[67]">(.*?)</span></a></li>'
#                )
#        one_info=Spider().get_info(url,**regex)['href']
#        one_info2=Spider().get_info(url,**regex)['img']
#        joinurl='http://www.172zy.net'
#        for i in one_info:
#            url=joinurl+i[0],
#            name=i[1],
#            name_info=i[2]
#            
#            
#        for i in one_info2:
#            types=i[0],
#            date=i[1],
#            area=i[2],
#            score=i[3],
#            times=i[4]
#        info=[dict(url=url,name=name,name_info=name_info,types=types,date=date,area=area,score=score,times=times)]
#
#        return {'film_list':info}

        
        
        
    
    def get_all_show_page_url(self):
        
        '''
        return:获取 http://www.172zy.net/ 网站所有 show_page_url
        
        '''
        
        url = 'http://www.172zy.net/?m=vod-index-pg-{}.html'
        
        self.queue = [url.format(i) for i in range(1, 536)]
        
        
        return self.queue

    
    
    def get_all_show_page_url_yield(self):

        url = 'http://www.172zy.net/?m=vod-index-pg-{}.html'

        for i in range(1, 536):

            yield url.format(i)
                
    
    def get_all_page(self,url):
        
        rst = Spider().get_html(url)
        
        
        page = int(str(re.findall('<li><div class="pages" style="margin-bottom:10px;">共.*?条数据&nbsp;当前:1/(.*?)页&nbsp;<em>',rst,re.S))[2:-2])
        
        return page
        
if __name__ == '__main__':
    
    url = 'http://www.172zy.net/?m=vod-index-pg-1.html'
    
    x = Ziyuanwang172()
    
#    page = x.get_all_page(url)
    
#    info = x.get_film_info('http://www.172zy.net/?m=vod-detail-id-58510.html')
    
#    info = x.film_search('西游记')
    
    
    #传入一个show_page_url返回所有电影信息

#    info = x.get_show_page_info('http://www.172zy.net/?m=vod-index-pg-9.html')

    #获取网站所有的show_page_url
#    info = x.get_all_show_page_url(page)
    
    #info = x.get_all_show_page_url_yield()