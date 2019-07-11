# -*- coding: utf-8 -*-
"""
Created on Thu May 30 08:13:53 2019

@author: 夜刀神十香
"""
__author__ = '夜刀神十香'

from spider import Spider


class Zy1977:
    
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
    
    domain = 'http://www.1977zy.com/'
    
    
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
        
            
#        url='http://www.1977zy.com/?m=vod-detail-id-60533.html'
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

                imgurl = '<img class="lazy" src="(.*?)"'


                )
        
        info = Spider().get_info(url, encoding = encoding, **regex)
        
        director = self.split_info(info['director'][0]) #导演
            
        actor = self.split_info(info['actor'][0]) #主演
        
        state = self.split_info(info['state'][0]) #状态
        
        types = self.split_info(info['types'][0]) #类型
        
        area = self.split_info(info['area'][0])  #区域
        
        language = self.split_info(info['language'][0]) #语言
        
        list_97m3u8 = [url.split('$')  for url in info['show_list'] if url.endswith('.m3u8')]
        
        list_1977zy = [url.split('$')  for url in info['show_list'] if not url.endswith('.m3u8')]
        
    
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
                
                imgurl=info['imgurl'][0] ,
                
                show_time = info['show_time'][0],
                
                up_date = info['up_date'][0],
                
                list_97m3u8 = list_97m3u8,
                
                list_1977zy = list_1977zy,
                
                )
        
        
        return film_info
    
    def film_search(self, keyword, encoding = None):
        
        post_url = 'http://www.1977zy.com/index.php?m=vod-search'
                   
        
        data = {
                'wd': keyword,
                'submit': 'search',
                
                }
        
        regex = dict(
                                                                                                                                                                                                                                                                                                                                
                info = '<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)<font color="#FF0000">(.*?)</font></a></span><span class="xing_vb51">(.*?)</span> <span class="xing_vb52">(.*?)</span> <span class="xing_vb54">(.*?)</span><span class="xing_vb53"><font color="#f60">(.*?)</font></span>  <span class="xing_vb[67]">(.*?)</span></li>'
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
                
#                info = '<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)<font color="#FF0000">(.*?)</font></a></span><span class="xing_vb51">(.*?)</span> <span class="xing_vb52">(.*?)</span> <span class="xing_vb54">(.*?)</span><span class="xing_vb53"><font color="#f60">(.*?)</font></span>  <span class="xing_vb[67]">(.*?)</span></li>'
                info ='\
<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)<font color="#FF0000">(.*?)</font></a></span><span class="xing_vb51">(.*?)</span><span class="xing_vb52">(.*?)</span><span class="xing_vb54">(.*?)</span><span class="xing_vb53"><font color="#f60">(.*?)</font></span>.*?<span class="xing_vb[67]">(.*?)</span></li>'
                )
        
        info = Spider().get_info(url,encoding = 'utf-8',  **regex)['info']

        info = [dict(url = i[0], name = i[1].split('&nbsp;')[0], update_total = i[2], types = i[3], erae = i[4], show_time = i[5], pingfen=i[6], update_time = i[7]) for i in info]
        
        
        
        return {'film_list': info}
        
        
        
    
    def get_all_show_page_url(self):
        
        '''
        return:获取 http://www.1977zy.com/ 网站所有 show_page_url
        
        '''
        
        url = 'http://www.1977zy.com/?m=vod-index-pg-{}.html'
        
        self.queue = [url.format(i) for i in range(1, 536)]
        
        
        return self.queue

    
    
    def get_all_show_page_url_yield(self):

        url = 'http://www.1977zy.com/?m=vod-index-pg-{}.html'

        for i in range(1, 536):

            yield url.format(i)
                
    
        
if __name__ == '__main__':
    
    url = 'http://www.1977zy.com/?m=vod-index-pg-1.html'
    
    x = Zy1977()
    
#    a = x.get_all_show_page_url_yield()
#    
#    ls = []
#    
#    for i in range(10):
#        
#        u = next(a)
        
#        ls.append(x.get_show_page_info(u))
#    info = x.get_show_page_info(url)
#    info = x.film_search('龙珠')