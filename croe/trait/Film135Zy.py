# -*- coding: utf-8 -*-
"""
Created on Thu May 30 19:47:28 2019

@author: dell
"""
from spider import Spider
from multiprocessing.dummy import Pool
pool=Pool(4)
class Film135Zy:
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
            
            获取网站所有的show_page_url的迭代
    
    '''
    
    domain='http://www.135zy.vip'
            
    def film_search(self,keyword,encoding=None):
        post_url='http://www.135zy.vip/index.php?m=vod-search'
        
        data = {
                'wd': keyword,
                'submit': 'search',
                }
        
        regex = dict(
                info = '<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span><span class="xing_vb5">(.*?)</span><span class="xing_vb6">(.*?)</span>'
                )
        
        info = Spider().post_info(post_url, data, encoding, **regex)['info']
        
        #print(info)
        
        joint_url = self.domain
        
        info = [{'url':joint_url + url, 'name':name, 'types':types, 'update_time': update_time} for url, name, types, update_time in info] 
        return {'search_list': info, 'search_word': keyword, 'host': self.domain}
    
   
        
    ##获取一级页面总页数和所有url
    def get_all_show_page_url(self):
        url='http://www.135zy.vip/?m=vod-index-pg-{}.html'
#        regex=dict(
#                page='共.*?条数据&nbsp;当前:1/(.*?)页'
#                )
#        page=Spider().get_info(url,**regex)
        self.queue=[url.format(i) for i in range(1,431)]
        return self.queue
            
    ##获取一级页面总页数和所有url 优化
    def get_all_show_page_url_yield(self):
        url='http://www.135zy.vip/?m=vod-index-pg-{}.html'
#        regex=dict(
#                page='共.*?条数据&nbsp;当前:1/(.*?)页'
#                )
#        page=Spider().get_info(url,**regex)
        for i in range(1,432):
            yield url.format(i)
    
    ##获取二级网页所有url
    def get_show_page_info(self,url):
        regex=dict(
                href='''<ul><li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span><span class="xing_vb5">(.*?)</span><span class="xing_vb[67]">(.*?)</span></li></ul>'''
                )
        one_info=Spider().get_info(url,**regex)['href']
        one_info=[dict(url=self.domain+i[0],name=i[1].split(' ')[0],types=i[2],update_time=i[3]) for i in one_info]
        return {'film_list':one_info}
    
    #3用于数据清洗
    def split_info(self,two_info_str):
        if '/' in two_info_str:
            two_info_str=two_info_str.split('/')
        elif ',' in two_info_str:
            two_info_str=two_info_str.split(',')
        elif ' ' in two_info_str:
            two_info_str=two_info_str.split(' ')
        else:
            two_info_str=[two_info_str]
        return [i.strip() for i in two_info_str if i != '']
  
    ##获取网站的二级网页所有字段
    def get_film_info(self,url,encoding=None):
        regex=dict(
            imgurl='<div class="vodImg"><img class="lazy" src="(.*?)" alt=".*?" />',
            name='<h2>(.*?)</h2>',
            score='<div class="vodh"><h2>.*?</h2><span>(.*?)</span>',
            pingfen='<label>(.*?)</label>',
            info='\
<li>别名：<span>(.*?)</span></li>\
<li>导演：<span>(.*?)</span></li>\
<li>主演：<span>(.*?)</span></li>\
<li>类型：<span>(.*?)</span></li>\
<li>地区：<span>(.*?)</span></li>\
<li>语言：<span>(.*?)</span></li>\
<li>上映：<span>(.*?)</span></li>\
<li>更新：<span>(.*?)</span></li>',
            infro='<strong>剧情介绍：</strong></div><div class="vodplayinfo">(.*?)</div>',
            show_list='checked="" />(.*?)</li>'
            )
        two_info=Spider().get_info(url,encoding,**regex)
        imgurl=two_info['imgurl'][0]
        infro=two_info['infro'][0]
        director=self.split_info(two_info['info'][0][1])
        actor=self.split_info(two_info['info'][0][2])
        types=self.split_info(two_info['info'][0][3])
        area=self.split_info(two_info['info'][0][4])
        language=self.split_info(two_info['info'][0][5])
        m3u8_list=[url.split('$') for url in two_info['show_list'] if url.endswith('.m3u8') ]
        yun_list=[url.split('$') for url in two_info['show_list'] if not url.endswith('.m3u8')]
        
        film_info=dict(
                imgurl=imgurl,
                name=two_info['name'][0],
                name_info=two_info['score'][0],
                pingfen=two_info['pingfen'][0],
                author_name=two_info['info'][0][0],
                director=director,
                actor=actor,
                types=types,
                area=area,
                language=language,
                infro=infro,
                show_time=two_info['info'][0][6],
                up_date=two_info['info'][0][7],
                m3u8_list=m3u8_list,
                yun_list=yun_list
                )
        return film_info

if __name__=='__main__':
    f=Film135Zy()
#    urls=f.get_all_show_page_url_yield()
#    urls=[i for i in urls]
#    urls=urls[:5]
#    ls=[]
#    ls.append(pool.map(f.get_show_page_info,urls[:5]))
#    ls2=[]
#    [ls2.append(i['film_list']) for i in ls[0]]
#    ls3=[]
#    [ls3.append(i[0]['url']) for i in ls2]
    
#    [ls.append(f.get_show_page_info(i)) for i in urls]
#    two_info2=f.get_film_info('http://www.135zy.vip/?m=vod-detail-id-23299.html')
#    four=f.get_page_film('http://www.135zy.vip/?m=vod-index-pg-32.html')

#    for i in one_href['film_list']:
#        two_info2=f.get_film_info(i['href'])
#        print(two_info2)

   
    
        
    
    
    
    
    
    
    
    
    