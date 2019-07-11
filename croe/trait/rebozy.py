                # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Created on Mon May 27 14:18:44 2019

@author: 杨坤
"""
from spider import Spider


class Rebozy:
    
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
    
    domain = 'https://www.rebozy.com'
    
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
                 
                #图片网址
                img_url = '<p class="margin-0 text-center hidden-xs"><a class="copy_btn text-muted" href="javascript:;" data-text="(.*?)">复制图片地址</a></p>',
                
                intro = '<meta name="description" content="(.*?)" />',
                
                name = '<h1 class="title"><!-- 名称 -->(.*?)<!-- end 名称 -->',
                
info = '\
<small class="text-red"><!-- 评分 -->(.*?)<!-- end 评分 --></small></h1>\s+?\
<p class="data"><span class="text-muted">别名：</span><!-- 别名 -->(.*?)<!-- end 别名 --></p>\s+?\
<p class="data">\s+?\
<span class="text-muted">状态：</span><span class="text-red"><!-- 更新 -->(.*?)<!-- end 更新 --></span>\s+?\
<span class="split-line hidden-xs"></span>\s+?\
<span class="text-muted hidden-xs">时间：</span><span class="text-red hidden-xs"><!-- 时间 -->(.*?)<!-- end 时间 --></span>\s+?\
</p>\s+?\
<p class="data"><span class="text-muted">主演：</span><!-- 主演 -->(.*?)<!-- end 主演 --></p>\s+?\
<p class="data"><span class="text-muted">导演：</span><!-- 导演 -->(.*?)<!-- end 导演 --></p>\s+?\
<p class="data hidden-xs">\s+?\
<span class="text-muted">类型：</span><!-- 分类 -->(.*?)<!-- end 分类 -->\s+?\
<span class="split-line"></span>\s+?\
<span class="text-muted">扩展：</span><!-- 扩展 -->(.*?)<!-- end 扩展 -->\s+?\
<span class="split-line"></span>\s+?\
<span class="text-muted">地区：</span><!-- 地区 -->(.*?)<!-- end 地区 -->\s+?\
<span class="split-line"></span>\s+?\
<span class="text-muted">年份：</span><!-- 年份 -->(.*?)<!-- end 年份 -->\s+?\
</p>\s+?\
<p class="data hidden-xs">\s+?\
<span class="text-muted">语言：</span><!-- 语言 -->(.*?)<!-- end 语言 -->\s+?\
<span class="split-line"></span>\s+?\
<span class="text-muted">集数：</span><!-- 集数 -->(.*?)<!-- end 集数 -->\s+?\
<span class="split-line"></span>\s+?\
<span class="text-muted">时长：</span><!-- 时长 -->(.*?)<!-- end 时长 -->\s+?\
<span class="split-line"></span>\s+?\
<span class="text-muted">点击：</span><!-- 点击 -->(.*?)<!-- end 点击 -->\s+?\
</p>',


                show_list = '<input type="checkbox" name=".*?" value="(.*?)" checked>'
                
                )
        info = Spider().get_info(url,encoding = 'utf8', **regex)
        
#      
#        return info
        
       
         #图片url
        imgurl = info['img_url'][0]
        
        #片名
        name = info['name'][0]
        
        #详情
        intro = info['intro'][0]
        
        #评分
        grade = self.split_info(info['info'][0][0])
        #别名
        athour_name = self.split_info(info['info'][0][1])
#        #状态
#        state = self.split_info(info['info'][0][2])
        #时间
        up_date = self.split_info(info['info'][0][3])
        #主演
        actor = self.split_info(info['info'][0][4])
        #导演
        director = self.split_info(info['info'][0][5])
        #类型
        types = self.split_info(info['info'][0][6])
        #扩展
        extend = self.split_info(info['info'][0][7])
        #地区
        area = self.split_info(info['info'][0][8])
        #年份
        show_time = self.split_info(info['info'][0][9])
        #语言
        language = self.split_info(info['info'][0][10])
        #集数
        name_info = self.split_info(info['info'][0][11])
        #片长
        lens = self.split_info(info['info'][0][12])
        #日播放量
        day_plays = self.split_info(info['info'][0][13])
        #rem3u8
        m3u8_list = [url.split('$')  for url in info['show_list'] if url.endswith('.m3u8')]
        #reyun
        yun_list = [url.split('$')  for url in info['show_list'] if not url.endswith('.m3u8')]
        
    
        film_info = dict(
            imgurl = self.domain + imgurl,
            name = name,
            intro= intro,
            grade = grade,
            athour_name = athour_name,
#            state = state,
            up_date = up_date,
            actor = actor,
            director = director,
            types = types,
            extend = extend,
            area = area,
            show_time = show_time,
            language = language,
            name_info = name_info,
            lens = lens,
            day_plays = day_plays,
            m3u8_list = m3u8_list,
            yun_list = yun_list,
            total_score = '',
            total_score_number = '',
            )
        
        
        return film_info
    
    
    def film_search(self, keyword, encoding = None):
        
        post_url = 'https://www.rebozy.com/index.php/vod/search.html'
        
        data = {
                'wd': keyword,
                'submit': 'search',
                
                }
        
        regex = dict(
             
info='<li class="clearfix">\s+?\
	<h3 class="title">\s+?\
		<a href="(.*?)" title="(.*?)">.*?<em>.*?</em></a>\s+?\
	</h3>\s+?\
	<span class="type">\s+?\
		<a href=".*?">(.*?)</a>\s+?\
	</span>\s+?\
	<span class="time">\s+?\
		(.*?)	</span>	'
                )
        
        info = Spider().post_info(post_url, data, encoding, **regex)['info']
        
        print(info)

        
        joint_url = self.domain
        
        info = [{'url':joint_url + url, 'name':name,'types':types, 'update_time': update_time} for url, name,types, update_time in info]
        
        return {'search_list': info, 'search_word': keyword, 'host': self.domain}
    
    
    def get_show_page_info(self,url):
        
        '''
        url:'https://www.rebozy.com/index.php/index/index/page/6.html'
        
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
              
info='<li class="clearfix">\s+?\
	<h3 class="title">\s+?\
		<a href="(.*?)" title="(.*?)">.*? <em>.*?</em></a>\s+?\
	</h3>\s+?\
	<span class="type">\s+?\
		<a href=".*?">(.*?)</a>\s+?\
	</span>\s+?\
	<span class="time">\s+?\
		(.*?)	</span>	'
                
                )
        
        info = Spider().get_info(url,encoding = 'utf-8',  **regex)['info']
        
#        return info
#        info = [dict(url = self.dimain+i[0], name = i[1],types = i[2], update_time = i[3]) for i in info]
        
        info = [{'url':self.domain+i[0],'name':i[1],'types':i[2],'update_time':i[3]} for i in info]
        
        
        
        return {'film_list': info}
        
        
        
    
    def get_all_show_page_url(self):
        
        '''
        return:获取 https://www.rebozy.com/ 网站所有 show_page_url
        
        '''
        
        url = 'https://www.rebozy.com/index.php/index/index/page/{}.html'
        
        self.queue = [url.format(i) for i in range(1, 301)]
        
        
        return self.queue

    
    
    def get_all_show_page_url_yield(self):

        url = 'https://www.rebozy.com/index.php/index/index/page/{}.html'

        for i in range(1, 301):

            yield url.format(i)
            print(url.format(i))       
    
        
if __name__ == '__main__':
    
    url = 'https://www.rebozy.com/index.php/vod/detail/id/3941.html'
#    url = 'https://www.rebozy.com/index.php/index/index/page/2.html'
    
    x = Rebozy()
    #info = x.get_film_info(url)
    
    #info = x.film_search('流浪地球')
    #info = x.get_show_page_info(url)
    #info = x.get_all_show_page_url()
    #info = x.get_all_show_page_url_yield()
    
    
    
    
        
        


