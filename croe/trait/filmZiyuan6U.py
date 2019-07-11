# -*- coding: utf-8 -*-
"""
Created on Wed May 29 20:20:46 2019
6u资源站
@author: 张茗杰
"""
__author__ = '张茗杰'

from spider import Spider


class FilmZiyuan6U:
    
    
    '''
    get_page(self) 获取页数
    
    def split_info(self, info_str) 分割字符串
    
    def get_film_info(self,url,encoding = None) 获取电影详情页字段
    
    film_search(self, keyword, encoding = None) 关键字查询
    
    get_all_show_page_url(self) 获取所有页的url
    
    get_all_show_page_url_yield(self) 返回url的迭代器
    
    get_show_page_info(self,url) 获取每页的50条电影字段
    '''
    
    domain =  'http://zy.ataoju.com/'
    
    def get_page(self):
        url = 'http://zy.ataoju.com/index.php'
        regex = dict(
                page = '<div class="pages" style="margin-bottom:10px;">共.*?条数据&nbsp;当前:.*?/(.*?)页&nbsp;<em>'
                )
        page = Spider().get_info(url,**regex)
        return int(page['page'][0])
    
    
    def split_info(self, info_str):
        if '/' in info_str:
            info_str = info_str.split('/')
        elif ',' in info_str:
            info_str = info_str.split(',')
        elif ' ' in info_str:
            info_str = info_str.split(' ')
        else:
            info_str = [info_str]
        return [i.strip() for i in info_str if i != '']
    
    def get_film_info(self,url,encoding = None):
        regex = dict(
                intro ='<div class="vodplayinfo">(.*?)</div>',
                name = '<h2>(.*?)</h2>\s+?<span>(.*?)</span>\s+?<label>(.*?)</label>',
                info = '\
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
                show_list = 'target=_blank>(.*?)</a>&emsp;',
                imgurl = '<img class="lazy" src="(.*?)" alt=".*?" />'
                )
        info = Spider().get_info(url,encoding = encoding,**regex)
        director = self.split_info(info['info'][0][1])
        actor = self.split_info(info['info'][0][2])
        types = self.split_info(info['info'][0][3])
        area = self.split_info(info['info'][0][4])
        language = self.split_info(info['info'][0][5])
        
        film_info = dict(
                name = info['name'][0][0],
                name_info = info['name'][0][1],
                grader = info['name'][0][2],
                athour_name = info['info'][0][0],
                director = director,
                actor = actor,
                types = types,
                area = area,
                language = language,
                show_time = info['info'][0][6],
                lens = info['info'][0][7],
                up_date = info['info'][0][8],
                day_palys = info['info'][0][9],
                total_score = info['info'][0][10],
                total_score_number = info['info'][0][11],
                intro = info['intro'][0],
                m3u8_list = [i.split('$') for i in info['show_list'] if i.endswith('index.m3u8')],
                yun_list = [i.split('$') for i in info['show_list'] if not i.endswith('index.m3u8')],
                imgurl = info['imgurl'][0]
                )
        return film_info
        
        #关键字查询
    def film_search(self, keyword, encoding = None):
        post_url = 'http://zy.ataoju.com/index.php?m=vod-search'
        data = {
                'wd': keyword,
                'submit': 'search'
                }
        regex = dict(
                info = '<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb[67]">(.*?)</span></li>'
                )
        info = Spider().post_info(post_url,data,**regex)
        info = [{'url':self.domain+i[0],'name':i[1],'types':i[2],'update_time':i[3]} for i in info['info']]
        return {'search_list': info, 'search_word': keyword, 'host': self.domain}
    
    
    #获取所有的url
    def get_all_show_page_url(self):
        page = self.get_page()
        join_url = 'http://zy.ataoju.com/?m=vod-index-pg-{}.html'
        self.queue = [join_url.format(i) for i in range(1,page+1)]
        return self.queue
    
    #获取url 优化
    def get_all_show_page_url_yield(self):
        page = self.get_page()
        join_url = 'http://zy.ataoju.com/?m=vod-index-pg-{}.html'
        for i in range(1,page+1):
            yield join_url.format(i)


    def get_show_page_info(self,url):
        regex = dict(
                info = '<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb[67]">(.*?)</span></li>'
                )
        info = Spider().get_info(url,**regex)['info']
        info = [{'url':self.domain+i[0],'name':i[1],'types':i[2],'update_time':i[3]} for i in info]
        return {'film_list':info}
    
    
if __name__ == '__main__' :
    z = FilmZiyuan6U()
    url = 'http://zy.ataoju.com/?m=vod-index-pg-40.html'
#    info = z.get_film_info('http://zy.ataoju.com/?m=vod-detail-id-61989.html')
#    page = z.get_page()
    info1 = z.get_all_show_page_url_yield()
    __author__
#    urls = z.get_all_show_page()
#    info3 = z.get_all_page(url)
#    print(type(z.get_all_show_page_yield()))