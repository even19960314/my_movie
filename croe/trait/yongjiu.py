# -*- coding: utf-8 -*-
"""
Created on Thu May 30 07:55:05 2019

@author: 张荣辉
"""
__author__ = '张荣辉'
from spider import Spider


class Yongjiu:
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
    domain = 'http://www.yongjiuzy.cc/'
    
    def split_info(self, info_str):#一个用在清洗数据的方法
        '''清洗数据'''
        if '/' in info_str:#用/分割开来
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
                intro ='<!--简介开始-->(.*?)<!--简介结束-->',
                info = '\
<li class="sa">影片名称: <!--片名开始-->(.*?)<!--片名结束--></li>\s+?\
<li class="sa">影片别名: <!--别名开始-->(.*?)<!--别名结束--></li>\s+?\
<li class="sa">影片备注: <!--备注开始-->(.*?)<!--备注结束--></li>\s+?\
<li class="sa">影片主演: <!--主演开始-->(.*?)<!--主演结束--></li>\s+?\
<li class="sa">影片导演: <!--导演开始-->(.*?)<!--导演结束--></li>\s+?\
<li><div class="left">栏目分类: <!--栏目开始-->(.*?)<!--栏目结束--></div><div class="right">影片类型: <!--类型开始-->(.*?)<!--类型结束--></div></li>\s+?\
<li><div class="left">语言分类: <!--语言开始-->(.*?)<!--语言结束--></div><div class="right">影片地区: <!--地区开始-->(.*?)<!--地区结束--></div></li>\s+?\
<li><div class="left">连载状态: <!--连载开始-->(.*?)<!--连载结束--></div><div class="right">上映年份: <!--年代开始-->(.*?)<!--年代结束--></div></li>\s+?\
<li><div class="left">更新时间: <!--时间开始-->(.*?)<!--时间结束--></div><div class="right">豆瓣ID: <!--豆瓣ID开始-->(.*?)<!--豆瓣ID结束--></div></li>\s+?',
            show_list='<input type="checkbox" name="copy_sel" value="(.*?)" checked="">',        
			imgurl='<div class="videoPic"><!--图片开始--><img src="(.*?)"/><!--图片结束--></div>'
        )
        
        info = Spider().get_info(url, encoding = encoding, **regex)
        
        actor = self.split_info(info['info'][0][3])#主演
        types = self.split_info(info['info'][0][5])#栏目分类
#        types = self.split_info(info['info'][0][6])#影片类型
        area = self.split_info(info['info'][0][8])#影片地区
        director = self.split_info(info['info'][0][4])#导演
        language = self.split_info(info['info'][0][7])#语言分类
        
        m3u8_list = [url.split('$')[1]  for url in info['show_list'] if url.endswith('.m3u8')]
        yun_list = [url.split('$')[1]  for url in info['show_list'] if not url.endswith('.m3u8')]
        
        film_info = dict(
                imgurl=info['imgurl'][0],
                name = info['info'][0][0],#影片名称
                name_info = '',
                grader = '',
                another_name = info['info'][0][1],#影片别名
                director = director,#影片导演
                actor = actor,
                types = types,
                area = area,
                language = language,
                show_time = info['info'][0][10],#上映年份
                length = '',
                update_time =info['info'][0][11],#更新时间
                day_palys = '',
                total_score = '',
                total_score_number = '',
                intro = info['intro'][0],
                m3u8_list = m3u8_list,
                yun_list = yun_list,
                
                film_remark = info['info'][0][2],#影片备注
                serial_state = info['info'][0][9],#连载状态
                halves_id = info['info'][0][12],#豆瓣id
                )
        
        
        return film_info
    
    
    def film_search(self, keyword, encoding = None):
        '''搜索页面解析'''
        post_url = 'http://www.yongjiuzy.cc/index.php?m=vod-search'
        data = {
                'wd': keyword
                }
        regex = dict(
                name = '<td class="l"><a href="\S+" target="_blank">(.*?)<font color="red">(.*?)</font>\s+?',
                urls = '<td class="l"><a href="(.*?)" target="_blank">\S+',
                types = '<td><a href="\S+" target="_blank">(.*?)</a></td>\s+?',
                update_time='<td><font color="#2932E1">(.*?)</font></td>\s+?'
                )
        
        info = Spider().post_info(post_url, data, encoding, **regex)
        search_list=[]
        info['urls']=['http://www.yongjiuzy.cc/'+x for x in info['urls']]
        info['name'] = [''.join(x) for x in info['name']]
        for name,url,types,update_time in zip(info['name'],info['urls'],info['types'],info['update_time']):
            search_list.append({'name':name,'url':url,'types':types,'update_time':update_time})
        return {'search_list': search_list, 'search_word': keyword, 'host': self.domain}
       
    def get_show_page_info(self,url):
        '''一级页面解析'''
        regex = dict(
                name = '<td class="l"><a href="\S+" target="_blank">(.*?)<font color="red">(.*?)</font>\s+?',
                urls = '<td class="l"><a href="(.*?)" target="_blank">\S+',
                types = '<td><a href="\S+" target="_blank">(.*?)</a></td>\s+?',
#                areas = '<td><p><font color="Black">(.*?)</font></p></td>\s+?',
#                serial_state= '<td><span class="bts_1"><font color="\S+">(.*?)</font></span></td>\s+?',
                update_time='<td><font color="#2932E1">(.*?)</font></td>\s+?'
                )
        
        info = Spider().get_info(url,encoding = 'utf-8',  **regex)
        search_list=[]
        info['name'] = [''.join(i) for i in info['name']]
        info['urls']=['http://www.yongjiuzy.cc/'+x for x in info['urls']]
        for name,url,types,update_time in zip(info['name'],info['urls'],info['types'],info['update_time']):
            search_list.append({'name':name,'url':url,'types':types,'update_time':update_time})
        return {'film_list': search_list}
    
    def get_all_show_page_url(self):
        '''获取所有的页面url列表'''
        url = 'http://www.yongjiuzy.cc/?m=vod-index-pg-{}.html'
        self.queue = [url.format(i) for i in range(1, 480+1)]
        return self.queue

    def get_all_show_page_url_yield(self):
        '''页面url生成器'''
        url = 'http://www.yongjiuzy.cc/?m=vod-index-pg-{}.html'
        for i in range(1, 480+1):
            yield url.format(i)
                
        
if __name__ == '__main__':
    
    url='http://www.yongjiuzy.cc/?m=vod-index-pg-2.html'    
    spider = YongJiuSpider()
#    url='https://http://www.yongjiuzy.cc/?m=vod-detail-id-2.html'

    info=spider.get_show_page_info(url)
#    info=spider.get_show_page_info(url)
#    info = spider.film_search('筑梦情缘')
