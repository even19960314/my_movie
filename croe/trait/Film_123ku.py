# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:04:28 2019

@author: 刘婷婷
"""
from spider import Spider
import re
from math import ceil
class Film123ku:
    
    
    domain = 'http://www.123ku.com/'
    
    def get_page(self,url,**regex):
        regex=dict(
                page='123资源站影片共有：<strong>(.*?)</strong>'
                )
        page=Spider().get_info(url,**regex)['page'][0]
        page=ceil(int(page)/50)
        return page
    
    def get_film_info(self,url,encoding=None):
        
        regex=dict(
                intro='<div class="vodplayinfo"><!--介绍开始-->(.*?)<!--介绍结束--></div>',
                name='<h2><!--片名开始-->(.*?)<!--片名结束--></h2>\s+?<span><!--备注开始-->(.*?)<!--备注结束--></span>\s+?<label>(.*?)</label>',
                anthor='<li>别名：<span><!--别名开始-->(.*?)<!--别名结束--></span></li>',
                director="<li>导演：<span><!--导演开始--><a target='_blank' href='.*?'>(.*?)</a>&nbsp;<!--导演结束--></span></li>",
                act="<li>主演：<span><!--主演开始--><a target='_blank' href='.*?'>(.*?)</a>&nbsp;<!--主演结束--></span></li>",
                jieshao='''\
<li>类型：<span><!--类型开始-->(.*?)<!--类型结束--></span></li>\s+?\
<li>地区：<span><!--地区开始--><a target='_blank' href='.*?'>(.*?)</a>&nbsp;<!--地区结束--></span></li>\s+?\
<li>语言：<span><!--语言开始--><a target='_blank' href='.*?'>(.*?)</a>&nbsp;<!--语言结束--></span></li>\s+?\
<li>上映：<span><!--上映开始--><a target='_blank' href='.*?'>(.*?)</a>&nbsp;<!--上映结束--></span></li>\s+?\
<li>更新：<span>(.*?)</span></li>\s+?\
<li class="sm">片长：<span>(.*?)</span></li>\s+?\
<li class="sm">更新：<span>(.*?)</span></li>\s+?\
<li class="sm">总播放量：<span><em id="hits">.*?</script></span></li>\s+?\
<li class="sm">今日播放量：<span>(.*?)</span></li>\s+?\
<li class="sm">总评分数：<span>(.*?)</span></li>\s+?\
<li class="sm">评分次数：<span>(.*?)</span></li>\s+?\
<li class="sm">影片评分：<span><script>.*?</script></span></li>''',

                show_list = 'target="_black">(.*?)</a>',
                imgurl='<img class="lazy" src="(.*?)" alt=".*?" />'
                )
        info=Spider().get_info(url,**regex)
        
        if len(info['act']) ==0:
            act=''
        else:   
            act=info['act'][0]
            act=re.findall('[\u4e00-\u9fa5]+',act)
        
        if len(info['director']) ==0:
            info['director']=''
        else:
            directors=info['director'][0]
            director=re.findall('[\u4e00-\u9fa5]+',directors)
            
        m3u8_list = [url.split('$')  for url in info['show_list'] if url.endswith('.m3u8')]
        
        yun_list = [url.split('$')  for url in info['show_list'] if not url.endswith('.m3u8')]
        
        
        x=info['jieshao'][0]
        film_info=dict(
                imgurl=info['imgurl'][0],
                name = info['name'][0][0],
                name_info = info['name'][0][1],
                grade = info['name'][0][2],
                athour_name=info['anthor'][0],
                director=director,
                act=act,
                types=x[0],
                area=x[1],
                language=x[2],
                show_time=x[3],
                up_date=x[4],
                lens=x[5],
                day_plays=x[7],
                total_score=x[8],
                total_score_number=x[9],
                m3u8_list=m3u8_list,
                yun_list=yun_list
                )
        return film_info
    
    def film_search(self,keyword,encoding=None):
        post_url='http://www.123ku.com/index.php?m=vod-search'
        data={
             'wd': keyword,
             'submit': 'search',
                }
        regex = dict(
                
                info = '<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb6">(.*?)</span></li>'
                )
        joint_url = self.domain
        info = Spider().post_info(post_url, data, encoding, **regex)['info']
        info = [{'url':joint_url + url[1:], 'name':name, 'types':types, 'update_time': update_time} for url, name, types, update_time in info]
        return {'search_list': info, 'search_word': keyword, 'host': self.domain}
        
    def get_show_page_info(self,url):
        regex = dict(
                info = '<li><span class="tt"></span><span class="xing_vb4"><img class="new" src="/template/www_api_xin/images/new/49.gif">&nbsp<a href="(.*?)">(.*?)<img class="hot" src="/template/www_api_xin/images/hot/hot.gif"></font></a></span> <span class="xing_vb5">(.*?)</span> <span class="xing_vb6">(.*?)</span></li>'
                )
        info = Spider().get_info(url,encoding = 'utf-8',  **regex)['info']
        info = [dict(url = self.domain+i[0], name = i[1].split('&nbsp')[0], types = i[2], update_time = i[3]) for i in info]
        return {'film_list': info}
    
    def get_all_show_page_url(self):

        url = 'http://www.123ku.com/?m=vod-index-pg-{}.html'
        
        page=self.get_page('http://www.123ku.com/')
        
        self.queue = [url.format(i) for i in range(1, page+1)]
        
        return self.queue
    
    
    def get_all_show_page_url_yield(self):

        url = 'http://www.123ku.com/?m=vod-index-pg-{}.html'
        
        page=self.get_page('http://www.123ku.com/')
        
        for i in range(1, page+1):

            yield url.format(i)
    
    
        
if __name__ == '__main__':
    url='https://123ku.com/?m=vod-detail-id-10973.html'
    f=Film123ku()
    
#    info=f.get_film_info(url)
        
        
        
        
        
        
        