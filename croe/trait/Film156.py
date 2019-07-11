# -*- coding: utf-8 -*-
"""
@author: 刘晶一
"""
__author__ = '刘晶一'
from spider import Spider

class Film156:
    
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
    
    domain = 'http://www.156zy.co/'
    
    
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
                              
                intro = '<div class="vodplayinfo">(.*?)</div>',
                
                name = '<h2><!--片名开始-->(.*?)<!--片名结束--></h2>\s+?<span><!--备注开始-->(.*?)<!--备注结束--></span>\s+?<label>(.*?)</label>',
                
                imgurl='<img class="lazy" src="(.*?)" alt=".*?" />',
                
                info = '\
<li>别名：<span><!--别名开始-->(.*?)<!--别名结束--></span></li>\s+?\
<li>导演：<span><!--导演开始-->(.*?)<!--导演结束--></span></li>\s+?\
<li>主演：<span><!--主演开始-->(.*?)<!--主演结束--></span></li>\s+?\
<li>类型：<span><!--类型开始-->(.*?)<!--类型结束--> </span></li>\s+?\
<li>地区：<span><!--地区开始-->(.*?)<!--地区结束--></span></li>\s+?\
<li>语言：<span><!--语言开始-->(.*?)<!--语言结束--></span></li>\s+?\
<li>上映：<span><!--上映开始-->(.*?)<!--上映结束--></span></li>\s+?\
<li>更新：<span>(.*?)</span></li>',


                show_list = 'checked="" />(.*?)</li>'



                )
        
        info = Spider().get_info(url, encoding = encoding, **regex)
        
        director = self.split_info(info['info'][0][1])
            
        actor = self.split_info(info['info'][0][2])
        
        types = self.split_info(info['info'][0][3])
        
        area = self.split_info(info['info'][0][4])
        
        language = self.split_info(info['info'][0][5])
        
        m3u8_list = [url.split('$')  for url in info['show_list'] if url.endswith('.m3u8')][1:]
        
        yun_list = [url.split('$')  for url in info['show_list'] if not url.endswith('.m3u8')][:-1]
        
    
        film_info = dict(
                
                name = info['name'][0][0],
                
                name_info = info['name'][0][1],
                
                grade = info['name'][0][2],
                
                athour_name = info['info'][0][0],
                
                director = director,
                
                actor = actor,
                
                types = types,
                
                area = area,
                
                imgurl=info['imgurl'][0],
                
                language = language,
                
                show_time = info['info'][0][6],
                
                up_date = info['info'][0][7],
                
                m3u8_list = m3u8_list,
                
                yun_list = yun_list,
                
                day_plays='',
                
                lens='',
                
                total_score='',
                
                total_score_number=''
                
                )
        
        
        return film_info
    
    
    def film_search(self, keyword, encoding = None):
        
        post_url = 'http://www.156zy.co/index.php?m=vod-search'
        

        data = {
                'wd': keyword,
                'submit': 'search',
                
                }
        
        regex = dict(
                
                info = '<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb6">(.*?)</span></li>'
                )
        
        
        info = Spider().post_info(post_url, data, **regex)['info']
        
        #print(info)
        
        joint_url = self.domain
        
        info = [{'url':joint_url + url[1:], 'name':name, 'types':types, 'update_time': update_time} for url, name, types, update_time in info]
        
        return {'search_list': info, 'search_word': keyword, 'host': self.domain}
    
    
    def get_show_page_info(self,url):
        
  
        regex = dict(
                
                info = '<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb[67]">(.*?)</span></li>'
                
                
                )
        
        info = Spider().get_info(url,encoding = 'utf-8',**regex)['info']
        
        info = [dict(url = 'http://www.156zy.co'+i[0], name = i[1].split('&nbsp;')[0], types = i[2], update_time = i[3]) for i in info]
        
        
        
        return {'film_list': info}
        
        
        
    
    def get_all_show_page_url(self,):
        
        '''
        return:获取 http://www.156zy.co/ 网站所有 show_page_url
        
        '''
        
        url = 'http://www.156zy.co/?m=vod-index-pg-{}.html'
        
        
        
        self.queue = [url.format(i) for i in range(1, 540)]
        
        
        return self.queue

    
    
    def get_all_show_page_url_yield(self):

        url = 'http://www.156zy.co/?m=vod-index-pg-{}.html'

        for i in range(1, 540):

            yield url.format(i)
    
#    def get_all_page(self,url):
#        
#        rst = Spider().get_html(url)
#        
#        ye = int(str(re.findall('<li><div class="pages" style="margin-bottom:10px;">共.*?条数据&nbsp;当前:1/(.*?)页&nbsp;<em>',rst,re.S))[2:-2])
#        
#        return ye
        
if __name__ == '__main__':
    
    url = 'http://www.156zy.co/?m=vod-index-pg-1.html'
    
    x = Film156()
    
#    yes = x.get_all_page(url)
    
    #info = x.get_film_info('http://www.156zy.co/?m=vod-detail-id-3975.html')
    
    #info = x.film_search('小黄人和萌友')
    
    
    #传入一个show_page_url返回所有电影信息
    #info = x.get_show_page_info('http://www.156zy.co/?m=vod-type-id-3-pg-9.html')

    #获取网站所有的show_page_url
    #info = x.get_all_show_page_url()
    
    #info = x.get_all_show_page_url_yield()
        
        


