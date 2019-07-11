# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:28:18 2019

@author: 一文 --最远的你们是我最近的爱
"""
import requests
from spider import Spider
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Filmbj:
    
    domain = 'https://bajiezy.cc/'
    
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
                              
                intro = '<!--简介开始-->(.*?)<!--简介结束-->',
                
                imgurl = '<div class="videoPic"><!--图片开始--><img src="(.*?)"/><!--图片结束--></div>',
                
                info='<li class="sa">影片名称: <!--片名开始-->(.*?)<!--片名结束--></li>\s+?\
<li class="sa">影片别名: <!--别名开始-->(.*?)<!--别名结束--></li>\s+?\
<li class="sa">影片备注: <!--备注开始-->(.*?)<!--备注结束--></li>\s+?\
<li class="sa">影片主演: <!--主演开始-->(.*?)<!--主演结束--></li>\s+?\
<li class="sa">影片导演: <!--导演开始-->(.*?)<!--导演结束--></li>\s+?\
<li><div class="left">栏目分类: <!--栏目开始-->(.*?)<!--栏目结束--></div><div class="right">影片类型: <!--类型开始-->(.*?)<!--类型结束--></div></li>\s+?\
<li><div class="left">语言分类: <!--语言开始-->(.*?)<!--语言结束--></div><div class="right">影片地区: <!--地区开始-->(.*?)<!--地区结束--></div></li>\s+?\
<li><div class="left">连载状态: <!--连载开始-->(.*?)<!--连载结束--></div><div class="right">上映年份: <!--年代开始-->(.*?)<!--年代结束--></div></li>\s+?\
<li><div class="left">更新时间: <!--时间开始-->(.*?)<!--时间结束--></div><div class="right"><font color=red>豆瓣评分:</font> <!--豆瓣ID开始-->(.*?)<!--豆瓣ID结束--></div></li>',
        
                show_list = 'checked=""><span>(.*?)</li>'

                )
        
        
        
        info = Spider().get_info(url, encoding = encoding, **regex)
                
        director = self.split_info(info['info'][0][4])
            
        actor = self.split_info(info['info'][0][3])
        
        types = self.split_info(info['info'][0][5])
        
        area = self.split_info(info['info'][0][8])
        
        language = self.split_info(info['info'][0][7])
        
        m3u8_list = [url.split('$')  for url in info['show_list'] if url.endswith('.m3u8')]
        
        yun_list = [url.split('$')  for url in info['show_list'] if not url.endswith('.m3u8')]
    
        film_info = dict(
                
                intro = str(info['intro']).replace('[','').replace(']',''),
                
                imgurl = info['imgurl'],
                
                name = info['info'][0][0],
                
                name_info = info['info'][0][2],
                
                grade = info['info'][0][12],
                
                athour_name = info['info'][0][0],
                
                director = director,
                
                actor = actor,
                
                types = types,
                
                area = area,
                
                language = language,
                
                show_time = info['info'][0][10],
                
                up_date = info['info'][0][11],
                
                m3u8_list = m3u8_list,
                
                yun_list = yun_list,
                
                )
        
        
        return film_info
    
    
    def film_search(self, keyword, encoding = None):
        
        post_url = 'https://bajiezy.cc/index.php?m=vod-search'
        
        data = {
                'wd': keyword
                }
        
        regex = dict(
                
                  info='<td class="l"><a href="(.*?)" target="_blank">(.*?)<font color="red">(.*?)</font>\s+?\
  <td><p><font color="Black">(.*?)</font></p></td>\s+?\
  <td><a href="(.*?)" target="_blank">(.*?)</a></td>\s+?\
  <td><p><font color="Black">(.*?)</font></p></td>\s+?\
  <td><span class="bts_1">(.*?)</span></td>\s+?\
  <td><font color="#2932E1">(.*?)</font></td>'
              
                )
        
        info = Spider().post_info(post_url, data, encoding, **regex)
        
        joint_url = self.domain
        
        info = [{'url':joint_url + url[1:], 'name':name, 'types':types, 'update_time': update_time} for url, name,  status, p_time, s_url, types, area, grade, update_time in info['info']]
        
        return {'search_list': info, 'search_word': keyword, 'host': self.domain}
    
    
    def get_show_page_info(self,url):
        
        regex = dict(
                
                  info='<td class="l"><a href="(.*?)" target="_blank">(.*?)<font color="red">(.*?)</font>\s+?\
  <td><p><font color="Black">(.*?)</font></p></td>\s+?\
  <td><a href="(.*?)" target="_blank">(.*?)</a></td>\s+?\
  <td><p><font color="Black">(.*?)</font></p></td>\s+?\
  <td><span class="bts_1">(.*?)</span></td>\s+?\
  <td><font color="#2932E1">(.*?)</font></td>'
              
                )
        
        info = Spider().get_info(url,encoding = 'utf-8',  **regex)
        
        joint_url = self.domain
        
        info = [{'url':joint_url + url[1:], 'name':name, 'types':types, 'update_time': update_time} for url, name,  status, p_time, s_url, types, area, grade, update_time in info['info']]
        
        return {'film_list': info}
        
    
    def get_all_show_page_url(self):
        
        url = 'https://bajiezy.cc/?m=vod-index-pg-{}.html'
        
        self.queue = [url.format(i) for i in range(1,275)]
        
        return self.queue
    
        
    def get_all_show_page_url_yield(self):

        url = 'https://bajiezy.cc/?m=vod-index-pg-{}.html'

        for i in range(1, 275):

            yield url.format(i)
                
    
        
if __name__ == '__main__':
    
    x = Filmbj()
