# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 09:11:53 2019

@author: 一文 --最远的你们是我最近的爱
"""
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from croe.film_spider import Film_spider

import json

import time

# Create your views here.


def index(request):

    return render(request, 'film_search/index.html')
    # return HttpResponse('Hello World !!!')

def search_get(request):

    keyword = request.GET.get('keyword')

    start=time.time()

    count_search_info = 0

    search_info = Film_spider().run(keyword)
    
    print('耗时:',time.time()-start)
    
    for key, value in search_info['search_detail'].items():
        
        count_search_info += len(value)
        
    search_info.update({'count': count_search_info})
        
    context = search_info

    return render(request, 'film_search/search-list.html', context)

def play(request):

    'search/play/?url=http://123ku.com/?m=vod-detail-id-17268.html'

    url = request.GET.get('url')
        
    num = request.GET.get('num')
        
    if num == None:
        
        num = 0
    
    url = url.split('&')[0]
    
    print(url)
    
    detail = Film_spider().play(url)
    
    if detail!='' and len(detail['m3u8_list'])!=0:
    
        detail.update({'show_now_name':detail['m3u8_list'][int(num)][0]})
        
        detail.update({'show_now_url':detail['m3u8_list'][int(num)][1].replace('</span>','')})
        
        name = [(i[0],detail['m3u8_list'].index(i)) for i in detail['m3u8_list']]
                
        detail.update({'m3u8':{'name':name}})
        
        context = detail
    
        return render(request, 'film_search/play.html',context)
    
    else :
        
        return render(request, 'film_search/error.html')

