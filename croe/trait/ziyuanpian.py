# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 17:20:39 2019

@author: 97286
"""
__author__='靳伟伟'

import re
from math import ceil
from spider import Spider
class Ziyuanpian:
    '''
    get_film_info:获取每个电影的所有的字段信息
    film_search:搜获电影
    get_show_page_info:获取指定类型的视频列表信息
    get_all_show_page_url:获取网站(首页)所有视频的的url
    get_all_show_page_url_yield:获取网站(首页)所有视频的url的迭代器
    '''
    domain='http://www.ziyuanpian.net/'

    def split_info(self,info_str):
        if '/' in info_str:
            info_str=info_str.split('/')
        elif ',' in info_str:
            info_str=info_str.split(',')
        elif ' ' in info_str:
            info_str=info_str.split(' ')
        else:
            info_str=[info_str]
    def get_film_info(self,url,encoding=None):
        regex=dict(
                imgurl='<img class="lazy" src="(.*?)" alt=".*?" />',
                intro='<div class="vodplayinfo">(.*?)</div>',
                name='<h2>(.*?)</h2>\s+?<span>(.*?)</span>\s+?<label>(.*?)</label>',
                info='\
<li>别名：<span>(.*?)</span></li>\s+?\
<li>导演：<span>(.*?)</span></li>\s+?\
<li>主演：<span>(.*?)</span></li>\s+?\
<li>类型：<span>(.*?)</span></li>\s+?\
<li class="sm">地区：<span>(.*?)</span></li>\s+?\
<li class="sm">语言：<span>(.*?)</span></li>\s+?\
<li class="sm">上映：<span>(.*?)</span></li>\s+?\
<li class="sm">片长：<span>(.*?)</span></li>\s+?\
<li class="sm">更新：<span>(.*?)</span></li>\s+?\
<li class="sm">总播放量：<span><em id="hits">.*?</script></span></li>\s+?\
<li class="sm">今日播放量：<span>(.*?)</span></li>\s+?\
<li class="sm">总评分数：<span>(.*?)</span></li>\s+?\
<li class="sm">评分次数：<span>(.*?)</span></li>',
                show_list='checked="" />(.*?)</li>'
                   )
        info=Spider().get_info(url,encoding=encoding,**regex)
        director=self.split_info(info['info'][0][1])
        actor=self.split_info(info['info'][0][2])
        types=self.split_info(info['info'][0][3])
        area=self.split_info(info['info'][0][4])
        language=self.split_info(info['info'][0][5])
        m3u8_list=[url.split('$') for url in info['show_list'] if url.endswith('.m3u8')]
        xunlei_list=[url.split('$') for url in info['show_list'] if url.endswith('.mp4')]
        yun_list=[url.split('$') for url in info['show_list'] if not url.endswith('.m3u8') and url.endswith('.mp4')]
        film_info=dict(
                imgurl=info['imgurl'][0],
                name=info['name'][0][0],
                name_info=info['name'][0][1],
                grade=info['name'][0][2],
                athour_name=info['info'][0][0],
                director=director,
                actor=actor,
                types=types,
                area=area,
                language=language,
                show_time=info['info'][0][6],
                lens=info['info'][0][7],
                up_date=info['info'][0][8],
                day_plays=info['info'][0][9],
                total_score=info['info'][0][10],
                total_score_number=info['info'][0][11],
                m3u8_list=m3u8_list,
                xunlei_list=xunlei_list,
                yun_list=yun_list
                )
        return film_info
    def film_search(self,keyword,encoding=None):
        post_url='http://www.ziyuanpian.net/index.php?m=vod-search'
        data={'wd':keyword,'submit':'search'}
        regex=dict(info='<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb6">(.*?)</span></li>')
        info=Spider().post_info(post_url,data,encoding,**regex)['info']
        joint_url=self.domain
        info=[{'url':joint_url+url[1:],'name':name,'types':types,'update_time':update_time} for url,name,types,update_time in info]
        return{'search_list':info,'search_word':keyword,'host':self.domain}
    def get_show_page_info(self,url):
        regex=dict(info='<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb[67]">(.*?)</span></li>')
        info=Spider().get_info(url,encoding='utf-8',**regex)['info']
        info=[dict(url='http://www.ziyuanpian.net'+i[0],name=i[1].split('&nbsp')[0],types=i[2],update_time=i[3]) for i in info]
        return{'film_list':info}
    def get_all_show_page_url(self):#获取网站所有的url
        url='http://www.ziyuanpian.net/?m=vod-index-pg-{}.html'
        global page_num
        self.page_num=ceil(int(re.findall('style="margin-bottom:10px;">共(.*?)条数据&nbsp;当前:',Spider().get_html(url.format(1)))[0])/50)
        self.queue=[url.format(i) for i in range(1,self.page_num+1)]
        return self.queue
    def get_all_show_page_url_yield(self):
        url='http://www.ziyuanpian.net/?m=vod-index-pg-{}.html'
        for i in range(1,self.page_num+1):
            yield url.format(i)

if __name__=='__main__':
    url='http://www.ziyuanpian.net/?m=vod-index-pg-2.html'
    x=Ziyuanpian()
#    info=x.get_film_info('http://www.ziyuanpian.net/?m=vod-detail-id-37330.html')
#    info=x.film_search('筑梦情缘')
#    info=x.get_all_show_page_url()
        