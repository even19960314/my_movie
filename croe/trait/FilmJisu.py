# -*- coding: utf-8 -*-
"""
Created on Fri May 31 07:46:46 2019

@author: 李鑫
"""
__author__:"李鑫"
import re#先导入python的内置库

import requests#再导入第三方库

from spider import Spider#最后导入自己的类

class FilmJisu:
    
    domain = 'http://www.caijizy.com'
    
    def __init__(self):
        
       	pass
        
    '''特征函数'''

    #这个函数用来清洗那些导演,主演中有时用,有时用/有使用''分割的情况
    def split_info(selfs, info_str):

        if '/' in info_str:#表示导演用/分割开来

            info_str = info_str.split('/')

        elif ',' in info_str:

            info_str = info_str.split(',')

        elif ' ' in info_str:

            info_str = info_str.split(' ')
            
        elif '[' in info_str:
            
            info_str = info_str.split(',')
            
        elif ']' in info_str:
            
            info_str = info_str.split(' ')

        else:

            info_str = [info_str]

        return [i.strip() for i in info_str if i !='']

#这个函数用来爬取二级页面的信息
    def get_film_info(self, url, encoding = None):
            
        regex = dict(
            #这个爬取的是简介
            intro = '<!--简介开始-->(.*?)<!--简介结束-->',

            #\s+?	\s代表换行或者空格	+最少有一个	?匹配离它最近的
            #片名,更新与评分

            info = '\
        <li class="sa">影片名称: <!--片名开始-->(.*?)<!--片名结束--></li>\s+?\
        <li class="sa">影片别名: <!--别名开始-->(.*?)<!--别名结束--></li>\s+?\
        <li class="sa">影片备注: <!--备注开始-->(.*?)<!--备注结束--></li>\s+?\
        <li class="sa">影片主演: <!--主演开始-->(.*?)<!--主演结束--></li>\s+?\
        <li class="sa">影片导演: <!--导演开始-->(.*?)<!--导演结束--></li>\s+?\
        <li><div class="left">栏目分类: <!--栏目开始-->(.*?)<!--栏目结束--></div><div class="right">影片类型: <!--类型开始-->(.*?)<!--类型结束--></div></li>\s+?\
        <li><div class="left">语言分类: <!--语言开始-->(.*?)<!--语言结束--></div><div class="right">影片地区: <!--地区开始-->(.*?)<!--地区结束--></div></li>\s+?\
        <li><div class="left">连载状态: <!--连载开始-->(.*?)<!--连载结束--></div><div class="right">上映年份: <!--年代开始-->(.*?)<!--年代结束--></div></li>\s+?\
        <li><div class="left">更新时间: <!--时间开始-->(.*?)<!--时间结束--></div><div class="right">豆瓣ID: <!--豆瓣ID开始-->(.*?)<!--豆瓣ID结束--></div></li>',

            show_list = '<input type="checkbox" name="copy_sel" value="(.*?)" checked="">',
            img_src='<!--图片开始--><img src="(.*?)"/>'
        )
            
        info = Spider().get_info(url, encoding = encoding, **regex)

        director = self.split_info(info['info'][0][4])

        actor = self.split_info(info['info'][0][3])

        types = self.split_info(info['info'][0][6])

        area = self.split_info(info['info'][0][8])

        language = self.split_info(info['info'][0][7])

        m3u8_list = [url.split('$') for url in info['show_list'] if url.endswith('.m3u8')]

        yun_list = [url.split('$') for url in info['show_list'] if not url.endswith('m3u8')]


        film_info = dict(

            name = info['info'][0][0],#影片名字
            
            athour_name = info['info'][0][1],#别名
            
            remarks = info['info'][0][2],#备注
            
            actor = actor,#主演
            
            director = director,#导演
            
            column_class = info['info'][0][5],#栏目分类
            
            types = types,#影片类型
            
            language = language,#语言
            
            area = area,#影片地区

            name_info = info['info'][0][9],#连载状态
            
            release_date = info['info'][0][10],#上映年份
            
            up_data = info['info'][0][11],#更新时间

            grade = info['info'][0][12],#影片评分
            
            brief_info = info['intro'][0],#简介

            m3u8_list = m3u8_list,

            yun_list = yun_list,

            imgsrc = info['img_src'][0]#图片链接

        )
        
        
        return film_info


    def film_search(self, keyword, encoding = None):
      
        
        post_url = 'http://www.caijizy.com/index.php?m=vod-search'

        data = {
                'wd': keyword
               }

        regex = dict(

            info = '\
<td class="l"><a href="(.*?)" target="_blank">(.*?)<font color="red">(.*?)</font>\s+?\
<td><a href=".*?" target="_blank">立即播放</a></td>\s+?\
<td><a href="(.*?)" target="_blank">(.*?)</a></td>\s+?\
<td><p><font color="Black">(.*?)</font></p></td>\s+?\
<td><span class="bts_1"><font color="#000000">(.*?)</font></span></td>\s+?\
<td><font color="#2932E1">(.*?)</font></td>'
            )

        info = Spider().post_info(post_url, data, encoding = 'utf-8', **regex)
        
        joint_url = self.domain
        
        #这里一定要用循环遍历
        
        
        info = [{'url' : joint_url + url, 'name' :name + name1,\
                'types_url' : joint_url + types_url, 'types' : types,\
                'area' : area, 'status' : status, 'update_time' : update_time}\
                for url, name, name1, types_url, types, area, status, update_time in info['info']]
        
        
        return {'search_list': info, 'search_word' : keyword, 'host' : self.domain}
    
    
    '''这个函数用来获取首页的信息'''
    def get_show_page_info(self, url):
        

        joint_url = self.domain
        
        regex = dict(
                
                #这里面的更新时间会根据今天是否更新分为两种,所以使用了re中的[]
                info = '\
<td class="l"><a href="(.*?)" target="_blank">(.*?)<font color="red">(.*?)</font>\s+?\
<td><a href=".*?" target="_blank">立即播放</a></td>\s+?\
<td><a href="(.*?)" target="_blank">(.*?)</a></td>\s+?\
<td><p><font color="Black">(.*?)</font></p></td>\s+?\
<td><span class="bts_1"><font color="#000000">完结</font></span></td>\s+?\
<td><font color="#2932E1">(.*?)</font></td>',

                )
        #最好指定encoding这样可以节约时间
        info = Spider().get_info(url, encoding = 'utf-8', **regex)
        
        info = [dict(url = joint_url+i[0], name = i[1]+i[2],types_url = joint_url + i[3], types = i[4],area = i[5], update_time = i[6])for i in info['info']]
        
        return {'film_list':info}
    
    
    def get_page(self):
        
        
        page = None
        
        url = "http://www.caijizy.com/"
        
        regex = dict(
                
                #这个正则用来获取总共的页数
                re_page = '当前:1/(.*?)页'
                
                )
        
        info = Spider().get_info(url, encoding = "utf-8", **regex)
                
        if page == None:
            
             page = int(info['re_page'][0])
             
             
        return page


    '''这个函数用来获取网站上所有的一级网页的url'''
    def get_all_show_page_url_yield(self):

        self.page = self.get_page()
                    
        url = 'http://www.caijizy.com/?m=vod-index-pg-{}.html'
        
        for i in range(1, self.page + 1):
            
            yield url.format(i)
            
            
    def get_all_show_page_url(self):

        self.page = self.get_page()
        
        url = 'http://www.caijizy.com/?m=vod-index-pg-{}.html'
        
        self.queue = [url.format(i) for i in range(1, self.page + 1)]
        
        
        return self.queue
        
    
if __name__=='__main__':
    url = 'http://www.caijizy.com/?m=vod-detail-id-42148.html'
#    url = 'http://www.caijizy.com/?m=vod-index-pg-1.html'
    
    x = FilmJisu()
#    info = x.get_film_info(url)
#x.get_show_page_info()
#    info = x.film_search('银魂')
#    x.get_show_page_info(next(x.pageUrl))
#    x.get_show_page_info(url)
