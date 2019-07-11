# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:18:44 2019

@author: 15633
"""
__author__='王张延'
from spider import Spider

class Mtemp:
    domain = 'http://www.okzyw.com/'
    def split_info(self,info_str):
        if ' ' in info_str:
            info_str=info_str.split(' ')
        elif ',' in info_str:
            info_str=info_str.split(',')
        elif '/' in info_str:
            info_str=info_str.split('/')
        else:
            info_str=[info_str]
        return [i.strip() for i in info_str if i != '']
    
    
    def get_film_info(self,url,encoding=None):
        
        regex=dict(
                imgurl='<img class="lazy" src="(.*?)" alt=".*?" />',
                name='<h2>(.*?)</h2> \s+?<span>(.*?)</span> \s+?<label>(.*?)</label>',
                info= '<li>别名：<span>(.*?)</span></li>\s+?\
<li>导演：<span>(.*?)</span></li>\s+?\
<li>主演：<span>(.*?)</span></li>\s+?\
<li>类型：<span>(.*?)</span></li> \s+\
<li class="sm">地区：<span>(.*?)</span></li>\s+?\
<li class="sm">语言：<span>(.*?)</span></li>\s+?\
<li class="sm">上映：<span>(.*?)</span></li>\s+?\
<li class="sm">片长：<span>(.*?)</span></li>\s+?\
<li class="sm">更新：<span>(.*?)</span></li>\s+?\
<li class="sm">总播放量：<span>(.*?)</span></li>\s+?\
<li class="sm">今日播放量：<span>(.*?)</span></li>\s+?\
<li class="sm">总评分数：<span>(.*?)</span></li>\s+?\
<li class="sm">评分次数：<span>(.*?)</span></li>',
                show_list='<input type="checkbox" name="copy_sel" value=".*?" checked="" />(.*?)</li> '
                )

        info=Spider().get_info(url,encoding=encoding,**regex)
        finally_dic=dict(
                imgurl=info['imgurl'],
                name=self.split_info(info['name'][0][0]),
                name_info=self.split_info(info['name'][0][1]),
                grade=self.split_info(info['name'][0][2]),
                athour_name=self.split_info(info['info'][0][0]),
                director=self.split_info(info['info'][0][1]),
                actor=self.split_info(info['info'][0][2]),
                types=self.split_info(info['info'][0][3]),
                area=self.split_info(info['info'][0][4]),
                language=self.split_info(info['info'][0][5]),
                show_time=self.split_info(info['info'][0][6]),
                lens=self.split_info(info['info'][0][7]),
                up_date=self.split_info(info['info'][0][8]),
                zongpingfen=self.split_info(info['info'][0][9]),
                day_plays=self.split_info(info['info'][0][10]),
                total_score=self.split_info(info['info'][0][11]),
                total_score_number=self.split_info(info['info'][0][12]),
                m3u8_list=[url.split('$')  for url in info['show_list'] if url.endswith('.m3u8')],
                xunlei_list=[url.split('$')  for url in info['show_list'] if url.endswith('.mp4')],
                yun_list=[url.split('$')  for url in info['show_list'] if not url.endswith('.m3u8') and not url.endswith('.mp4')]
                
                 )

        return finally_dic
    
    
    def film_search(self,keyword,encoding=None):
        
        post_url='http://www.okzyw.com/index.php?m=vod-search'
        data={
               'wd': keyword,
               'submit': 'search' 
                }
        regex=dict(
                info='<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb6">(.*?)</span></li>'
                )
        info=Spider().post_info(post_url,data,encoding,**regex)['info']
        urls=self.domain
        infos=[{'url':urls+url[1:],'name':name,'types':types,'update_time':update_time} for url,name,types,update_time in info]
        return {'search_list':infos,'search_word':keyword,'host':self.domain}
    
    
    def get_show_page_info(self,url):
        
        regex=dict(
                info='<a href="(.*?)" target="_blank">(.*?)&nbsp<font color=#FF0000>.*?</font></a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb.*?">(.*?)</span></li>'
                )
        info=Spider().get_info(url,encoding='utf-8',**regex)['info']
        
        joint_url = self.domain
        
        info = [dict(url = joint_url+i[0], name = i[1].split('&nbsp;')[0], types = i[2], update_time = i[3]) for i in info]
        
        
        return {'film_list': info}
    
    def get_all_show_page_url(self):
        
        url = 'http://www.okzyw.com/?m=vod-index-pg-{}.html'
        
        self.queue = [url.format(i) for i in range(1, 669)]
        
        
        return self.queue

    
    
    def get_all_show_page_url_yield(self):

        url = 'http://www.okzyw.com/?m=vod-index-pg-{}.html'

        for i in range(1, 669):

            yield url.format(i)
    
if __name__=='__main__':
    url='http://www.okzyw.com/?m=vod-detail-id-26773.html'
    #url='http://www.123ku.com/?m=vod-index-pg-1.html'
    x=Mtemp()
    #info=x.get_all_show_page_url()
    info=x.get_film_info(url)
    #info=x.film_search('')
    #info=x.get_show_page_info('http://www.123ku.com/?m=vod-index-pg-1.html')
    

    
    
   
    
    
    

    
    
